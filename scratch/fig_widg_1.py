# Scratch code to learn more about figure widgets

import plotly.graph_objs as go
from ipywidgets import Output, VBox
import winpty


fig = go.FigureWidget()
fig.add_pie(values=[1, 2, 3])
pie = fig.data[0]

out = Output()
@out.capture(clear_output=True)
def handle_click(trace, points, state):
    print(points.point_inds)
    print(trace)
    trace.values = [1, 2, 3, 4, 5]

pie.on_click(handle_click)

VBox([fig, out])