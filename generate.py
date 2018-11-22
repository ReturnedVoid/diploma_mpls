import csv
import random
from diploma_mpls.graph import GraphUtil


gutil = GraphUtil()
unique_routes = gutil.unique_routes
unique_routes_cnt = gutil.unique_routes_cnt
mpls_graph = gutil.graph


def generate_example_inputs(g):
        k_load = []

        k_load.append(np.random.choice(['CS0', 'CS1', 'CS2']))
        k_load.append(gutil.source)
        k_load.append(gutil.target)

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
    for source, dest in gutil.destinations:
        gutil.source = source
        gutil.target = dest
        # maybe i need to get cnt for every destination
        # unique_routes_cnt = gutil.unique_routes_cnt
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
            if i % 10000 == 0:
                perc = int(np.floor(len(new_datas) / m * 100))
                print(cnt, '{}%'.format(perc))

        m = examples_per_route * unique_routes_cnt
        with open(filename, 'a', newline='') as f:
            writer = csv.writer(f)
            for i in range(m):
                k = []
                k.append(new_labels[i])
                example = new_datas[i] + k
                writer.writerow(example)


generate_dataset(2400, 'dataset2.csv')
