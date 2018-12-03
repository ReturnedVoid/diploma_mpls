from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras import losses

np.random.seed(7)

dataset = np.loadtxt("dataset2.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:, 0:-15]
Y = dataset[:, 23:]

# create model
model = Sequential()
model.add(Dense(410, input_dim=23, activation='relu'))
model.add(Dense(410, activation='relu'))
model.add(Dense(15, activation='sigmoid'))

# Compile model
model.compile(loss=losses.mean_squared_error,
              optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)


# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# make prediction
predictions = model.predict(X)
# round predictions
rounded = [round(x[0]) for x in predictions]
print(rounded)
