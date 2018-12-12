import numpy as np

num_of_inputs = 18
num_of_outputs = 10


def load_samples():
    dataset = np.loadtxt("dataset.csv", delimiter=",")
    # split into input (X) and output (Y) variables
    np.random.shuffle(dataset)
    X = dataset[:, 0:-10]
    Y = dataset[:, 18:]
    return X, Y
