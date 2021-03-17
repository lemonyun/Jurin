import pandas as pd
train_data1 = pd.read_csv("./train0315_112.csv") 
train_data2 = pd.read_csv("./train0312_89.csv")
train_data3 = pd.read_csv("./train0311_123.csv")

train_data = pd.concat([train_data1, train_data2, train_data3])
test_data = pd.read_csv("./test0310_117.csv")

train_data

print(train_data.iloc[5555])

type(train_data)

test_data

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline 
import matplotlib.pyplot as plt

train_data['label'].value_counts().plot(kind='bar')

test_data['label'].value_counts().plot(kind='bar')

print(train_data.groupby('label').size().reset_index(name='count')) 
print(test_data.groupby('label').size().reset_index(name='count'))

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

# !apt-get update
# !apt-get install g++ openjdk-8-jdk python-dev python3-dev
# !pip3 install JPype1-py3
# !pip3 install konlpy
# !JAVA_HOME="C:\Program Files\Java\jdk-15.0.2"

import konlpy 
from konlpy.tag import Okt 
okt = Okt() 
X_train = [] 
for sentence in train_data['title']: 
  temp_X = [] 
  temp_X = okt.morphs(sentence, stem=True) # 토큰화 
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거 
  X_train.append(temp_X) 
  
X_test = [] 
for sentence in test_data['title']: 
  temp_X = [] 
  temp_X = okt.morphs(sentence, stem=True) # 토큰화 
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거 
  X_test.append(temp_X)

print(X_train[:3])
print(X_test[:3])

from keras.preprocessing.text import Tokenizer 
max_words = 35000 
tokenizer = Tokenizer(num_words = max_words) 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train) 
X_test = tokenizer.texts_to_sequences(X_test)

print(X_train[:3])
print(X_test[:3])

import numpy as np 

y_train = [] 
y_test = [] 

for i in range(len(train_data['label'])): 
  if train_data['label'].iloc[i] == 1: 
    y_train.append([0, 0, 1]) 
  elif train_data['label'].iloc[i] == 0: 
    y_train.append([0, 1, 0]) 
  elif train_data['label'].iloc[i] == -1: 
    y_train.append([1, 0, 0]) 

for i in range(len(test_data['label'])): 
  if test_data['label'].iloc[i] == 1: 
    y_test.append([0, 0, 1]) 
  elif test_data['label'].iloc[i] == 0: 
    y_test.append([0, 1, 0]) 
  elif test_data['label'].iloc[i] == -1: 
    y_test.append([1, 0, 0]) 

y_train = np.array(y_train) 
y_test = np.array(y_test)

y_train
y_test

"""### 모델 만들기"""

from keras.layers import Embedding, Dense, LSTM 
from keras.models import Sequential 
from keras.preprocessing.sequence import pad_sequences 

max_len = 20 
X_train = pad_sequences(X_train, maxlen=max_len) 
X_test = pad_sequences(X_test, maxlen=max_len)

model = Sequential() 
model.add(Embedding(max_words, 100)) 
model.add(LSTM(128)) 
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy']) 
history = model.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.1)

print("\n 테스트 정확도 : {:.2f}%".format(model.evaluate(X_test, y_test)[1] * 100))



model2 = Sequential()
model2.add(Embedding(max_words, 100))
model2.add(LSTM(128))
model2.add(Dense(3, activation='softmax'))

model2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model2.fit(X_train, y_train, epochs=10, batch_size=10, validation_split=0.1)

print("\n 테스트 정확도 : {:.2f}%".format(model2.evaluate(X_test, y_test)[1] * 100))

predict = model.predict(X_test)

import numpy as np 
predict_labels = np.argmax(predict, axis=1) 
original_labels = np.argmax(y_test, axis=1)

cnt = 0
for i in range(len(original_labels)):
  if original_labels[i] != predict_labels[i]:
    cnt += 1
    print("기사제목 : ", test_data['title'].iloc[i], "/\t 원래 라벨 : ", original_labels[i], "/\t예측한 라벨 : ", predict_labels[i])

len(test_data)

print(cnt)

model.save("rmsprop_v1.h5")
model2.save("adam_v1.h5")

