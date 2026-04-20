import abc
import json
from pathlib import Path
import pandas as pd


class InstProcessor:
    @abc.abstractmethod
    def __call__(self, df: pd.DataFrame, instrument, *args, **kwargs):
        """
        process the data

        NOTE: **The processor could change the content of `df` inplace !!!!! **
        User should keep a copy of data outside

        Parameters
        ----------
        df : pd.DataFrame
            The raw_df of handler or result from previous processor.
        """

    def __str__(self):
        return f"{self.__class__.__name__}:{json.dumps(self.__dict__, sort_keys=True, default=str)}"


class MicrocapUniverseInstProcessor(InstProcessor):
    """Filter each instrument's rows by a precomputed dynamic universe membership file.

    The membership file is expected to contain at least columns:
    - trade_date (YYYYMMDD or parseable date)
    - ts_code
    - selected (bool-like)
    """

    def __init__(self, membership_path: str):
        self.membership_path = membership_path
        self._loaded = False
        self._selected_map = {}

    def _load(self):
        if self._loaded:
            return
        path = Path(self.membership_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Microcap universe membership file not found: {path}")
        if path.suffix.lower() == ".parquet":
            members = pd.read_parquet(path)
        else:
            members = pd.read_csv(path)
        members = members[members["selected"].astype(bool)].copy()
        members["trade_date"] = pd.to_datetime(members["trade_date"].astype(str), format="%Y%m%d", errors="coerce")
        members = members.dropna(subset=["trade_date", "ts_code"])
        self._selected_map = set(zip(members["ts_code"], members["trade_date"]))
        self._loaded = True

    def __call__(self, df: pd.DataFrame, instrument, *args, **kwargs):
        self._load()
        if df is None or df.empty:
            return df
        temp = df.copy()
        temp["__dt__"] = pd.to_datetime(temp.index)
        mask = [(instrument, dt.normalize()) in self._selected_map for dt in temp["__dt__"]]
        temp = temp.loc[mask].drop(columns=["__dt__"])
        return temp
