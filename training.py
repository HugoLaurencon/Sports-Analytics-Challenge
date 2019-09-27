from data_extraction import data_first_task, data_task_2_3
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint

def training_task_1(data_task_1, num_training_examples):
    Xtrain_task_1 = data_task_1[0:num_training_examples, 1:]
    Xtest_task_1 = data_task_1[num_training_examples:, 1:]
    
    y = data_task_1[:, 0]
    dico_player = {}
    for uID in y:
        dico_player[int(uID)] = 1
    list_player = dico_player.keys()
    list_player.sort()
    dico_id = {list_player[i]: i for i in range(len(list_player))}
    for i in range(len(y)):
        y[i] = dico_id[y[i]]
    
    ytrain_task_1 = y[0:num_training_examples]
    ytrain_task_1 = keras.utils.to_categorical(ytrain_task_1, num_classes = len(list_player))
    ytest_task_1 = y[num_training_examples:]
    ytest_task_1 = keras.utils.to_categorical(ytest_task_1, num_classes = len(list_player))
    
    model = Sequential()
    model.add(Dense(500, input_dim = 380, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(233, activation='softmax'))
    
    model.compile(loss = 'categorical_crossentropy', optimizer=Adam(lr = 0.001), metrics = ['accuracy'])
    
    filepath = "w_task_1-{epoch:02d}-{val_acc:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor = 'val_acc', verbose = 1, save_best_only = False, mode = 'max')
    callbacks_list = [checkpoint]
    
    model.fit(Xtrain_task_1, ytrain_task_1, epochs = 400, batch_size = 10000,
              validation_data = (Xtest_task_1, ytest_task_1), callbacks = callbacks_list, verbose = 1)
    
    scorestrain = model.evaluate(Xtrain_task_1, ytrain_task_1)
    print('Test loss train:', scorestrain[0])
    print('Test accuracy train:', scorestrain[1])
    scorestest = model.evaluate(Xtest_task_1, ytest_task_1)
    print('Test loss test:', scorestest[0])
    print('Test accuracy test:', scorestest[1])


def training_task_2(data_task_2, num_training_examples):
    Xtrain_task_2 = data_task_2[0:num_training_examples, 1:]
    ytrain_task_2 = data_task_2[0:num_training_examples, 0]
    ytrain_task_2 = keras.utils.to_categorical(ytrain_task_2, num_classes = 2)
    
    Xtest_task_2 = data_task_2[num_training_examples:, 1:]
    ytest_task_2 = data_task_2[num_training_examples:, 0]
    ytest_task_2 = keras.utils.to_categorical(ytest_task_2, num_classes = 2)
    
    model = Sequential()
    model.add(Dense(2000, input_dim = 245, activation = 'relu'))
    model.add(Dropout(0.1))
    model.add(Dense(2, activation = 'softmax'))
    
    model.compile(loss = 'categorical_crossentropy', optimizer = Adam(lr=0.001), metrics = ['accuracy'])
    
    filepath = "w_task_2-{epoch:02d}-{val_acc:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor = 'val_acc', verbose = 1, save_best_only = False, mode = 'max')
    callbacks_list = [checkpoint]
    
    model.fit(Xtrain_task_2, ytrain_task_2, epochs = 200, batch_size = 1000,
              validation_data = (Xtest_task_2, ytest_task_2), callbacks = callbacks_list, verbose = 1)
    
    scorestrain = model.evaluate(Xtrain_task_2, ytrain_task_2)
    print('Test loss train:', scorestrain[0])
    print('Test accuracy train:', scorestrain[1])
    scorestest = model.evaluate(Xtest_task_2, ytest_task_2)
    print('Test loss test:', scorestest[0])
    print('Test accuracy test:', scorestest[1])


def training_task_3(data_task_3, num_training_examples):
    Xtrain_task_3 = data_task_3[0:num_training_examples, 2:]
    ytrain_task_3 = data_task_3[0:num_training_examples, 0:2]
    
    Xtest_task_3 = data_task_3[num_training_examples:, 2:]
    ytest_task_3 = data_task_3[num_training_examples:, 0:2]
    
    model = Sequential()
    model.add(Dense(2500, input_dim = 245, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(2, activation='linear'))
    
    model.compile(loss = 'mse', optimizer = Adam(lr=0.001), metrics = ['mse'])
    
    filepath = "w_task_3-{epoch:02d}-{val_acc:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor = 'val_loss', verbose = 1, save_best_only = False, mode = 'min')
    callbacks_list = [checkpoint]
    
    model.fit(Xtrain_task_3, ytrain_task_3, epochs = 50, batch_size = 1000,
              validation_data = (Xtest_task_3, ytest_task_3), callbacks = callbacks_list, verbose = 1)
    
    scorestrain = model.evaluate(Xtrain_task_3, ytrain_task_3)
    print('Test loss train:', scorestrain[0])
    scorestest = model.evaluate(Xtest_task_3, ytest_task_3)
    print('Test loss test:', scorestest[0])


path_to_matches_directory = r'data/matches/'

data_task_1 = data_first_task(path_to_matches_directory)
data_task_2, data_task_3 = data_task_2_3(path_to_matches_directory)

num_training_examples_task_1 = 18000
num_training_examples_task_2_3 = 100000

training_task_1(data_task_1, num_training_examples_task_1)
training_task_2(data_task_2, num_training_examples_task_2_3)
training_task_3(data_task_3, num_training_examples_task_2_3)

