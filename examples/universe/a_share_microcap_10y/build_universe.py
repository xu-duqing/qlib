from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
OUTPUT_ROOT = ROOT / "outputs"
TUSHARE_URL = "https://api.tushare.pro"
A_SHARE_SUFFIX = (".SZ", ".SH", ".BJ")
EXCLUDED_MARKERS = ("ST", "*ST", "退", "退市")


@dataclass
class TushareClient:
    token: str

    def call(self, api_name: str, params: dict | None = None, fields: str = "") -> pd.DataFrame:
        payload = json.dumps(
            {
                "api_name": api_name,
                "token": self.token,
                "params": params or {},
                "fields": fields,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            TUSHARE_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            obj = json.loads(resp.read().decode("utf-8"))
        if obj.get("code") != 0:
            raise RuntimeError(f"Tushare API {api_name} failed: code={obj.get('code')} msg={obj.get('msg')}")
        data = obj.get("data") or {}
        fields_list = data.get("fields") or []
        items = data.get("items") or []
        return pd.DataFrame(items, columns=fields_list)


def load_token() -> str:
    p = Path.home() / "tk.csv"
    rows = list(csv.reader(p.open()))
    if len(rows) > 1:
        return rows[1][0].strip()
    return rows[0][0].strip()


def active_name_for_date(name_changes: pd.DataFrame, ts_code: str, trade_date: str, fallback_name: str) -> str:
    sub = name_changes[name_changes["ts_code"] == ts_code]
    if sub.empty:
        return fallback_name
    for _, row in sub.iterrows():
        start = row["start_date"] or "00000000"
        end = row["end_date"] or "99991231"
        if start <= trade_date <= end:
            return row["name"]
    return fallback_name


def is_excluded_name(name: str) -> tuple[bool, str | None]:
    if not isinstance(name, str):
        return False, None
    normalized = name.upper()
    if "*ST" in normalized or normalized.startswith("ST") or " ST" in normalized:
        return True, "st"
    if any(marker in name for marker in ("退市", "退")):
        return True, "delist_arrangement"
    return False, None


def build_open_unopened_ipo_map(limit_df: pd.DataFrame, stock_basic: pd.DataFrame) -> dict[str, set[str]]:
    list_date_map = dict(zip(stock_basic["ts_code"], stock_basic["list_date"]))
    result: dict[str, set[str]] = defaultdict(set)
    if limit_df.empty:
        return result
    limit_df = limit_df.copy()
    limit_df = limit_df.sort_values(["ts_code", "trade_date"])
    for ts_code, group in limit_df.groupby("ts_code"):
        list_date = list_date_map.get(ts_code)
        if not list_date:
            continue
        for _, row in group.iterrows():
            trade_date = str(row["trade_date"])
            if trade_date < list_date:
                continue
            is_up = row.get("limit") == "U"
            open_times = row.get("open_times")
            unopened = is_up and pd.notna(open_times) and float(open_times) == 0
            if unopened:
                result[ts_code].add(trade_date)
            else:
                # once opened/non-limit encountered after listing, stop excluding subsequent days
                break
    return result


def previous_trade_date_map(trade_dates: list[str]) -> dict[str, str | None]:
    prev = {}
    last = None
    for d in trade_dates:
        prev[d] = last
        last = d
    return prev


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-date", default=None)
    parser.add_argument("--end-date", default=None)
    parser.add_argument("--lookback-years", type=int, default=10)
    parser.add_argument("--bottom-n", type=int, default=400)
    parser.add_argument("--mv-field", choices=["total_mv", "circ_mv"], default="total_mv")
    args = parser.parse_args()

    token = load_token()
    client = TushareClient(token)

    cal = client.call(
        "trade_cal",
        {"exchange": "SSE", "start_date": "20100101", "end_date": datetime.now().strftime("%Y%m%d")},
        "exchange,cal_date,is_open,pretrade_date",
    )
    cal = cal[cal["is_open"] == 1].copy().sort_values("cal_date")
    trade_dates_all = cal["cal_date"].astype(str).tolist()
    end_date = args.end_date or trade_dates_all[-1]
    if args.start_date:
        start_date = args.start_date
    else:
        end_dt = datetime.strptime(end_date, "%Y%m%d")
        start_dt = end_dt - timedelta(days=365 * args.lookback_years + 30)
        start_date = start_dt.strftime("%Y%m%d")
    trade_dates = [d for d in trade_dates_all if start_date <= d <= end_date]
    prev_map = previous_trade_date_map(trade_dates)

    stock_basic = client.call(
        "stock_basic",
        {"exchange": "", "list_status": "L"},
        "ts_code,symbol,name,market,list_date,delist_date",
    )
    stock_basic = stock_basic[stock_basic["ts_code"].str.endswith(A_SHARE_SUFFIX)].copy()

    name_changes = client.call(
        "namechange",
        {"start_date": start_date, "end_date": end_date},
        "ts_code,name,start_date,end_date,ann_date,change_reason",
    )
    if not name_changes.empty:
        name_changes["start_date"] = name_changes["start_date"].fillna("00000000").astype(str)
        name_changes["end_date"] = name_changes["end_date"].fillna("99991231").astype(str)

    daily_frames = []
    daily_basic_frames = []
    limit_frames = []
    for td in trade_dates:
        daily_basic_frames.append(
            client.call(
                "daily_basic",
                {"trade_date": td},
                f"ts_code,trade_date,close,{args.mv_field},total_mv,circ_mv,free_share,total_share,turnover_rate,volume_ratio",
            )
        )
        daily_frames.append(
            client.call(
                "daily",
                {"trade_date": td},
                "ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount",
            )
        )
        limit_frames.append(
            client.call(
                "limit_list_d",
                {"trade_date": td},
                "trade_date,ts_code,name,close,pct_chg,fd_amount,first_time,last_time,open_times,limit",
            )
        )

    daily_basic = pd.concat(daily_basic_frames, ignore_index=True) if daily_basic_frames else pd.DataFrame()
    daily = pd.concat(daily_frames, ignore_index=True) if daily_frames else pd.DataFrame()
    limit_df = pd.concat(limit_frames, ignore_index=True) if limit_frames else pd.DataFrame()

    unopened_ipo_map = build_open_unopened_ipo_map(limit_df, stock_basic)
    basic_name_map = dict(zip(stock_basic["ts_code"], stock_basic["name"]))
    list_date_map = dict(zip(stock_basic["ts_code"], stock_basic["list_date"]))

    merged = daily_basic.merge(daily, on=["ts_code", "trade_date"], how="left", suffixes=("_basic", "_daily"))
    merged = merged.merge(stock_basic[["ts_code", "market", "list_date"]], on="ts_code", how="left")

    member_rows = []
    daily_counts = []
    for td, day_df in merged.groupby("trade_date"):
        day_df = day_df.copy()
        mv_series = day_df[args.mv_field]
        if isinstance(mv_series, pd.DataFrame):
            mv_series = mv_series.iloc[:, 0]
        day_df = day_df.assign(_market_value=pd.to_numeric(mv_series, errors="coerce"))
        day_df = day_df.dropna(subset=["_market_value"])
        total_candidates = len(day_df)
        excluded_stats = defaultdict(int)
        rows = []
        for _, row in day_df.iterrows():
            ts_code = row["ts_code"]
            base_name = basic_name_map.get(ts_code, ts_code)
            active_name = active_name_for_date(name_changes, ts_code, str(td), base_name)
            include = True
            reasons = []
            excluded, reason = is_excluded_name(active_name)
            if excluded:
                include = False
                reasons.append(reason)
            if list_date_map.get(ts_code) == td:
                include = False
                reasons.append("listing_first_day")
            if str(td) in unopened_ipo_map.get(ts_code, set()):
                include = False
                reasons.append("ipo_unopened_limit_up")
            if reasons:
                for r in reasons:
                    excluded_stats[r] += 1
            rows.append(
                {
                    "trade_date": td,
                    "ts_code": ts_code,
                    "name": active_name,
                    "market": row.get("market"),
                    "list_date": row.get("list_date"),
                    "mv_field": args.mv_field,
                    "market_value": row.get("_market_value"),
                    "close": row.get("close_basic", row.get("close_daily")),
                    "include_pre_rank": include,
                    "exclude_reasons": "|".join(reasons),
                }
            )
        ranked = pd.DataFrame(rows)
        eligible = ranked[ranked["include_pre_rank"]].copy().sort_values("market_value", ascending=True)
        eligible["rank_smallest_mv"] = range(1, len(eligible) + 1)
        selected_codes = set(eligible.head(args.bottom_n)["ts_code"].tolist())
        ranked["selected"] = ranked["ts_code"].isin(selected_codes)
        ranked["weight_eq"] = ranked["selected"].astype(float)
        if ranked["selected"].sum() > 0:
            ranked.loc[ranked["selected"], "weight_eq"] = 1.0 / ranked["selected"].sum()
        member_rows.append(ranked)
        daily_counts.append(
            {
                "trade_date": td,
                "candidate_count": total_candidates,
                "eligible_count": int(ranked["include_pre_rank"].sum()),
                "selected_count": int(ranked["selected"].sum()),
                "excluded_st": excluded_stats.get("st", 0),
                "excluded_delist_arrangement": excluded_stats.get("delist_arrangement", 0),
                "excluded_listing_first_day": excluded_stats.get("listing_first_day", 0),
                "excluded_ipo_unopened_limit_up": excluded_stats.get("ipo_unopened_limit_up", 0),
            }
        )

    members = pd.concat(member_rows, ignore_index=True) if member_rows else pd.DataFrame()
    daily_counts_df = pd.DataFrame(daily_counts)

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_strict_microcap_10y"
    out_dir = OUTPUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    members.to_csv(out_dir / "members.csv", index=False)
    members.to_parquet(out_dir / "members.parquet", index=False)
    daily_counts_df.to_csv(out_dir / "daily_counts.csv", index=False)

    summary = {
        "run_id": run_id,
        "start_date": start_date,
        "end_date": end_date,
        "bottom_n": args.bottom_n,
        "mv_field": args.mv_field,
        "trading_days": len(trade_dates),
        "selected_mean": float(daily_counts_df["selected_count"].mean()) if not daily_counts_df.empty else 0.0,
        "selected_min": int(daily_counts_df["selected_count"].min()) if not daily_counts_df.empty else 0,
        "selected_max": int(daily_counts_df["selected_count"].max()) if not daily_counts_df.empty else 0,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    (out_dir / "config.json").write_text(
        json.dumps(
            {
                "start_date": start_date,
                "end_date": end_date,
                "lookback_years": args.lookback_years,
                "bottom_n": args.bottom_n,
                "mv_field": args.mv_field,
                "rules": [
                    "exclude ST and *ST by active historical name",
                    "exclude delisting-arrangement-like names by active historical name",
                    "exclude listing first day",
                    "exclude IPO consecutive unopened upper-limit phase via limit_list_d open_times == 0",
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    print(out_dir)


if __name__ == "__main__":
    main()
