"""
Routines to interactively visualize network server error log files
to graphically determine which servers tend to fail and to potentially
relations between failing connections.

Created by: Tony Held tony.held@gmail.com
Created on: 2020/09/10
Copyright © 2020 Tony Held.  All rights reserved.
"""

import ipywidgets as widgets
from IPython.display import display

from network_log_reader_v02 import NetworkLogReader
from network_log_plotter_v02 import NetworkLogPlotter

if __name__ == "__main__":

    # Select log file and initialize reader/plotter
    # ---------------------------------------------
    error_log_file = "data_log_files/weight_node_node2.txt"
    nlr = NetworkLogReader(error_log_file)
    nlp = NetworkLogPlotter()

    # Select your IDE type.
    # ----------------------
    # Note that only jupyter fully supports the widget plots used in this analysis
    python_environment = 'Pycharm'
    # python_environment = 'jupyter'

    # Select the edge_type and node for the initial plot rendering
    # ------------------------------------------------------------
    # edge_types can be ['Send', 'Receive', 'Send+Receive']
    edge_type = 'Send+Receive'
    # a good starting plot_node is likely
    # nlr.receiver_fails_name[0] or nlr.sender_fails_name[1]
    plot_node = nlr.receiver_fails_name[0]

    print(f'Your selected python environment is: {python_environment}')
    print(f'{edge_type=} and {plot_node=}')

    # Create cumulative error figure
    if True:
        nlp.plot_cumulative_errors(nlr.sender_fails_count, nlr.receiver_fails_count)

    # plot_network1 uses slow stock routines and you should use plot_network3 instead
    if False:
        nlp.plot_network1(nlr.send_graph, nlr.plot_data)

    # plot_network3 is the primary plot of interest to show failure relations.
    fig01 = nlp.plot_network3(nlr, plot_node, edge_type)

    # todo - resume refactor here

    # Figure widget interactive ability is only available in jupyter environment
    # if the environment is Pycharm, then only a static html file will be created.
    if python_environment == 'Pycharm':
        fig01.show()    # Use .show() when in pycharm
    elif python_environment == 'jupyter':

        # Create interactive widgets/callback to create interactive network figure

        # data to display in widgets
        node_names = list(nlr.unique_nodes)
        num_nodes = len(node_names)
        edge_types = ['Send', 'Receive', 'Send+Receive']


        # Figure widgets, create them with a dummy state and then
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
