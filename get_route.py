import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

import matplotlib.pyplot as plt
import plotly_express as px

import networkx as nx
import osmnx as ox

class GetRoute:
    """Класс для расчета маршрутов"""  
    longitude = 0.0
    latitude = 0.0
    dataJson = {}
  
    def __init__(self,):  
       

        ox.config(use_cache=True, log_console=True)

        def create_graph(loc, dist, transport_mode, loc_type="address"):
            """Transport mode = ‘walk’, ‘bike’, ‘drive’, ‘drive_service’, ‘all’, ‘all_private’, ‘none’"""
            if loc_type == "address":
                 self.G = ox.graph_from_address(loc, dist=dist, network_type=transport_mode)
            elif loc_type == "points":
                 self.G = ox.graph_from_point(loc, dist=dist, network_type=transport_mode )
            return  self.G

            # G = create_graph("Gothenburg", 2500, "drive", fig_width=12, fig_height=12)
        G = create_graph("Gothenburg", 2500, "drive")
        # Отрисовка путей маршрута
        #ox.plot_graph(G)

        # impute missing edge speeds and add travel times
        G = ox.add_edge_speeds( self.G)
        G = ox.add_edge_travel_times( self.G)

    def getRoteData(self, longitude, latitude):  
        GetRoute.longitude = longitude  
        GetRoute.latitude = latitude

        # start = (57.715495, 12.004210)
        start = (longitude, latitude) 
        end = (57.707166, 11.978388)
        start_node = ox.get_nearest_node( self.G, start) 
        end_node = ox.get_nearest_node( self.G, end)
        route = nx.shortest_path( self.G, start_node, end_node, weight='travel_time')

        # ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k',fig_width=12, fig_height=12 );
        # Отрисовка маршурта на карте (отображения фото)
        # ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k' );

        #see the travel time for the whole route
        travel_time = nx.shortest_path_length( self.G, start_node, end_node, weight='travel_time')
        print(round(travel_time))

        node_start = []
        node_end = []
        X_to = []
        Y_to = []
        X_from = []
        Y_from = []
        length = []
        travel_time = []

        for u, v in zip(route[:-1], route[1:]):
            node_start.append(u)
            node_end.append(v)
            length.append(round( self.G.edges[(u, v, 0)]['length']))
            travel_time.append(round( self.G.edges[(u, v, 0)]['travel_time']))
            X_from.append( self.G.nodes[u]['x'])
            Y_from.append( self.G.nodes[u]['y'])
            X_to.append( self.G.nodes[v]['x'])
            Y_to.append( self.G.nodes[v]['y'])

        df = pd.DataFrame(list(zip(node_start, node_end, X_from, Y_from,  X_to, Y_to, length, travel_time)), 
                    columns =["node_start", "node_end", "X_from", "Y_from",  "X_to", "Y_to", "length", "travel_time"]) 
        df.head()

        df.reset_index(inplace=True)
        df.head()

        GetRoute.dataJson = df.head().to_json(orient="index")

        print(GetRoute.dataJson)