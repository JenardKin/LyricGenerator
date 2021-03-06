from __future__ import print_function
import collections
import os
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Embedding, Dropout, TimeDistributed
from keras.layers import LSTM
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint
import numpy as np
import argparse

"""To run this code, you'll need to first download and extract the text dataset
    from here: http://www.fit.vutbr.cz/~imikolov/rnnlm/simple-examples.tgz. Change the
    data_path variable below to your local exraction path"""

#data_path = "C:\\Users\Andy\Documents\simple-examples\data"
data_path = 'data/'

parser = argparse.ArgumentParser()
parser.add_argument('run_opt', type=int, default=1, help='An integer: 1 to train, 2 to test')
parser.add_argument('--data_path', type=str, default=data_path, help='The full path of the training data')
parser.add_argument('--load_model', type=str, default='data/final_model.hdf5', help='The model will be used')
parser.add_argument("--nb_epochs", type=int, default=5, help="number of epochs")
parser.add_argument("--num_steps", type=int, default=5, help="number of time steps")
parser.add_argument("--skip_step", type=int, default=2, help="number of skip steps")
parser.add_argument("--hidden_size", type=int, default=500, help="number of hidden size of LSTM cell")
parser.add_argument("--test_string", type=str, default='I loved how you walk with your hands in', help="number of epochs")
args = parser.parse_args()
print(args)
if args.data_path:
    data_path = args.data_path

def read_words(filename):
    with tf.gfile.GFile(filename, "r") as f:
        return f.read().replace("\n", " ").split()
#.decode("utf-8")

def build_vocab(filename):
    data = read_words(filename)

    counter = collections.Counter(data)
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))

    words, _ = list(zip(*count_pairs))
    word_to_id = dict(zip(words, range(len(words))))

    return word_to_id


def file_to_word_ids(filename, word_to_id):
    data = read_words(filename)
    return [word_to_id[word] for word in data if word in word_to_id]

def test_only(test_string, num_steps):  # here test_string has been splited into a list
    train_path = os.path.join(data_path, "ptb.train.txt")
#    test_path = os.path.join(data_path, "ptb.test.txt")

    # build the complete vocabulary, then convert text data to list of integers
    word_to_id = build_vocab(train_path)
    data = test_string.split()
    test_data = [word_to_id[word] for word in data if word in word_to_id]    
    
    return test_data[-num_steps:]       

def load_data():
    # get the data paths
    train_path = os.path.join(data_path, "ptb.train.txt")
    valid_path = os.path.join(data_path, "ptb.valid.txt")
#    test_path = os.path.join(data_path, "ptb.test.txt")

    # build the complete vocabulary, then convert text data to list of integers
    word_to_id = build_vocab(train_path)
    train_data = file_to_word_ids(train_path, word_to_id)
    valid_data = file_to_word_ids(valid_path, word_to_id)
#    test_data = file_to_word_ids(test_path, word_to_id)
    vocabulary = len(word_to_id)
    reversed_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))

    print(train_data[:5])
    print(word_to_id)
    print(len(train_data))
    print(vocabulary)
    print(" ".join([reversed_dictionary[x] for x in train_data[:10]]))
    return train_data, valid_data, vocabulary, reversed_dictionary

train_data, valid_data, vocabulary, reversed_dictionary = load_data()


class KerasBatchGenerator(object):

    def __init__(self, data, num_steps, batch_size, vocabulary, skip_step=5):
        self.data = data
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.vocabulary = vocabulary
        # this will track the progress of the batches sequentially through the
        # data set - once the data reaches the end of the data set it will reset
        # back to zero
        self.current_idx = 0
        # skip_step is the number of words which will be skipped before the next
        # batch is skimmed from the data set
        self.skip_step = skip_step

    def generate(self):
        x = np.zeros((self.batch_size, self.num_steps))
        y = np.zeros((self.batch_size, self.num_steps, self.vocabulary))
        while True:
            for i in range(self.batch_size):
                if self.current_idx + self.num_steps >= len(self.data):
                    # reset the index back to the start of the data set
                    self.current_idx = 0
                x[i, :] = self.data[self.current_idx:self.current_idx + self.num_steps]
                temp_y = self.data[self.current_idx + 1:self.current_idx + self.num_steps + 1]
                # convert all of temp_y into a one hot representation
                y[i, :, :] = to_categorical(temp_y, num_classes=self.vocabulary)
                self.current_idx += self.skip_step
            yield x, y

skip_step=args.skip_step


class KerasBatchGenerator2(object):

    def __init__(self, data, num_steps, batch_size, vocabulary, skip_step=skip_step):
        self.data = data
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.vocabulary = vocabulary
        # this will track the progress of the batches sequentially through the
        # data set - once the data reaches the end of the data set it will reset
        # back to zero
        self.current_idx = 0
        # skip_step is the number of words which will be skipped before the next
        # batch is skimmed from the data set
        self.skip_step = skip_step

    def generate(self):
        x = np.zeros((self.batch_size, self.num_steps))
