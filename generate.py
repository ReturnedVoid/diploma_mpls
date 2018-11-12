import numpy as np
import csv
import random
from diploma_mpls.graph import GraphUtil


gutil = GraphUtil()
unique_routes = gutil.unique_routes
unique_routes_cnt = gutil.unique_routes_cnt
mpls_graph = gutil.graph

ethernet_max_packet_size = 1518 + 12 + 8
ethernet_max_throughput = 125e5  # 100 MB/s
ethernet_min_throughput = 1e2  # 100 bytes/s


def generate_example_inputs(g):
    gutil.clear_edges_load()
    while True:
        koefs = []
        ran = random.randint(0, 5)
        for edge in gutil.nodes_to_edges(gutil.tunnels_routes[ran]):
            i, j = edge
            g[i][j]['K'] += 0.1

        for ure in gutil.unique_routes_edges:
            route_load = []
            for edge in ure:
                i, j = edge
                inten = np.random.uniform(
                    ethernet_min_throughput, ethernet_max_throughput // 15)
                k_load = inten / ethernet_max_throughput
                route_load.append(k_load)
                g[i][j]['intensity'] += inten
                g[i][j]['K'] += k_load
            koefs.append(sum(route_load))
        k = max(koefs)

        if k >= 0.65:
            gutil.clear_edges_load()
            continue

        k_load = []

        k_load.append(np.random.choice(['EF', 'BE', 'AF']))

        for edge in gutil.unique_edges_set:
            i, j = edge
            k_load.append(round(g[i][j]['K'], 3))
        break

    return k_load


def generate_example_output(input):
    if input[0] == 0:
        d = []
        for u in gutil.routes_with_index:
            d.append((u[0], gutil.get_route_load(u[1])))
        return min(d, key=lambda x: x[1])[0]
    else:
        tuns = [t for t in gutil.tunnels if t.qos == input[0]]
        d = [(t, gutil.get_route_load(t.route)) for t in tuns]
        best_tunnel = min(d, key=lambda x: x[1])[0]
        return best_tunnel.index


def generate_example():
    x = generate_example_inputs(mpls_graph)
    y = generate_example_output(x)
    return (x, y)


def generate_dataset(m, filename):
    cnt = [0] * unique_routes_cnt
    examples_per_route = m // unique_routes_cnt
    print('Generating {} examples per route'.format(examples_per_route))
    new_datas = []
    new_labels = []
    i = 0

    while True:
        new_data, new_label = generate_example()

        if cnt[new_label] < examples_per_route:
            new_datas.append(new_data)
            new_labels.append(new_label)
            cnt[new_label] += 1

        if len(new_datas) >= examples_per_route * unique_routes_cnt:
            break

        i += 1
        if i % 1000 == 0:
            print(cnt, '{}%'.format(int(np.floor(len(new_datas) / m * 100))))

    m = examples_per_route * unique_routes_cnt
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in range(m - 1):
            k = []
            k.append(new_labels[i])
            example = new_datas[i] + k
            writer.writerow(example)


generate_dataset(100, 'dataset2.csv')

with open('valid_routes.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for r in range(unique_routes_cnt):
        k = []
        k.append(r)
        writer.writerow(k)
