from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/members.parquet"
OUT = ROOT / "examples/universe/a_share_microcap_10y/outputs/20260421_103028_strict_microcap_10y/microcap_strict_recent.txt"


def to_qlib_code(ts_code: str) -> str:
    ts_code = str(ts_code)
    raw = ts_code.replace(".SZ", "").replace(".SH", "").replace(".BJ", "")
    if ts_code.endswith(".SZ"):
        return f"SZ{raw}"
    if ts_code.endswith(".SH"):
        return f"SH{raw}"
    if ts_code.endswith(".BJ"):
        return f"BJ{raw}"
    return ts_code


def main() -> None:
    df = pd.read_parquet(SRC)
    df = df[df["selected"] == True].copy()
    df["trade_date"] = pd.to_datetime(df["trade_date"].astype(str), format="%Y%m%d")
    df["instrument"] = df["ts_code"].map(to_qlib_code)
    df = df.sort_values(["instrument", "trade_date"])

    rows = []
    for inst, g in df.groupby("instrument"):
        dates = list(g["trade_date"])
        if not dates:
            continue
        start = dates[0]
        prev = dates[0]
        for dt in dates[1:]:
            if (dt - prev).days <= 4:
                prev = dt
                continue
            rows.append((inst, start.strftime("%Y-%m-%d"), prev.strftime("%Y-%m-%d")))
            start = dt
            prev = dt
        rows.append((inst, start.strftime("%Y-%m-%d"), prev.strftime("%Y-%m-%d")))

    OUT.write_text("\n".join("\t".join(r) for r in rows) + "\n")
    print(json.dumps({
        "source": str(SRC),
        "output": str(OUT),
        "instrument_count": int(df["instrument"].nunique()),
        "interval_count": len(rows),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
