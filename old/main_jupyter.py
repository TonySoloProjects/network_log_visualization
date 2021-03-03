import random
from math import ceil

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
import ipaddress  # for sorting ip addresses
import ipywidgets as widgets
from IPython.display import display

import pprint
pp = pprint.PrettyPrinter(indent=4)  # pretty printer

from network_log_reader_v02 import NetworkLogReader
from network_log_plotter_v02 import NetworkLogPlotter



if __name__ == "__main__":
    # Select your python environment
    # Only jupyter fully supports the widget plots used in this analysis
    python_environment = 'Pycharm'
    # python_environment = 'jupyter'

    # Read in Error Log file and inspect contents
    # This is the same file Ryan sent with a one line header
    file_name = "../data_log_files/weight_node_node2.txt"
    nlr = NetworkLogReader(file_name)
    nlp = NetworkLogPlotter()

    # Set to True if you want to create the original plot figure formats
    if False:
        # Create cumulative error figure
        nlp.plot_cumulative_errors(nlr.sender_fails_count, nlr.receiver_fails_count)
        nlp.plot_network1(nlr.send_graph, nlr.plot_data)

    # Create the network visualization based on
    #   the plot node and the desired edge connection type
    plot_node = nlr.receiver_fails_name[0]
    # plot_node = nlr.sender_fails_name[1]
    # edge_types = ['Send', 'Receive', 'Send+Receive']
    edge_type = 'Send+Receive'
    fig01 = nlp.plot_network3(nlr, plot_node, edge_type)

    # Pycharm: display the figure as a html file
    # jupyter: dislay as an interactive widget
    if python_environment == 'Pycharm':
        fig01.show()    # Use .show() when in pycharm
    elif python_environment == 'jupyter':

        # Create interactive wigets/callback to create interactive network figure

        # data to display in widgets
        node_names = list(nlr.unique_nodes)
        num_nodes = len(node_names)
        edge_types = ['Send', 'Receive', 'Send+Receive']

        # Figure wigets, create them with a dummy state and then
        # change the value to invoke the event handler before first use
        slider = widgets.IntSlider(
            min=0,
            max=num_nodes - 1,
            value=1,
            description='Node #: ')

        slider_label = widgets.Label(value="Node Name: ")

        node_hb = widgets.HBox([slider, slider_label])

        drop = widgets.Dropdown(
            options=edge_types,
            value=edge_types[1],
            description='Errors: ',
            disabled=False, )

        drop_label = widgets.Label(value="Error Type: ")

        drop_hb = widgets.HBox([drop, drop_label])


        # widget handlers
        def on_slider_value_change(change):
            new_node_number = change['new']
            new_node_name = node_names[new_node_number]
            slider_label.value = f'Node Name: {new_node_name}'
            nlp.update_figure(fig01, nlr, plot_node=new_node_name, edge_type=drop.value)


        def on_drop_value_change(change):
            new_edge_type = change['new']
            drop_label.value = f'Error Type:  {new_edge_type}'
            node_name = node_names[slider.value]
            nlp.update_figure(fig01, nlr, plot_node=node_name, edge_type=new_edge_type)


        slider.observe(on_slider_value_change, names='value')
        drop.observe(on_drop_value_change, names='value')

        # Initialize (changing from the instantiated value will invoke the handlers)
        slider.value = 0
        drop.value = edge_types[2]


        # Callback for clicking on the scatterplot
        # Changes the slider widget which will update the figure and synch with the slider
        def update_point(trace, points, selector):
            node_id = points.point_inds[0]
            slider.value = node_id

        scatter = fig01.data[0]
        scatter.on_click(update_point)

        # display widgets and interactive figure
        display(node_hb)
        display(drop)
        display(fig01)  # Use display when in jupyter
