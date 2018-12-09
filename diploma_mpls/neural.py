from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras import losses
import keras
import matplotlib.pyplot as plt
from keras.layers.advanced_activations import LeakyReLU, PReLU


np.random.seed(7)

dataset = np.loadtxt("dataset2.csv", delimiter=",")
# split into input (X) and output (Y) variables
np.random.shuffle(dataset)
X = dataset[:, 0:-15]
Y = dataset[:, 23:]


# create model
model = Sequential()
model.add(Dense(32, input_dim=23, activation='linear'))
model.add(Dense(80, activation='linear'))
model.add(LeakyReLU(alpha=.001))   # add an advanced activation
# model.add(Dense(48, activation='leakyrelu'))
model.add(Dense(15, activation='relu'))

# Compile model
model.compile(optimizer=keras.optimizers.Adam(lr=0.001),
              loss=losses.mean_squared_error,
              metrics=['accuracy'])

# Fit the model
history = model.fit(X, Y, validation_split=0.3, epochs=500, batch_size=32)


# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# make prediction
pr = np.loadtxt("dataset.csv", delimiter=",")
pr = pr[:, 0:-15]

pr = pr[8995]
pr = pr.reshape(1, 23)
print(pr)
predictions = model.predict(pr)
# round predictions
# rounded = [round(x[0]) for x in predictions]
print(predictions)


print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
