"""
Created on May 15 from Francesco
"""
import json
import os

from apimedic.api_requests import get_auth_token, get_item
from apimedic.auth_data import username, password, medicapi_auth, medicapi_health

class DatabaseBuilder:
    """ Builds a JSON File of Diseases and their associated symptoms + probabilities

    Gets the Data from https://apimedic.com/apitestand. One Disease is manually chosen as starting point.
    Further diseases are chosen from the symptoms of the diseases already in the built database.
    For each disease all its symptoms and their probability of being expressed are put in the database.
    Creates a disease_db.json file and exports the database to it.
    """

    n_diseases = 100 # Number of diseases in the constructed database
    n_api_calls = 0
    api_calls_max = 97
    auth_index = 0
    diseases = []  # Final Disease-Symptom List to be exported
    disease_queue = []  # Queue with the ids of the next diseases to process
    n_queue_added = 0 # Number of diseases the current disease added to the queue
    n_queue_add_max = 3 # Maximum number of diseases, one disease can add to the queue
    all_symptoms = []
    all_issues = []

    def __init__(self):
        self.auth_token = get_auth_token(username[self.auth_index], password[self.auth_index], medicapi_auth)
        self.all_symptoms = self.get_all_symptoms()
        self.all_issues = self.get_all_issues()

    def check_api_calls(self):
        self.n_api_calls += 1
        if self.n_api_calls >= self.api_calls_max:
            self.auth_index += 1
            self.auth_token = get_auth_token(username[self.auth_index], password[self.auth_index], medicapi_auth)
            self.n_api_calls = 0

    def get_all_symptoms(self):
        params = {'token': self.auth_token, 'format': 'json', 'language': 'en-gb'}
        response = get_item('symptoms', params=params, url=medicapi_health)
        self.check_api_calls()
        print("API Call " + str(self.n_api_calls))
        return response.json()

    def get_all_issues(self):
        params = {'token': self.auth_token, 'format': 'json', 'language': 'en-gb'}
        response = get_item('issues', params=params, url=medicapi_health)
        self.check_api_calls()
        print("API Call " + str(self.n_api_calls))
        return response.json()

    def get_issue(self, id):
        request = 'issues/' + str(id) + '/info'
        params = {'token': self.auth_token, 'format': 'json', 'language': 'en-gb'}
        response = get_item(item=request, params=params, url=medicapi_health)
        self.check_api_calls()
        print("API Call " + str(self.n_api_calls))
        return response.json()

    def get_diagnosis(self, id):
        params = {'symptoms': str([id]), 'gender': 'male', 'year_of_birth': '25', 'token': self.auth_token, 'format': 'json',
                  'language': 'en-gb'}
        response = get_item('diagnosis', params=params, url=medicapi_health)
        self.check_api_calls()
        print("API Call " + str(self.n_api_calls))
        return response.json()

    def get_id_of_name(self, name, list):
        for item in list:
            if item["Name"] == name:
                return item["ID"]
        return -1

    def is_issue_in_db(self, issue_id):
        if issue_id in self.disease_queue:
            return True
        for item in self.diseases:
            if item["id"] == issue_id:
                return True
        return False

    def get_probability(self, symptom_id, issue_id):
        diagnosis = self.get_diagnosis(symptom_id)
        prob = -100
        for issue in diagnosis:
            if issue["Issue"]["ID"] == issue_id:
                prob = issue["Issue"]["Accuracy"]
                if self.n_queue_added == self.n_queue_add_max:
                    break
            elif self.n_queue_added < self.n_queue_add_max and \
                    not self.is_issue_in_db(issue["Issue"]["ID"]):
                self.disease_queue.append(issue["Issue"]["ID"])
                self.n_queue_added += 1

        return prob/100

    """ Parses the string of all symtoms to a list
    As the symptoms are divided by comma, but some symptoms have a comma and space inside
    the ', ' substring gets replaced first, then the string is split and replaced back last.
    """
    def split_symptoms(self, symptom_str):
        temp_str = symptom_str.replace(", ", "*$*")
        split_list = temp_str.split(',')
        symptoms = []
        for s in split_list:
            symptoms.append(s.replace("*$*", ", "))
        return symptoms

    def build_disease(self, issue):
        issue_id = self.get_id_of_name(issue["Name"], self.all_issues)
        disease = {"name": issue["Name"], "id": issue_id}
        symptom_list = []
        possible_symptoms = self.split_symptoms(issue["PossibleSymptoms"])
        for s in possible_symptoms:
            symptom_id = self.get_id_of_name(s, self.all_symptoms)
            symptom_prob = self.get_probability(symptom_id, issue_id)
            symptom_list.append({"id": symptom_id, "probability": symptom_prob})
        disease["symptoms"] = symptom_list
        return disease

    def build_disease_list(self):
        for i in range(self.n_diseases):
            self.n_queue_added = 0
            issue = self.get_issue(self.disease_queue.pop(0))
            self.diseases.append(self.build_disease(issue))

    def set_start_disease(self, id):
        if len(self.disease_queue) == 0:
            self.disease_queue.append(id)

    def get_issue_descriptions(self):
        """
        Get missing issue descriptions
        :return: None
        """
        self.auth_token = get_auth_token('Kc89A_AWDRT_NET_AUT', 'p7BPk34MtYq9x2H6K', medicapi_auth)
        with open('../database/diseases_100_db.json', 'r') as db:
            disease_db = json.load(db)

        # get list of issue ids in db
        all_issue_ids = [i['id'] for i in disease_db]

        # get existing issue description ids
        issue_ids = [int(''.join(filter(str.isdigit, f))) for f in os.listdir('../database/Diseases')]

        for i in all_issue_ids:
            if (i in all_issue_ids) and (i not in issue_ids):

                response = self.get_issue(i)
                with open('../database/Diseases/Issue{}.json'.format(i), 'w') as file:
                    json.dump(response, file)




