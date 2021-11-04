from sklearn import svm, model_selection, metrics
import numpy as np
import pickle

import sklearn

data_5 = np.load('data_5.npy')
data_f = np.load('data_f.npy')

data_5_final = []
data_f_final = []
num_data_5 = np.size(data_5, 0)
num_data_f = np.size(data_f, 0)

for i in range(num_data_5):
    for j in range(3):
        data_5[i, j, :] = data_5[i, j, :] - data_5[i, j, 0]
    data_5_final.append(np.delete(data_5[i], 0, axis=1))

for i in range(num_data_f):
    for j in range(3):
        data_f[i, j, :] = data_f[i, j, :] - data_f[i, j, 0]
    data_f_final.append(np.delete(data_f[i], 0, axis=1))


data_5_2d = np.reshape(data_5_final, (num_data_5, 60))
data_f_2d = np.reshape(data_f_final, (num_data_f, 60))

# print(data_5[2])

target_5 = np.ones(np.size(data_5, 0))
target_f = np.zeros(np.size(data_f, 0))

X = np.append(data_5_2d, data_f_2d, axis=0)
y = np.append(target_5, target_f)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3, random_state=0)

clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

y_pred = clf.predict((X_test))
print(y_pred)
score = metrics.accuracy_score(y_test, y_pred)
print(score)


with open('svm.pickle', 'wb') as fw:
    pickle.dump(clf, fw)