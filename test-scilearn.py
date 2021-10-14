from sklearn import svm
import numpy as np
import pickle

data_5 = np.load('data_5.npy')
data_f = np.load('data_f.npy')

data_5_final = []
data_f_final = []
for i in range(np.size(data_5, 0)):
    for j in range(3):
        data_5[i, j, :] = data_5[i, j, :] - data_5[i, j, 0]
    data_5_final.append(np.delete(data_5[i], 0, axis=1))

for i in range(np.size(data_f, 0)):
    for j in range(3):
        data_f[i, j, :] = data_f[i, j, :] - data_f[i, j, 0]
    data_f_final.append(np.delete(data_f[i], 0, axis=1))


data_5_2d = np.reshape(data_5_final, (10, 60))
data_f_2d = np.reshape(data_f_final, (12, 60))

# print(data_5[2])

target_5 = np.ones(np.size(data_5, 0))
target_f = np.zeros(np.size(data_f, 0))

X = np.append(data_5_2d, data_f_2d, axis=0)
y = np.append(target_5, target_f)

clf = svm.SVC()
clf.fit(X, y)
print(clf.predict([X[1]]))

with open('svm.pickle', 'wb') as fw:
    pickle.dump(clf, fw)