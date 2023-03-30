import json
from typing import List

from PlotlyChart import Plotly2DChart


class PlotlyLine(Plotly2DChart):
    @property
    def data_dict(self) -> List[dict]:
        chart_data = self.transform()
        for trace in chart_data:
            trace["type"] = "scatter"
            trace["mode"] = "lines+markers"
            trace["line"] = {"shape": "spline", "smoothing": 0.3}

        return chart_data

    @property
    def layout_dict(self) -> dict:
        if self.agg is not None:
            title = f"{self.agg.capitalize()} of {self.y_name} by {self.x_name}"
            ytitle = f"{self.agg.capitalize()} of {self.y_name}"
        else:
            title = f"{self.y_name} by {self.x_name}"
            ytitle = f"{self.y_name}"
        return {
            "legend": {"orientation": "h", "y": -0.3},
            "title": {"text": title},
            "xaxis": {
                # "tickformat": "0:g",
                "title": {"text": self.x_name}
            },
            "yaxis": {
                "title": {"text": ytitle},
                "type": "linear",
            },
        }

    def to_json(self) -> str:
        return json.dumps({"data": self.data_dict, "layout": self.layout_dict})

    def to_dict(self) -> str:
        return {"data": self.data_dict, "layout": self.layout_dict}
