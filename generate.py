import csv
from diploma_mpls.graph import GraphUtil
import numpy as np
import itertools
import os
from mpls_spec import ETHERNET_MAX_THROUGHTPUT_MBIT as emtm
from mpls_spec import MPLS_TUNNEL_MAX_LOAD_KOEF as mtmlk

gutil = GraphUtil()
unique_routes = gutil.unique_routes
unique_routes_cnt = gutil.unique_routes_cnt
mpls_graph = gutil.graph
ETH_MAX_THR = 100  # Mbit


def del_sample_files(*files):
    for f in files:
        try:
            os.remove(f)
        except Exception:
            pass


def generate_example_inputs(g, util):
    util.init_network_load()

    sample = []
    sample.append(np.random.choice(list(range(8))))
    sample.append(gutil.source)
    sample.append(gutil.target)

    threads = [round(np.random.uniform(8, 12), 2) for _ in range(10)]
    for k in gutil.tunnels_load[:5]:
        sample.append(k)
    for thread in threads:
        sample.append(thread)

    return sample


def generate_example_output(sample, util):
    coses = list(range(8))
    current_cos = sample[0]
    threads = sample[8:]
    cnt = [0] * len(threads)

    source = util.source
    target = util.target

    forward = True if (source, target) in util.destinations[0] else False
    # if traffic class >= max tunnel class
    if current_cos >= 2:
        current_cos = 2

    if forward:
        tuns = [t for t in gutil.tunnels[0:5] if t.cos == current_cos]
    else:
        tuns = [t for t in gutil.tunnels[5:] if t.cos == current_cos]

    for i in range(len(threads)):
        d = [(t, gutil.tunnels_load[t.index]) for t in tuns]

        best_tunnel = min(d, key=lambda x: x[1])[0]
        if gutil.add_load(
                best_tunnel.index, threads[i] / emtm).load >= mtmlk:
            index = coses.index(best_tunnel.cos)
            if index - 1 != -1:
                index -= 1

            if forward:
                tuns = [t for t in gutil.tunnels[0:5] if t.cos == coses[index]]
            else:
                tuns = [t for t in gutil.tunnels[5:] if t.cos == coses[index]]
            d = [(t, gutil.tunnels_load[t.index]) for t in tuns]
            best_tunnel = min(d, key=lambda x: x[1])[0]
        cnt[i] = best_tunnel.index
    return cnt


def generate_example(util):
    x = generate_example_inputs(mpls_graph, util)
    y = generate_example_output(x, util)
    return (x, y)


def generate_dataset(m, filename):
    print('Generating dataset for {}'.format(filename))
    f = open(filename, 'a', newline='')
    all_destinations = itertools.chain(gutil.destinations[0],
                                       gutil.destinations[1])

    for source, dest in all_destinations:
        gutil.source = source
        gutil.target = dest

        print('Generating samples for {0},{1} destination'
              .format(source, dest))
        try:
            current_dest_index = gutil.destinations[0].index((source, dest))
            print('{}% done'.format(current_dest_index / 16 * 100))
        except ValueError:
            current_dest_index = gutil.destinations[1].index((source, dest))
            current_dest_index += 8
            print('{}% done'.format(current_dest_index / 16 * 100))

        for k in range(8):
            i = 0
            while i < m:
                inp, out = generate_example(gutil)
                if inp[0] != k:
                    continue
                sample = []
                for z in itertools.chain(inp, out):
                    sample.append(z)
                writer = csv.writer(f)
                writer.writerow(sample)

                i += 1
    f.close()


del_sample_files('dataset.csv', 'validation.csv')
generate_dataset(400, 'dataset.csv')
generate_dataset(10, 'validation.csv')
