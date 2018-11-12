import networkx as nx
from collections import namedtuple
import matplotlib.pyplot as plt


class GraphUtil:
    SOURCE = 12
    TARGET = 1

    def __init__(self):
        self.graph = nx.Graph()
        self.__init_edges()
        self.__init_tunnels()
        self.clear_edges_load()
        self.show_graph()

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value):
        self._graph = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def unique_routes(self):
        unique_routes = list(nx.all_simple_paths(
            self.graph, source=self.SOURCE, target=self.TARGET))
        unique_routes.sort(key=len)
        return unique_routes

    @property
    def unique_routes_cnt(self):
        return len(self.unique_routes)

    @property
    def unique_routes_edges(self):
        return [self._nodes_to_edges(route) for route in self.unique_routes]

    @property
    def tunnels(self):
        tunnels = []
        tunnels.append(self.tunnel1)
        tunnels.append(self.tunnel2)
        tunnels.append(self.tunnel3)
        tunnels.append(self.tunnel4)
        tunnels.append(self.tunnel5)
        return tunnels

    @property
    def tunnels_cnt(self):
        return len(self.tunnels)

    @property
    def tunnels_routes(self):
        return [t.route for t in self.tunnels]

    @property
    def routes_with_index(self):
        i = self.tunnels_cnt
        rwi = []
        for u in self.unique_routes:
            if u in self.tunnels_routes:
                continue
            else:
                rwi.append((i, u))
                i += 1
        return rwi

    @property
    def unique_edges_set(self):
        u = []
        for ure in self.unique_routes_edges:
            for edge in ure:
                if edge not in u:
                    u.append(edge)
        return u

    def _nodes_to_edges(self, node_route):
        edges = []
        y = node_route[0]
        for i in range(1, len(node_route)):
            x = y
            y = node_route[i]
            edge = (x, y)
            edges.append(edge)
        return edges

    def get_route_load(self, path):
        edge_path = self._nodes_to_edges(path)
        load_koefs = []
        for i, u in edge_path:
            load_koefs.append(self.graph[i][u]['K'])
        return sum(load_koefs)

    def __init_edges(self):
        self.graph.add_nodes_from(list(range(16)))
        self.graph.add_node('КР')
        self.graph.add_node('П-тки')
        self.graph.add_node('ДЗ')
        self.graph.add_node('Сл-ке')
        self.graph.add_node('Дніпро')
        self.graph.add_node('НДВ')
        self.graph.add_node('Павлоград')
        self.graph.add_node('Ново-ївка')
        self.graph.add_node('Синель-во')
        self.graph.add_node('ЗП')

        edges = [
            (0, 'КР', 1),
            (1, 'КР', 1),
            (2, 'КР', 2),
            (1, 'П-тки', 1),
            (3, 'П-тки', 2),
            (4, 'Дніпро', 2),
            (6, 'Дніпро', 1),
            (8, 'Дніпро', 3),
            (7, 'Дніпро', 1),
            (10, 'Дніпро', 2),
            (11, 'Дніпро', 2),
            (15, 'Дніпро', 3),
            (6, 'ДЗ', 1),
            (5, 'ДЗ', 1),
            (5, 'Сл-ке', 1),
            (7, 'Сл-ке', 1),
            (15, 'НДВ', 3),
            (15, 'ЗП', 1),
            (14, 'ЗП', 1),
            (11, 'Синель-во', 1),
            (12, 'Синель-во', 2),
            (14, 'Синель-во', 1),
            (9, 'Ново-ївка', 1),
            (10, 'Ново-ївка', 1),
            (8, 'Павлоград', 1),
            (9, 'Павлоград', 1),
            (12, 'Павлоград', 1),
            (13, 'Павлоград', 5),
            (3, 4, 2),
            (2, 4, 2),
            (0, 13, 10),
        ]
        for start, end, length in edges:
            self.graph.add_edge(start, end, length=length)

    def __init_tunnels(self):
        Tunnel = namedtuple('MPLSTunnel', 'index, qos, route')
        self.tunnel1 = Tunnel(0, 1, self.unique_routes[4])
        self.tunnel2 = Tunnel(1, 2, self.unique_routes[1])
        self.tunnel3 = Tunnel(2, 1, self.unique_routes[2])
        self.tunnel4 = Tunnel(3, 3, self.unique_routes[7])
        self.tunnel5 = Tunnel(4, 4, self.unique_routes[3])

    def clear_edges_load(self):
        for edge in self.graph.edges():
            i, j = edge
            self.graph[i][j]['K'] = 0
            self.graph[i][j]['intensity'] = 0

    def show_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos, node_size=300)

        nx.draw_networkx_edges(self.graph, pos,
                               width=1,
                               alpha=0.6, edge_color='b', style='solid')

        # labels
        nx.draw_networkx_labels(
            self.graph, pos, font_size=14, font_family='sans-serif')

        plt.axis('off')
        plt.savefig("Graph.png", format="PNG")
        plt.show()
