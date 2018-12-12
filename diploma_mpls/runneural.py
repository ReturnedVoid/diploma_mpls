from keras.models import load_model
import numpy as np
import data
import keras
from keras import losses

X, Y = data.load_samples()

loaded_model = load_model('model.h5')

loaded_model.compile(optimizer=keras.optimizers.Adam(lr=0.001),
                     loss=losses.mean_squared_error,
                     metrics=['accuracy'])
scores = loaded_model.evaluate(X, Y)
print("\n%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1]*100))

# make prediction
pr = np.loadtxt("validation.csv", delimiter=",")
pr = pr[:, 0:-10]

predictions = loaded_model.predict(pr)

for predi in predictions:
    for i in range(len(predi)):
        predi[i] = round(predi[i])

print(predictions)
with open('predictions.txt', 'w') as f:
    for item in predictions:
        f.write("%s\n" % item)
