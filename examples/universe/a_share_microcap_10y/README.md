# A-share microcap universe (strict Tushare-backed version)

This directory builds a daily-updated A-share microcap universe for the last 10 years using Tushare data.

## Target definition

Daily components are selected as:

- A-shares only
- bottom 400 by market cap (`total_mv` by default)
- equal-weight conceptual construction
- exclusions:
  - ST / *ST
  - delisting arrangement / delisting-related names
  - listing first day
  - IPO consecutive limit-up unopened names

## Current implementation notes

This implementation uses Tushare as the authoritative source for:

- stock list and listing date
- daily market value (`daily_basic.total_mv`, `circ_mv`)
- historical name changes (`namechange`)
- daily limit-up information (`limit_list_d`)
- IPO schedule (`new_share`)
- trading calendar (`trade_cal`)

## Output

Each run writes into `outputs/<run_id>/`:

- `members.parquet` / `members.csv`
- `daily_counts.csv`
- `summary.json`
- `config.json`

## Rule notes

### ST / *ST
Historical ST status is approximated from `namechange` records by checking whether the active name on a date contains `ST` or `*ST`.

### Delisting arrangement
Approximated from active names containing delisting-related markers such as `退` or `退市`.

### Listing first day
Excluded by comparing `trade_date == list_date`.

### IPO consecutive limit-up unopened names
Approximated using `limit_list_d` and `open_times == 0` on upper-limit days after IPO. If a stock is still in its unopened consecutive upper-limit phase, it is excluded.

## Caveat

This is a research universe builder. The universe definition is much stricter and more faithful than the public qlib-only proxy approach, but it still depends on the quality and semantics of Tushare historical name/status data.
