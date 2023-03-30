import json
from typing import List

from PlotlyChart import Plotly2DChart


class PlotlyScatter(Plotly2DChart):
    @property
    def data_dict(self) -> List[dict]:
        chart_data = self.transform()
        for trace in chart_data:
            trace["type"] = "scatter"
            trace["mode"] = "markers"

        return chart_data

    @property
    def layout_dict(self) -> dict:
        return {
            "legend": {"orientation": "h", "y": -0.3},
            "title": {"text": f"{self.agg.capitalize()} of {self.y_name} by {self.x_name}"},
            "xaxis": {
                # "tickformat": "0:g",
                "title": {"text": self.x_name}
            },
            "yaxis": {
                "title": {"text": f"{self.agg.capitalize()} of {self.y_name}"},
                "type": "linear",
            },
        }

    def to_json(self):
        return json.dumps({"data": self.data_dict, "layout": self.layout_dict})

    def to_dict(self) -> str:
        return {"data": self.data_dict, "layout": self.layout_dict}
