"""
From pycharm.

Created by: Tony Held tony.held@gmail.com
Created on: 2020/09/10
Copyright © 2020 Tony Held.  All rights reserved.
"""

import random
from math import ceil

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import networkx as nx
import ipaddress    # for sorting ip addresses
import ipywidgets as widgets
from IPython.display import display

import pprint
pp = pprint.PrettyPrinter(indent=4)     # pretty printer

class NetworkLogPlotter:
    """Class to plot/visualize NetworkLogReader objects"""

    @staticmethod
    def plot_cumulative_errors(sender_fails, receiver_fails):
        """Visualize the network errors as cumulative distribution plot
         to gain intuition on the number of servers participating in failures.

        Parameters
        ----------
        sender_fails : array-like
            # of sending fails per server
        receiver_fails : array-like
            # of receiving fails per server

        Notes
        -------
        1.  It is assumed that the list is sorted in descending order.
        """
        # Create cumulative sum of fails
        sender_fails_total = np.sum(sender_fails)
        sender_fails_cumulative = np.cumsum(sender_fails)
        sender_fails_percent = sender_fails_cumulative / sender_fails_total * 100

        receiver_fails_total = np.sum(receiver_fails)
        receiver_fails_cumulative = np.cumsum(receiver_fails)
        receiver_fails_percent = receiver_fails_cumulative / receiver_fails_total * 100

        # Plot the cumulative fail data via matplotlib
        fig1, ax1 = plt.subplots(1)
        ax1.plot(sender_fails_percent, '-', label=f"Sender Fails")
        ax1.plot(receiver_fails_percent, '-', label=f"Receiver Fails")
        ax1.set_xlabel('Number of Servers')
        ax1.set_ylabel('Percent of Failures')
        ax1.legend()
        ax1.set_title(f"# of Server's Involved in {receiver_fails_total} Total Fails")
        plt.show()

    @staticmethod
    def plot_network1(nx_graph, plot_data):
        """Visualize network with built in networkx and matplotlib routines.

        This can run very slowly!  Use customized plot routines (plot_network3) instead.

        Parameters
        ----------
        nx_graph :
            networkx.graph object
        plot_data : dict
            plot_data object created by NetworkLogReader
        """
        plot_types = [nx.draw, nx.draw_networkx, nx.draw_kamada_kawai, nx.draw_spring]

        # plot using the networkx built-in drawing routines
        fig1, ax1 = plt.subplots(1)
        nx.draw(nx_graph, with_labels=False)

        x = plot_data['Node Coordinates'][0]
        y = plot_data['Node Coordinates'][1]

        # plot using matplotlib using coordinates from layout data
        fig2, ax2 = plt.subplots(1)
        # x = self.node_coordinates[:, 0]
        # y = self.node_coordinates[:, 1]
        ax2.plot(x, y, 'bx')

        plt.show()

    @staticmethod
    def plot_network3(nlr, plot_node, edge_type):
        """Visualize NetworkLogReader object with customized plotly routines.

        Parameters
        ----------
        nlr : NetworkLogReader
            Plot based on plot_data attribute.
        plot_node: str
            The node of interest (the one selected in the figure).
        edge_type : ['Send', 'Receive', 'Send+Receive']
            Type of connection to analyse.

        Returns
        -------
        fig : plotly.graph_objs._figurewidget.FigureWidget
            Figure widget capable of responding to click events

        Notes
        -------
        """
        nlp = NetworkLogPlotter

        # Step 1.  Gather plot input based on nlr, node, edge_type
        # -------------------------------------------------------------
        # Lines that represent the edges between nodes
        shapes = nlr.plot_data[plot_node][edge_type]['shape_data']

        # Node locations
        x_coord = nlr.plot_data['Node Coordinates'][0]
        y_coord = nlr.plot_data['Node Coordinates'][1]

        # Node color and hover text
        node_text = nlr.plot_data[plot_node][edge_type]['node_text']
        node_color = nlr.plot_data[plot_node][edge_type]['node_color']

        # Step 2.  Create trace and figure with edge trace in the layout
        # -------------------------------------------------------------
        node_trace = nlp.create_scatter(edge_type, node_color, node_text, x_coord, y_coord)
        fig = nlp.create_figure(plot_node, node_trace, shapes)
        fig.write_html("network_errors.html")
        return fig

    @staticmethod
    def create_scatter(edge_type, node_color, node_text, x_coord, y_coord):
        """Create plotly scatterplot.

        Parameters
        ----------
        edge_type : ['Send', 'Receive', 'Send+Receive']
            Type of connection to analyse.
        node_color : list of numeric
            A value for each node is created with the same numeric type as the weight in the original
                error log file (likely integer) with length of self.plot_data['Node Names'].
        node_text : list of str
            Text to include as hover text in plotly routines that includes a caption for each node
                with a length of self.plot_data['Node Names'].
        x_coord : [float]
            x coordinates of nodes
        y_coord : [float]
            y coordinates of nodes

        Returns
        -------
        scatter : plotly.graph_objs._scatter.Scatter
            plotly scatter plot
        """
        scatter = go.Scatter(
            x=x_coord, y=y_coord,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                # colorscale options
                # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Reds',
                #                reversescale=True,
                color=node_color,
                size=10,
                colorbar=dict(
                    thickness=15,
                    title=f'Num of Failures<br>{edge_type}',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))
        return scatter

    @staticmethod
    def create_figure(plot_node, node_trace, my_shapes):
        """Create a plotly figure based on node trace and edge shape

        Parameters
        ----------
        plot_node: str
            The node of interest (the one selected in the figure).
        node_trace : plotly.graph_objs._scatter.Scatter
            Scatter plot of node location
        my_shapes : [dict]
            Shape objects suitable for plotly layout inclusion.

        Returns
        -------
        fig : plotly.graph_objs._figurewidget.FigureWidget
            Figure widget capable of responding to click events
        """
        fig = go.FigureWidget(data=[node_trace],
                         layout=go.Layout(
                             title=f'Interactive Graph of Network Failures<br>Selected Node: {plot_node}',
                             titlefont_size=16,
                             showlegend=False,
                             hovermode='closest',
                             margin=dict(b=20, l=5, r=5, t=40),
                             annotations=[dict(
                                 text="<a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'> Click me for more info</a>",
                                 showarrow=False,
                                 xref="paper", yref="paper",
                                 x=0.005, y=-0.002)],
                             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                             shapes=my_shapes)
                         )
        return fig

    @staticmethod
    def update_figure(fig, nlr, plot_node, edge_type):
        """Update network figure based on change in plot_node and/or edge_type.

        Parameters
        ----------
        fig : plotly.graph_objs._figurewidget.FigureWidget
            Original figure created by create_figure(...)
        nlr : NetworkLogReader
            Plot based on plot_data attribute.
        plot_node: str
            The node of interest (the one selected in the figure).
        edge_type : ['Send', 'Receive', 'Send+Receive']
            Type of connection to analyse.
        """

        # Lines that represent the edges between nodes
        my_shapes = nlr.plot_data[plot_node][edge_type]['shape_data']

        # Node color and hover text
        node_text = nlr.plot_data[plot_node][edge_type]['node_text']
        node_color = nlr.plot_data[plot_node][edge_type]['node_color']

        # update scatter trace
        scatter = fig.data[0]
        scatter.text = node_text
        scatter.marker.color = node_color
        scatter.marker.colorbar.title = f'Num of Failures<br>{edge_type}'

        # update figure layout
        fig.layout.title = f'Interactive Graph of Network Failures<br>Selected Node: {plot_node}'
        fig.layout.shapes = my_shapes


