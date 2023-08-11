"""
Created on May 22 from Francesco
"""
import json

import pandas as pd
import tensorflow as tf

from tensorflow import keras
from tensorflow import feature_column
from sklearn.model_selection import train_test_split

import os

# A utility method to create a tf.data dataset from a Pandas Dataframe
def df_to_dataset(dataframe, label_index, shuffle=True, batch_size=32):
    dataframe = dataframe.copy()
    labels = dataframe.pop(label_index)
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    return ds


""" Converts a single dataframe to a tensorflow dataset
If the Dataframe has no label, the label gets set to -1. 
As this label should not be used further one, this is okay.
"""


def show_batch(dataset):
    for batch, label in dataset.take(1):
        for key, value in batch.items():
            print("{:20s}: {}".format(key, value.numpy()))


""" Converts the labels to integers in the interval
Labels should be in the interval [0, number_of_labels) for the neural network.
Returns the labels, the mapping of old and new labels and the number of different labels.
"""


def encode_labels(df, label_index):
    n_labels = 0
    label_dict = {}
    for i in df[label_index]:
        if not i in label_dict.values():
            label_dict[n_labels] = i
            n_labels += 1
    reverse_dict = {y: x for x, y in label_dict.items()}
    df = df.replace(to_replace=reverse_dict)
    return df, label_dict, n_labels


def save_model(model, path='model'):
    model.save(path)  # saving the whole model in directory "model"
    # keras_file = "tfmodel.h5" # Saving in the old .h5 format
    # keras.models.save_model(model, keras_file)

def export_label_dict(label_dict):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, '..', 'database', 'label_dict_100.json')
    with open(file_path, "w") as outfile:
        json.dump(label_dict, outfile)

def build_model():
    label_index = '0.0'  # String Value of the label column
    data_name = 'patients_50000.csv' # name of the patients file used for model training
    n_epochs = 10
    batch_size = 256  # Number of samples the model is trained with before parameters get modified each step


    # load the csv file and convert the labels to integers starting from 0
    dirname = os.path.dirname(__file__)
    patients_csv = os.path.join(dirname, '..', 'database', data_name)
    temp_df = pd.read_csv(patients_csv, dtype=int)
    dataframe, label_dict, n_labels = encode_labels(temp_df, label_index)
    print(n_labels + 1, 'different labels')

    # split the data and convert to tensorflow datasets
    train, test = train_test_split(dataframe, test_size=0.2)
    train, val = train_test_split(train, test_size=0.2)
    print(len(train), 'train examples')
    print(len(val), 'validation examples')
    print(len(test), 'test examples')


    train_ds = df_to_dataset(train, label_index, batch_size=batch_size)
    val_ds = df_to_dataset(val, label_index, shuffle=False, batch_size=batch_size)
    test_ds = df_to_dataset(test, label_index, shuffle=False, batch_size=batch_size)

    # Build the feature colums:
    # all features are one hot encoded, so features are numeric
    feature_columns = []
    for feature_batch, label_batch in train_ds.take(1):
        for header in feature_batch.keys():
            feature_columns.append(feature_column.numeric_column(header))
    feature_layer = keras.layers.DenseFeatures(feature_columns)

    # Build the model with standard parameters
    model = keras.Sequential()
    model.add(feature_layer)
    model.add(keras.layers.Dense(128, activation=keras.activations.relu))
    model.add(keras.layers.Dense(128, activation=keras.activations.tanh))
    model.add(keras.layers.Dense(256, activation=keras.activations.tanh))
    model.add(keras.layers.Dense(n_labels))

    # Adam optimizer is standard, loss must be SparseCategoricalCrossentropy,
    # because there are multiple labels, which are not one hot encoded
    model.compile(optimizer='Adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    model.fit(train_ds, validation_data=val_ds, epochs=n_epochs)  # epoch size 10 was sufficient for good accuracy
    print('\n *** Evaluation *** \n')
    model.summary()
    loss, accuracy = model.evaluate(test_ds)
    print('Accuracy: ', accuracy)


    export_label_dict(label_dict) # used to translate the disease label ids back to the original ids

    save_model(model)  # saves current model into directory "test"

    # # Show example results for 10 test patients
    # predictions = model.predict(test_ds)
    # patient_index = 1
    # for prediction, label in zip(predictions[:10], list(test_ds)[0][1][:10]):
    #     prediction = tf.nn.softmax(prediction).numpy()  # Softmax transforms the tensor values to probabilities
    #     print("\n### PATIENT {} ###".format(patient_index))
    #     print("Disease Prediction: ")
    #     for i in range(n_labels):
    #         print("ID {0}: {1:.1f}%".format(label_dict[i], prediction[i] * 100))
    #     print("==> Actual outcome: ", label_dict[label.numpy()])
    #     patient_index += 1

    return model

if __name__ == '__main__':
    build_model()


