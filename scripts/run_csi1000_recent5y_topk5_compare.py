from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPARE_ROOT = ROOT / "examples" / "benchmarks" / "comparison_runs"
RUN_ID = datetime.now().strftime("%Y%m%d_%H%M%S") + "_csi1000_recent5y_topk5"
RUN_DIR = COMPARE_ROOT / RUN_ID
RUN_DIR.mkdir(parents=True, exist_ok=True)

ENV = os.environ.copy()
ENV.update(
    {
        "LDFLAGS": "-L/usr/local/opt/libomp/lib",
        "CPPFLAGS": "-I/usr/local/opt/libomp/include",
        "DYLD_LIBRARY_PATH": "/usr/local/opt/libomp/lib",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
    }
)

RUNS = {
    "linear": "examples/benchmarks/Linear/workflow_config_linear_Alpha158_csi1000_recent5y_topk5.yaml",
    "lightgbm": "examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158_csi1000_recent5y_topk5.yaml",
}

METRIC_PATTERNS = {
    "IC": r"'IC': np\.float64\(([-0-9.eE]+)\)",
    "ICIR": r"'ICIR': np\.float64\(([-0-9.eE]+)\)",
    "Rank IC": r"'Rank IC': np\.float64\(([-0-9.eE]+)\)",
    "Rank ICIR": r"'Rank ICIR': np\.float64\(([-0-9.eE]+)\)",
    "annualized_return": r"annualized_return\s+([-0-9.]+)",
    "information_ratio": r"information_ratio\s+([-0-9.]+)",
    "max_drawdown": r"max_drawdown\s+([-0-9.]+)",
}


def extract_cost_metrics(text: str) -> dict[str, str | None]:
    cost_anchor = "The following are analysis results of the excess return with cost(1day)."
    idx = text.find(cost_anchor)
    block = text[idx:] if idx >= 0 else text
    result: dict[str, str | None] = {}
    for key in ["annualized_return", "information_ratio", "max_drawdown"]:
        match = re.search(METRIC_PATTERNS[key], block)
        result[key] = match.group(1) if match else None
    return result


def extract_signal_metrics(text: str) -> dict[str, str | None]:
    result: dict[str, str | None] = {}
    for key in ["IC", "ICIR", "Rank IC", "Rank ICIR"]:
        match = re.search(METRIC_PATTERNS[key], text)
        result[key] = match.group(1) if match else None
    return result


def run_one(name: str, config_rel: str) -> dict:
    log_path = RUN_DIR / f"{name}_stdout.log"
    cmd = ["python", "qlib/cli/run.py", config_rel]
    proc = subprocess.run(cmd, cwd=ROOT, env=ENV, text=True, capture_output=True)
    full_text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    log_path.write_text(full_text)
    metrics = {}
    metrics.update(extract_signal_metrics(full_text))
    metrics.update(extract_cost_metrics(full_text))
    return {
        "name": name,
        "config": config_rel,
        "exit_code": proc.returncode,
        "log": str(log_path.relative_to(ROOT)),
        "metrics": metrics,
    }


results = [run_one(name, cfg) for name, cfg in RUNS.items()]

summary = {
    "run_id": RUN_ID,
    "generated_at": datetime.now().isoformat(timespec="seconds"),
    "results": results,
}

(RUN_DIR / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2))

lines = [
    f"# CSI1000 recent5y topk=5 comparison\n",
    f"Run dir: `{RUN_DIR.relative_to(ROOT)}`\n",
    "| Model | Exit | IC | ICIR | Rank IC | Rank ICIR | annualized_return(cost) | information_ratio(cost) | max_drawdown(cost) | Log |",
    "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
]
for item in results:
    m = item["metrics"]
    lines.append(
        f"| {item['name']} | {item['exit_code']} | {m['IC']} | {m['ICIR']} | {m['Rank IC']} | {m['Rank ICIR']} | {m['annualized_return']} | {m['information_ratio']} | {m['max_drawdown']} | `{item['log']}` |"
    )

(RUN_DIR / "summary.md").write_text("\n".join(lines) + "\n")
print(str(RUN_DIR))
