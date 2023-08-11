"""
Created on June 8 from Francesco
"""
import os
import pandas as pd


# converts the input to a list of strings, e.g. 15 => ['15.0']
def convert_input_list(ids):
    if not type(ids) is list:
        ids = [ids]
    else:
        ids = ids.copy() # Lennart: added copy() to prevent original symptoms list being converted to float
    for i in range(len(ids)):
        ids[i] = str(float(ids[i]))
    return ids


# converts back to a list of ints, e.g. ['15.0', '16.0', '21.0'] => [15, 16, 21]
def convert_output_list(ids):
    for i in range(len(ids)):
        ids[i] = int(float(ids[i]))
    return ids


class SymptomSuggestor:
    """ Suggests the most common symptoms for shown symptoms

    For given shown and excluded symptoms the database of all patients is queried to find all patients
    with a similar symptom pattern. Then the occurrence of other symptoms of those patients is calculated
    and the most common symptoms are suggested.
    """

    label_string = '0.0'  # name of the label / disease column in the database
    patients_df = pd.DataFrame()
    n_suggests = 3  # number of suggestions for similar symptoms

    def __init__(self):
        dirname = os.path.dirname(__file__)
        patients_csv = os.path.join(dirname, '..', 'database', 'patients_50000.csv')
        self.patients_df = pd.read_csv(patients_csv, dtype=int).drop(columns=self.label_string)

    def suggest(self, shown_symptoms=None, excluded_symptoms=None):
        """Suggests most common symptoms

        :param shown_symptoms: IDs of all symptoms the user has. Can be single value or list.
        :param excluded_symptoms: IDs of all symptoms the user doesn't have. Can be single value or list.
        :return: List of the IDs of the most common symptoms
        """

        # allow integers and single values as input
        if excluded_symptoms is None:
            excluded_symptoms = []
        if shown_symptoms is None:
            shown_symptoms = []
        shown_symptoms = convert_input_list(shown_symptoms)
        excluded_symptoms = convert_input_list(excluded_symptoms)

        df = self.patients_df
        similar_patients = df  # default all patients are similar
        if shown_symptoms:
            # build a dataframe only containing patients with similar symptoms
            locator = (df[str(float(shown_symptoms[0]))] == 1)
            for i in range(1, len(shown_symptoms)):
                locator = locator & (df[str(float(shown_symptoms[i]))] == 1)
            for i in range(len(excluded_symptoms)):
                locator = locator & (df[str(float(excluded_symptoms[i]))] == 0)
            similar_patients = df.loc[locator]

        # remove the last added symptom, if no patients had this combination of symptoms
        # if there is only 1 symptom which was never expressed,
        # the method call with empty lists returns the most common symptoms
        if similar_patients.empty:
            del shown_symptoms[-1]
            return self.suggest(shown_symptoms, excluded_symptoms)

        # only suggest new symptoms
        similar_patients = similar_patients.drop(columns=(shown_symptoms + excluded_symptoms))
        # take the sum to calculate the occurrence of other symptoms
        sum_df = similar_patients.sum(axis=0)

        # filter the sums for the most common symptoms
        suggestion = []
        for i in range(self.n_suggests):
            max = sum_df.idxmax(axis=0)
            suggestion.append(max)
            sum_df = sum_df.drop(max)
        return convert_output_list(suggestion)


if __name__ == '__main__':
    # sample uses
    symptom_suggestor = SymptomSuggestor()
    print(' ** Sample Uses **')

    # if called with empty arguments, you get the most common symptoms
    s = symptom_suggestor.suggest()
    print('\ncall suggest(): ')
    print('Default most common symptoms: ' + str(s))

    # then the user might show symptom 16
    s = symptom_suggestor.suggest(16)
    print('\ncall suggest(16): ')
    print('Most common symptoms: ' + str(s))

    # or the user might not show any of those symptoms
    s = symptom_suggestor.suggest(excluded_symptoms=[16, 10, 15])
    print('\ncall suggest(excluded_symptoms=[16, 10, 15]): ')
    print('Most common symptoms: ' + str(s))

    # further one you can combine shown and excluded symptoms
    s = symptom_suggestor.suggest([64, 95], [28, 15, 54, 16])
    print('\ncall suggest([64, 95], [28, 15, 54, 16]): ')
    print('Most common symptoms: ' + str(s))

    # for calls without any match you get the default common symptoms
    s = symptom_suggestor.suggest(17, 17)
    print('\ncall suggest(17, 17): ')
    print('Most common symptoms: ' + str(s))