#        y = np.zeros((self.batch_size, self.num_steps, self.vocabulary))
        while True:
            for i in range(self.batch_size):
                if self.current_idx + self.num_steps >= len(self.data):
                    # reset the index back to the start of the data set
                    self.current_idx = 0
       
#                print(i)
#                print(x.shape)
#                print(len(self.data))
#                print(self.current_idx)
#                print(self.current_idx + self.num_steps)
                
                x[i, :] = self.data[self.current_idx:self.current_idx + self.num_steps]
#                temp_y = self.data[self.current_idx + 1:self.current_idx + self.num_steps + 1]
                # convert all of temp_y into a one hot representation
#                y[i, :, :] = to_categorical(temp_y, num_classes=self.vocabulary)
                self.current_idx += self.skip_step
            yield x
            
num_steps = args.num_steps
batch_size = 100
train_data_generator = KerasBatchGenerator(train_data, num_steps, batch_size, vocabulary)
#                                           skip_step=num_steps)
valid_data_generator = KerasBatchGenerator(valid_data, num_steps, batch_size, vocabulary)
#                                           skip_step=num_steps)

hidden_size = args.hidden_size
use_dropout=True
model = Sequential()
model.add(Embedding(vocabulary, hidden_size, input_length=num_steps))
model.add(LSTM(hidden_size, return_sequences=True))
model.add(LSTM(hidden_size, return_sequences=True))
if use_dropout:
    model.add(Dropout(0.5))
model.add(TimeDistributed(Dense(vocabulary)))
model.add(Activation('softmax'))

optimizer = Adam()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])

print(model.summary())
checkpointer = ModelCheckpoint(filepath=data_path + '/model-{epoch:02d}.hdf5', verbose=1, monitor='val_categorical_accuracy',save_best_only=True, mode="max")
num_epochs = args.nb_epochs
if args.run_opt == 1:
#    model.fit_generator(train_data_generator.generate(), epochs=num_epochs,
#                        validation_data=valid_data_generator.generate(),validation_steps=len(valid_data)//(batch_size*num_steps),callbacks=[checkpointer])
    # model.fit_generator(train_data_generator.generate(), 2000, num_epochs,
    #                     validation_data=valid_data_generator.generate(),
    #                     validation_steps=10)
    hist = model.fit_generator(train_data_generator.generate(), len(train_data)//(batch_size*skip_step), num_epochs,
                        validation_data=valid_data_generator.generate(),
                        validation_steps=len(valid_data)//(batch_size*skip_step), callbacks=[checkpointer])
    
    
    np.save(data_path + 'hist.npy',hist.history)
    model.save(data_path + "final_model.hdf5")
    
    
elif args.run_opt == 2:
    m = args.load_model
    model = load_model(m)
#    dummy_iters = 40
#    example_training_generator = KerasBatchGenerator(train_data, num_steps, 1, vocabulary,
#                                                     skip_step=1)
#    print("Training data:")
#    for i in range(dummy_iters):
#        dummy = next(example_training_generator.generate())
#    num_predict = 10
#    true_print_out = "Actual words: "
#    pred_print_out = "Predicted words: "
#    for i in range(num_predict):
#        data = next(example_training_generator.generate())
#        prediction = model.predict(data[0])
#        predict_word = np.argmax(prediction[:, num_steps-1, :])
#        true_print_out += reversed_dictionary[train_data[num_steps + dummy_iters + i]] + " "
#        pred_print_out += reversed_dictionary[predict_word] + " "
#    print(true_print_out)
#    print(pred_print_out)
    # test data set
#    dummy_iters = 40
    
    test_string = args.test_string
#    num_steps = 5
#    test_data = test_only(test_string)
#    example_test_generator = KerasBatchGenerator2(test_data, num_steps, 1, vocabulary, skip_step=1)
    print("Test string: "+test_string)
#    for i in range(dummy_iters):
#        dummy = next(example_test_generator.generate())
    num_predict = 100
#    num_steps = 5
#    true_print_out = "Actual words: "
    pred_print_out = test_string+' '
    for i in range(num_predict):
#        print(i)
        test_data = test_only(test_string, num_steps)
        
        example_test_generator = KerasBatchGenerator2(test_data, num_steps, 1, vocabulary, skip_step=1)           
           
        data = next(example_test_generator.generate())
        prediction = model.predict(data)
        predict_word = np.argmax(prediction[:, num_steps - 1, :])
        
#        true_print_out += reversed_dictionary[test_data[num_steps + dummy_iters + i]] + " "
        pred_print_out += reversed_dictionary[predict_word] + " "
        test_string = pred_print_out
        

#    print(true_print_out)
    print(pred_print_out)





