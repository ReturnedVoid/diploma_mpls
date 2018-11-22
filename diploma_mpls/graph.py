import networkx as nx
from collections import namedtuple
import matplotlib.pyplot as plt
import itertools


class GraphUtil:
    SOURCE = 'ДЗ'
    TARGET = 'Дніпро'

    def __init__(self):
        self.graph = nx.Graph()
        self.__init_destination()
        self.__init_edges()
        self.__init_tunnels()
        self.clear_edges_load()

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
        route = []
        forward, backward = self.destinations

        for i in range(self.tunnels_cnt):
            temp = []
            if (self.source, self.target) in forward:
                to = self.routes(self.source, 'Дніпро')
                if not to:
                    to.append(self.source)
                else:
                    to = to[0]
                temp.append(list(itertools.chain(
                    to, self.tunnels[i].route[1:])))

                if self.target != self.tunnels[i].route[-1]:
                    temp[0].append(self.target)

            else:
                to = self.routes(self.source, 'Павлоград')
                if not to:
                    to.append(self.source)
                else:
                    to = to[0]
                temp.append(list(itertools.chain(
                    to, self.tunnels[i].invroute[1:])))

                if self.target != self.tunnels[i].invroute[-1]:
                    temp[0].append(self.target)

            route.append(temp[0])
            temp.clear()
        return route

    def routes(self, s, t):
        unique_routes = list(nx.all_simple_paths(
            self.graph, source=s, target=t))
        unique_routes.sort(key=len)
        return unique_routes

    @property
    def unique_routes_cnt(self):
        return len(self.unique_routes)

    @property
    def unique_routes_edges(self):
        return [self.nodes_to_edges(route) for route in self.unique_routes]

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

    @property
    def destinations(self):
        forward = [
            ('ДЗ', 'Павлоград'),
            ('ДЗ', 'Мик-вка'),
            ('П-тки', 'Павлоград'),
            ('П-тки', 'Мик-вка'),
            ('КР', 'Павлоград'),
            ('КР', 'Мик-вка'),
            ('Дніпро', 'Павлоград'),
            ('Дніпро', 'Мик-вка'),
        ]
        backward = [(dest[1], dest[0]) for dest in forward]
        return forward, backward

    def nodes_to_edges(self, node_route):
        edges = []
        y = node_route[0]
        for i in range(1, len(node_route)):
            x = y
            y = node_route[i]
            edge = (x, y)
            edges.append(edge)
        return edges

    def get_route_load(self, path):
        edge_path = self.nodes_to_edges(path)
        load_koefs = []
        for i, u in edge_path:
            load_koefs.append(self.graph[i][u]['K'])
        return sum(load_koefs)

    def __init_edges(self):
        self.graph.add_nodes_from(list(range(1, 4)))
        self.graph.add_node('КР')
        self.graph.add_node('П-тки')
        self.graph.add_node('ДЗ')
        self.graph.add_node('Мик-вка')
        self.graph.add_node('Дніпро')
        self.graph.add_node('НДВ')
        self.graph.add_node('Павлоград')
        self.graph.add_node('Ново-ївка')
        self.graph.add_node('Синель-во')
        self.graph.add_node('ЗП')
        self.graph.add_node('Славгород')

        edges = [
            ('КР', 'П-тки'),
            # ('КР', 5),
            ('КР', 'Дніпро'),
            ('П-тки', 1),
            ('П-тки', 'Дніпро'),
            (1, 'ДЗ'),
            ('ДЗ', 2),
            (2, 'Дніпро'),
            ('Дніпро', 'НДВ'),
            ('Дніпро', 'Ново-ївка'),
            ('Дніпро', 'ЗП'),
            ('Дніпро', 'Синель-во'),
            ('Ново-ївка', 4),
            (4, 'Павлоград'),
            ('Павлоград', 3),
            (3, 'Мик-вка'),
            # ('Павлоград', 6),
            # (6, 5),
            ('ЗП', 'Синель-во'),
            ('Синель-во', 'Павлоград'),
            ('Синель-во', 'НДВ'),
            ('ЗП', 'Славгород'),
            ('Славгород', 'Синель-во')
        ]
        for start, end in edges:
            self.graph.add_edge(start, end)

    def __init_tunnels(self):
        Tunnel = namedtuple('MPLSTunnel', 'index, qos, route invroute')
        s = 'Дніпро'
        t = 'Павлоград'
        self.tunnel1 = Tunnel(
            0, 'CS0', self.routes(s, t)[0], self.routes(s, t)[0][:: -1])
        self.tunnel2 = Tunnel(
            1, 'CS0', self.routes(s, t)[1], self.routes(s, t)[1][:: -1])
        self.tunnel3 = Tunnel(
            2, 'CS1', self.routes(s, t)[2], self.routes(s, t)[2][:: -1])
        self.tunnel4 = Tunnel(
            3, 'CS1', self.routes(s, t)[3], self.routes(s, t)[3][:: -1])
        self.tunnel5 = Tunnel(
            4, 'CS2', self.routes(s, t)[4], self.routes(s, t)[4][:: -1])

    def __init_destination(self):
        self.source = self.SOURCE
        self.target = self.TARGET

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
