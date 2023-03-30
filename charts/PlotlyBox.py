import json
from typing import List, Literal, Optional

import numpy as np
import pandas as pd
from PlotlyChart import PlotlyChart


class PlotlyBox(PlotlyChart):
    def __init__(
        self,
        data: pd.DataFrame,
        var_names: List[str],
        group_name: Optional[str] = None,
        display_data: bool = False,
        horizontal: bool = False,
    ) -> None:
        self.y_names = var_names
        self.display_data = display_data
        self.horizontal = horizontal
        if group_name:
            self.data = data[var_names + [group_name]]
            self.data.set_index(group_name, inplace=True)
        else:
            self.data = data[var_names]
        self.data.replace({np.nan: None}, inplace=True)
        self.group_name = group_name

    def transform(self) -> List[dict]:
        chart_data = []
        for col in self.data:
            trace = {}
            trace["type"] = "box"
            trace["name"] = col
            chart_data.append(trace)

            if self.display_data:
                trace["boxpoints"] = "all"
                trace["jitter"] = 0.3
                trace["pointpos"] = -1.8

            if self.horizontal:
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
        return {
            "legend": {"orientation": "h", "y": -0.3},
            "title": {"text": title},
            "xaxis": {"anchor": "y", "domain": [0.0, 1.0]},
            "yaxis": {
                "anchor": "x",
                "domain": [0.0, 1.0],
            },
            "margin": {"t": 60},
            "boxmode": "group",
        }

    def to_json(self) -> str:
        return json.dumps({"data": self.data_dict, "layout": self.layout_dict})

    def to_dict(self) -> str:
        return {"data": self.data_dict, "layout": self.layout_dict}
