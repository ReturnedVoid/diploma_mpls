from keras.models import model_from_json
import numpy as np
from data import X, Y
import keras
from keras import losses
# from neural import num_of_inputs, num_of_outputs

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")

loaded_model.compile(optimizer=keras.optimizers.Adam(lr=0.001),
                     loss=losses.mean_squared_error,
                     metrics=['accuracy'])
scores = loaded_model.evaluate(X, Y)
print("\n%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1]*100))

# make prediction
pr = np.loadtxt("dataset.csv", delimiter=",")
pr = pr[:, 0:-10]

pr = pr[129275]
pr = pr.reshape(1, 18)
print(pr)
predictions = loaded_model.predict(pr)
# round predictions
# rounded = [round(x[0]) for x in predictions]
print(predictions)
