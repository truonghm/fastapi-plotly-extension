from abc import ABC, abstractmethod
from typing import List, Literal, Optional

import numpy as np
import pandas as pd


class PlotlyChart(ABC):
    @property
    @abstractmethod
    def data_dict(self) -> List[dict]:
        pass

    @property
    @abstractmethod
    def layout_dict(self) -> dict:
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> str:
        pass

    @abstractmethod
    def transform(self) -> List[dict]:
        pass


class Plotly2DChart(PlotlyChart):
    def __init__(
        self,
        data: pd.DataFrame,
        x_name: str,
        y_name: str,
        agg: Optional[Literal["sum", "count", "mean"]] = None,
        group_name: Optional[str] = None,
    ) -> None:
        self.x_name = x_name
        self.y_name = y_name
        self.agg = agg
        self.group_name = group_name
        cols = [x_name, y_name]
        if self.group_name:
            cols.extend([group_name])
        self.data = data[cols]

    def transform(self) -> List[dict]:
        if self.group_name:
            group_data = self.data.groupby([self.x_name, self.group_name])
            if self.agg:
                group_data = group_data.agg({self.y_name: self.agg}).unstack()
            else:
                group_data = self.data.set_index([self.x_name, self.group_name]).unstack()
            group_data.columns = [col[1] for col in group_data.columns.to_flat_index()]
        else:
            group_data = self.data.groupby([self.x_name])
            if self.agg:
                group_data = group_data.agg({self.y_name: self.agg})
            else:
                group_data = self.data.set_index([self.x_name])

        group_data.replace({np.nan: 0}, inplace=True)
        chart_data = []
        for col in group_data:
            trace = {}
            trace["x"] = list(group_data.index)
            trace["y"] = list(group_data[col])
            trace["name"] = col
            chart_data.append(trace)

        return chart_data
