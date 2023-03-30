import json
from typing import List

from PlotlyChart import Plotly2DChart


class PlotlyBar(Plotly2DChart):
    @property
    def data_dict(self) -> List[dict]:
        chart_data = self.transform()
        for trace in chart_data:
            trace["type"] = "bar"

        return chart_data

    def to_dict(self) -> str:
        return {"data": self.data_dict, "layout": self.layout_dict}

    def to_json(self) -> str:
        return json.dumps({"data": self.data_dict, "layout": self.layout_dict})


class PlotlyStackedBar(PlotlyBar):
    @property
    def layout_dict(self) -> dict:
        return {
            "barmode": "stack",
            "legend": {"orientation": "h", "y": -0.3},
            "title": {"text": f"{self.agg.capitalize()} of {self.y_name} by {self.x_name}"},
            "xaxis": {"title": {"text": self.x_name}},
            "yaxis": {
                "title": {"text": f"{self.agg.capitalize()} of {self.y_name}"},
                "type": "linear",
            },
        }


class PlotlyGroupedBar(PlotlyBar):
    @property
    def layout_dict(self) -> dict:
        return {
            "barmode": "group",
            "legend": {"orientation": "h", "y": -0.3},
            "title": {"text": f"{self.agg.capitalize()} of {self.y_name} by {self.x_name}"},
            "xaxis": {"title": {"text": self.x_name}},
            "yaxis": {
                "title": {"text": f"{self.agg.capitalize()} of {self.y_name}"},
                "type": "linear",
            },
        }
