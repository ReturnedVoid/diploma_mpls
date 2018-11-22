import csv
from diploma_mpls.graph import GraphUtil
import numpy as np
import sys


gutil = GraphUtil()
unique_routes = gutil.unique_routes
unique_routes_cnt = gutil.unique_routes_cnt
mpls_graph = gutil.graph
ethernet_max_throughput = 125e5  # 100 MB/s


def generate_example_inputs(g, util):

    sample = []
    sample.append(np.random.choice(['CS0', 'CS1', 'CS2']))
    sample.append(gutil.source)
    sample.append(gutil.target)

    threads = [round(np.random.uniform(1, 15), 2) for _ in range(15)]
    for k in gutil.tunnels_load:
        sample.append(k)
    for thread in threads:
        sample.append(thread)

    return sample


def generate_example_output(input):
    coses = ['CS0', 'CS1', 'CS2']

    threads = input[8:]
    cnt = [0] * len(threads)

    tuns = [t for t in gutil.tunnels if t.qos == input[0]]
    for i in range(len(threads)):
        d = [(t, gutil.tunnels_load[t.index]) for t in tuns]
        print(gutil.tunnels_load)
        best_tunnel = min(d, key=lambda x: x[1])[0]
        # best_tunnel = 
        if gutil.add_load(best_tunnel.index, threads[i] / 100).load >= 0.65:
            index = coses.index(best_tunnel.qos)
            if index - 1 != -1:
                index -= 1

            tuns = [t for t in gutil.tunnels if t.qos == coses[index]]
            d = [(t, gutil.tunnels_load[t.index]) for t in tuns]
            best_tunnel = min(d, key=lambda x: x[1])[0]
        cnt[i] = best_tunnel.index
    print(cnt)
    sys.exit()

    return best_tunnel.index


def generate_example(util):
    x = generate_example_inputs(mpls_graph, util)
    y = generate_example_output(x)
    return (x, y)


def generate_dataset(m, filename):
    for source, dest in gutil.destinations[0]:
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
            new_data, new_label = generate_example(gutil)

            if cnt[new_label] < examples_per_route:
                new_datas.append(new_data)
                new_labels.append(new_label)
                cnt[new_label] += 1

            if len(new_datas) >= examples_per_route * unique_routes_cnt:
                break

            i += 1
            if i % 100 == 0:
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


generate_dataset(100, 'dataset2.csv')
