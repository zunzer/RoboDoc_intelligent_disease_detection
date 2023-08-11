import requests
import json
from apimedic.api_requests import get_auth_token, get_item
import auth_data
import pandas as pd
import sys


def writePageToJson(symptoms, issue_id):

    # get api token
    token = get_auth_token(auth_data.username, auth_data.password, auth_data.medicapi_auth)

    # get symptoms as DataFrame
    symptoms_df = pd.read_json('./data/Symptoms.json')

    # get issue by id
    params = {'token': token, 'format': 'json', 'language': 'en-gb'}
    response = get_item('issues/{}/info'.format(issue_id), params=params, url=auth_data.medicapi_health)

    # dump issue information into file
    file = open('./data/Issue' + str(issue_id) + '.json', 'w')
    json.dump(response.json(), file)
    file.close()

    issue_symptoms = response.json()['PossibleSymptoms'].split(',')

    # get id of symptoms as list
    symptoms_id = []
    # change: added try/except for error handling
    for s in issue_symptoms:
        try:
            tmp_id = symptoms_df.loc[symptoms_df['Name'] == s].ID.item()
            if tmp_id not in symptoms:
                symptoms_id.append(tmp_id)
        except:
            e = sys.exc_info()[0]
            print("Error: {} for item '{}'".format(e, s))

    print('Symptoms IDs: {}'.format(symptoms_id))
    # for every symptom, get diagnosis and save issue ids as list
    issue_id_lst = []
    for act in symptoms_id:
        params = {'symptoms': str([act]), 'gender': 'male', 'year_of_birth': '25', 'token': token, 'format': 'json',
                  'language': 'en-gb'}

        response = get_item('diagnosis', params=params, url=auth_data.medicapi_health)
        data = response.json()

        for i in range(0, len(data)):
            tmp_id = data[i]['Issue']['ID']
            if tmp_id not in issue_id_lst:
                issue_id_lst.append(tmp_id)

        # write diagnose of symptom to file
        file = open('./data/Symptom' + str(act) + '.json', 'w')
        json.dump(data, file)
        file.close()

    return symptoms_id, issue_id_lst
