import os
import json
import pandas as pd
import tensorflow as tf

from machine_learning.build_model import build_model, df_to_dataset
from machine_learning.symptom_suggestor import convert_input_list

def create_sample_patient():
    # load the csv file and convert the labels to integers starting from 0
    dirname = os.path.dirname(__file__)
    in_path = os.path.join(dirname, '..', 'database', 'patients_50000.csv')
    df = pd.read_csv(in_path, dtype=int)
    all_symptoms = list(df.columns)
    d = {s: [0, 0] for s in all_symptoms}
    df = pd.DataFrame(data=d)
    print(df)
    out_path = os.path.join(dirname, '..', 'database', 'sample_patient.csv')
    df.to_csv(out_path, index=False)


class RoboDoctor:
    """Makes Disease predictions for given symptoms using a deep neural network

    The Prediction has probabilities for all possible diseases
    """
    model = None
    sample_patient = None
    label_string = '0.0'
    label_dict = {}

    def __init__(self):
        dirname = os.path.dirname(__file__)
        model_path = os.path.join(dirname, '..', 'machine_learning', 'model')
        self.model = tf.keras.models.load_model(model_path)

        patient_path = os.path.join(dirname, '..', 'database', 'sample_patient.csv')
        self.sample_patient = pd.read_csv(patient_path)

        label_dict_path = os.path.join(dirname, '..', 'database', 'label_dict_100.json')
        with open(label_dict_path, "r") as label_file:
            self.label_dict = json.load(label_file)

    def predict_single(self, symptoms):
        """Predict the disease of a single patient

        :param symptoms: list of all symptom IDs
        :return: a dictionary with probabilities for all diseases in the database
        """
        # use a sample dataframe with 2 rows all zeros. We use 2 rows, because the tensor rank must be 1 and not 0
        patient_df = self.sample_patient.copy()
        symptoms = convert_input_list(symptoms)
        for s in symptoms:
            patient_df.at[0, s] = 1
            patient_df.at[1, s] = 1
        patient_ds = df_to_dataset(patient_df, self.label_string, shuffle=False, batch_size=1)
        prediction = self.model.predict(patient_ds)
        prediction = tf.nn.softmax(prediction[0]).numpy()  # only the first prediction is relevant
        return {self.label_dict[str(i)]: prediction[i] for i in range(len(prediction))}


if __name__ == '__main__':
    # Sample Use
    robo_doc = RoboDoctor()
    # make a prediction for symptoms 9, 11, 17, 21, 991
    res1 = robo_doc.predict_single([9, 11, 17, 21, 991])
    res2 = robo_doc.predict_single([190, 233, 288, 170, 17])
    res3 = robo_doc.predict_single([996, 104, 1009, 77, 147])
    res4 = robo_doc.predict_single([192, 128, 92, 53, 93])
    # result has probabilities for all possible diseases
    print("************************************************************************************************************************************")
    print(res1)
    print("************************************************************************************************************************************")
    print(res2)
    print("************************************************************************************************************************************")
    print(res3)
    print("************************************************************************************************************************************")
    print(res4)
    print("************************************************************************************************************************************")

