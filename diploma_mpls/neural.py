from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from keras import losses
import keras
import matplotlib.pyplot as plt
import data
from project_folders import SAMPLES_PATH, MODELS_PATH

np.random.seed(7)

dataset = np.loadtxt(
    '{}/dataset.csv'.format(SAMPLES_PATH), delimiter=",")
# split into input (X) and output (Y) variables
np.random.shuffle(dataset)

X, Y = data.load_samples()

# create model
model = Sequential()
model.add(Dense(36, input_dim=data.num_of_inputs, activation='relu'))
model.add(Dense(150, activation='relu'))
model.add(Dense(150, activation='relu'))
model.add(Dense(data.num_of_outputs, activation='relu'))

# Compile model
model.compile(optimizer=keras.optimizers.Adam(lr=0.001),
              loss=losses.mean_squared_error,
              metrics=['accuracy'])

# Fit the model
history = model.fit(X, Y, validation_split=0.2, epochs=100, batch_size=32)


# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

model.save('{}/model.h5'.format(MODELS_PATH))


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
