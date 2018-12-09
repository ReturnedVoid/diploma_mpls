from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras import losses
import keras
import matplotlib.pyplot as plt
from keras.layers.advanced_activations import LeakyReLU, PReLU


num_of_inputs = 18
num_of_outputs = 10
np.random.seed(7)

dataset = np.loadtxt("dataset2.csv", delimiter=",")
# split into input (X) and output (Y) variables
# np.random.shuffle(dataset)
X = dataset[:, 0:-num_of_outputs]
Y = dataset[:, num_of_inputs:]


# create model
model = Sequential()
model.add(Dense(50, input_dim=num_of_inputs, activation='relu'))
model.add(Dense(25, activation='relu'))
#model.add(Dense(12, activation='relu'))
model.add(Dense(num_of_outputs, activation='relu'))

# Compile model
model.compile(optimizer=keras.optimizers.Adam(lr=0.001),
              loss=losses.mean_squared_error,
              metrics=['accuracy'])

# Fit the model
history = model.fit(X, Y, validation_split=0.2, epochs=400, batch_size=32)


# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# make prediction
pr = np.loadtxt("dataset.csv", delimiter=",")
pr = pr[:, 0:-num_of_outputs]

pr = pr[2598]
pr = pr.reshape(1, num_of_inputs)
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
