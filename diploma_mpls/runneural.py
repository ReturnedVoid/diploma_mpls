from keras.models import load_model
import numpy as np
import data
from project_folders import SAMPLES_PATH, MODELS_PATH, PREDICTIONS_PATH

X, Y = data.load_samples()

loaded_model = load_model('{}/model.h5'.format(MODELS_PATH))


scores = loaded_model.evaluate(X, Y)
print("\n%s: %.2f%%" % (loaded_model.metrics_names[1], scores[1]*100))

# make prediction
pr = np.loadtxt('{}/validation.csv'.format(SAMPLES_PATH), delimiter=",")
pr = pr[:, 0:-data.num_of_outputs]

predictions = loaded_model.predict(pr)

for predi in predictions:
    for i in range(len(predi)):
        predi[i] = round(predi[i])

with open('{}/predictions.txt'.format(PREDICTIONS_PATH), 'w') as f:
    for item in predictions:
        f.write("%s\n" % item)
