import json
from typing import List, Literal, Optional

import numpy as np
import pandas as pd
from PlotlyChart import PlotlyChart


class PlotlyHist(PlotlyChart):
    def __init__(
        self,
        data: pd.DataFrame,
        var_names: List[str],
        group_name: Optional[str] = None,
        histfunc: Optional[Literal["sum", "count"]] = None,
        barmode: Optional[Literal["overlay", "stack"]] = None,
        horizontal: bool = False,
    ) -> None:
        self.y_names = var_names
        self.barmode = barmode
        self.histfunc = histfunc
        self.horizontal = horizontal
        self.group_name = group_name
        if group_name:
            self.data = data[var_names + [group_name]]
            self.data.set_index(group_name, inplace=True)
        else:
            self.data = data[var_names]
        self.data.replace({np.nan: None}, inplace=True)

    def transform(self) -> List[dict]:
        chart_data = []
        for col in self.data:
            trace = {}
            trace["type"] = "histogram"
            trace["name"] = col
            trace["opacity"] = 0.7
            chart_data.append(trace)

            if self.histfunc:
                trace["histfunc"] = self.histfunc
            else:
                trace["histfunc"] = "count"

            if not self.horizontal:
                trace["x"] = self.data[col].tolist()
                if self.group_name:
                    trace["y"] = self.data.index.tolist()
            else:
                trace["y"] = self.data[col].tolist()
                if self.group_name:
                    trace["x"] = self.data.index.tolist()

        return chart_data

    @property
    def data_dict(self) -> List[dict]:
        chart_data = self.transform()

        return chart_data

    @property
    def layout_dict(self) -> dict:
        title = " vs. ".join(self.y_names)
        if self.histfunc:
            yaxis_title = self.histfunc.capitalize()
        else:
            yaxis_title = "Count"
        return {
            "legend": {"orientation": "h", "y": -0.3},
            "barmode": self.barmode if self.barmode else "overlay",
            "bargap": 0.05,
            "bargroupgap": 0.2,
            "title": {"text": title},
            "xaxis": {"title": "Value"},
            "yaxis": {"title": yaxis_title},
        }

    def to_json(self) -> str:
        return json.dumps({"data": self.data_dict, "layout": self.layout_dict})

    def to_dict(self) -> str:
        return {"data": self.data_dict, "layout": self.layout_dict}
