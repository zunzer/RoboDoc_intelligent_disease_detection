from django.shortcuts import render
from django.template.defaulttags import register

import sys
import json
import pandas as pd

from .models import Issue
from datetime import date

sys.path.append("..")   # added to fix import error on linux
from machine_learning.robo_doctor import RoboDoctor
from machine_learning.symptom_suggestor import SymptomSuggestor
from src.util import don_t_show_selected_symptoms
from django.contrib.auth.decorators import login_required  # make a login required for save
from .models import UserSymptoms, Symptoms, Symptom_list
from register.models import myUser
# Create your views here.

# not able to dump int64
# https://stackoverflow.com/questions/11942364/typeerror-integer-is-not-json-serializable-when-serializing-json-in-python
# convert numpy dtype to python dtype
# https://stackoverflow.com/questions/9452775/converting-numpy-dtypes-to-native-python-types/11389998#11389998
@register.filter
def dumpj(value):
    return json.dumps(value)

# path to symptoms.csv
url = '../database/Symptoms/Symptoms.csv'
data = pd.DataFrame()

# initialize symptom suggester
suggester = SymptomSuggestor()

# intialize robodoc
robodoc = RoboDoctor()


# function called with localhost
def home(request):
    # load csv path and read as DataFrame
    global data
    data = pd.DataFrame(Symptom_list.objects.all().values())
    data.columns = ['ID', 'Name']
    data.sort_values(by='Name', inplace=True)

    # open page RoboDoc.html
    template_name = 'common/RoboDoc.html'
    # list of symptom names and empty symptoms dict as context
    context = {
        'data': data,
        'symptoms': {'ID': [], 'Name': []},
        'valid': True
    }

    return render(request, template_name, context=context)


# function to add selected symptom to list
def add(request):
    if request.method == "POST":
        # get the selected symptom user wants to add
        selected = request.POST['selected']
        # load symptoms dict from json
        symptoms = json.loads(request.POST['symptoms'])
    else:
        symptoms = {'ID': [], 'Name': []}
        selected = ""

    # load csv as DataFrame
    global data

    # if user input exists in data, add to symptoms list
    try:
        tmp = data.loc[data['Name'] == selected]
        symptoms['ID'].append(tmp['ID'].values[0].item())   # .item() for np.int64 -> int
        symptoms['Name'].append(tmp['Name'].values[0])
        valid = True
    except IndexError:
        # set to false to show error message
        valid = False

    # remove selected symptoms from data to avoid multi selecting
    if valid:
        data = don_t_show_selected_symptoms(symptoms['ID'], data)

    # get suggested symptoms
    global suggester
    suggested_ids = suggester.suggest(symptoms['ID'])

    suggested = []
    for s in suggested_ids:
        # after a while the same symptoms are suggested, regardless if picked already -> try block to catch this case
        try:
            suggested.append(data.loc[data['ID'] == s]['Name'].values[0])
        except IndexError:
            continue

    template_name = 'common/RoboDoc.html'
    context = {
        'data': data,
        'symptoms': symptoms,
        'suggested': suggested,
        'valid': valid
    }

    return render(request, template_name, context=context)


# function called to delete element from symptom list
def delete(request):
    global data
    if request.method == "POST":
        # get the selected symptom user wants to delete
        selected = request.POST['selected']
        # load symptoms dict from json
        symptoms = json.loads(request.POST['symptoms'])
    else:
        symptoms = {'ID': [], 'Name': []}
        selected = ""
    print(selected,"\n here my selected\n")
    # remove selected symptom
    if selected in symptoms['Name']:
        # get index to remove ID
        idx = symptoms['Name'].index(selected)
        p_id= symptoms['ID'].pop(idx)
        p_nam = symptoms['Name'].pop(idx)
        popped = pd.DataFrame([[p_id,p_nam]],columns=['ID','Name'])
        data = pd.concat([data,popped])
    valid = True

    for s in symptoms:
        print("this is dont show selected symp :" ,s)
        data.drop(data.loc[data['ID'] == s].index, inplace=True)

    # get suggested symptoms
    # TODO: fix problem with duplicate suggested symptoms when deleting FIXED ?
    global suggester
    suggested_ids = suggester.suggest(symptoms['ID'])

    suggested = []
    for s in suggested_ids:
        # after a while the same symptoms are suggested, regardless if picked already -> try block to catch this case
        try:
            suggested.append(data.loc[data['ID'] == s]['Name'].values[0])
        except IndexError:
            continue

    template_name = 'common/RoboDoc.html'
    context = {
        'data': data,
        'symptoms': symptoms,
        'suggested': suggested,
        'valid': valid
    }
    return render(request, template_name, context=context)

# builds an issue object from Issue ID and Probability
def build_issue(i):
    portion = int(round(i[1] * 10)) # portion means x out of 10
    # round results, so 10 out of 10 and 0 out of 10 are never displayed
    if portion < 1:
        portion = 1
    if portion == 10:
        portion = 9
    disease_id = i[0]
    try:
        # create issue object from disease id
        issue = Issue(disease_id)
        issue.Portion = portion
    except FileNotFoundError:
        issue = dict()
        issue['Description'] = 'No Description yet.'
        issue['DescriptionShort'] = 'No Short Description yet.'
        issue['MedicalCondition'] = 'No Medical Conditions yet.'
        issue['Name'] = 'Disease with ID {}'.format(disease_id)
        issue['PossibleSymptoms'] = 'No Possible Symptoms yet.'
        issue['TreatmentDescription'] = 'No TreatmentDescription yet.'
        issue['Portion'] = portion
    return issue

def results(request):
    # load symptoms dict from json
    symptoms = json.loads(request.POST['symptoms'])

    # create RoboDoctor object
    global robodoc
    # get probability for all diseases as dictionary
    dis_prob = robodoc.predict_single(symptoms['ID'])
    # sort diseases by probability
    dis_prob = sorted(dis_prob.items(), key=lambda x: x[1])

    # three most probable diseases are displayed with their portion out of 10 people
    issue1 = build_issue(dis_prob[-1])
    issue2 = build_issue(dis_prob[-2])
    issue3 = build_issue(dis_prob[-3])

    if request.user.is_authenticated:
        userr = myUser.objects.get(username=request.user.username)
        type = userr.usertype
    else:
        type = 'def'

    template_name = 'common/multiple_results.html'
    context = {
        'issue1': issue1,
        'issue2': issue2,
        'issue3': issue3,
        'selected': symptoms['Name'],
        'type': type
    }
    response = render(request, template_name, context=context)  # save all entered symptoms and results in cookies
    response.set_cookie('issue1', str(issue1.Name))  # needed cookies to make them available after login
    response.set_cookie('issue2', str(issue2.Name))
    response.set_cookie('issue3', str(issue3.Name))
    response.set_cookie('selectedSymptoms',
                        str(symptoms['Name']))  # session not working because it is cleared after login
    return response

def query(request):  # got query request
    template_name = 'common/exe.html'  # query request with search bar
    searchinput = request.GET['q']

    # get diseases
    with open('../database/diseases_100_db.json', 'r') as file:
        data = file.read()
    obj = json.loads(data)
    diseases = []
    id = []
    for item in obj:
        for attribute, value in item.items():
            if attribute == 'name':
                diseases.append(value)
            if attribute == 'id':
                id.append(value)

    # get symptoms
    with open('common/fixtures/symptomlist.json', 'r') as file:
        data2 = file.read()
    obj2 = json.loads(data2)
    symptoms = []
    symptoms_id = []
    for item in obj2:
        for attribute, value in item.items():
            if attribute == 'pk':
                symptoms_id.append(value)
            if attribute == 'fields':
                symptoms.append(value['Name'])

    # check if search is a disease or a symptom
    issue = -1
    valid = False
    symptom = False
    disease = False
    count = 0
    for d in diseases:
        if d.lower() == searchinput.lower():
            issue = Issue(id[count])
            valid = True
            disease = True
            break
        count = count + 1

    symptom_name = ''
    symptom_id = -1
    count2 = 0
    for s in symptoms:
        if s.lower() == searchinput.lower():
            valid = True
            symptom = True
            symptom_name = s
            symptom_id = symptoms_id[count2]
            break
        count2 = count2 + 1

    # get matching diseases for symptom
    matching_diseases = []
    current_name = ''
    for item in obj:
        for attribute, value in item.items():
            if attribute == 'name':
                current_name = value
            if attribute == 'symptoms':
                for dic in value:
                    for key in dic:
                        if key == 'id':
                            if dic[key] == symptom_id:
                                matching_diseases.append(current_name)

    matching_diseases.sort()
    matching_diseases = list(dict.fromkeys(matching_diseases))

    return render(request, template_name, {'valid': valid, 'disease': disease, 'symptom': symptom, 'issue': issue,
                                           'symptom_name': symptom_name, 'matching_diseases': matching_diseases})


@login_required(login_url='/login/')
def saveSysmptoms(request) :
    userr = myUser.objects.get(username=request.user.username)
    type = userr.usertype
    if type != 'doc':
        if ('selectedSymptoms' in request.COOKIES.keys() and 'selectedIssue' in request.COOKIES.keys()):
            selectedsymptoms = request.COOKIES.get('selectedSymptoms').replace("'", "").strip('[').strip(']').split(', ')  # symptoms array, maybe you need to convert it

            selectedIssue = request.COOKIES.get('selectedIssue')
            issue = request.COOKIES.get(selectedIssue)

            user = request.user  # get user from request
            user_name = user.username
            userwithsymp = UserSymptoms.objects.create(username=user_name, symp_date=date.today(), diagnosis=issue )
            userwithsymp.save()

            for sym in selectedsymptoms:
                s = Symptoms(Name=sym, ownuser=userwithsymp)
                s.save()
            msg = "SYMPTOMS SAVED IN HISTORY"
            model = UserSymptoms.objects.all()  # need to reload the model
            context = {
                'msg': msg,
                'Symptoms': Symptoms.objects.filter(ownuser__in=model.filter(username=user_name)),
                'UserSymptoms': model.filter(username=user_name)
            }
            template_name = 'register/profile.html'
            response = render(request, template_name, context)
            return response
        else:
            return home(request)

    else:
        return home(request)    # if login and no symptoms in cookies, redirect user to home


def deleteSavedSymptom(request) : #
    template_name = 'register/profile.html'
    user = request.user  # get user from request
    user_name = user.username
    selected = request.POST['selected']  # receive the id of UserSymptoms entry that should be deleted

    Symptoms.objects.filter(ownuser=selected).delete()  #delete all connected Symptoms (1 to many relationship)
    UserSymptoms.objects.get(id=selected).delete()      #delete selected main entry

    model = UserSymptoms.objects.all()  #reload model
    context = {
        'msg': "DELETED ENTRY",
        'Symptoms': Symptoms.objects.filter(ownuser__in=model.filter(username=user_name)),  #only filter for may own symptoms
        'UserSymptoms': model.filter(username=user_name) #only filter for my own diseases
    }
    return render(request, template_name, context)


def wiki(request):
    template_name = 'common/wiki.html'

    with open('../database/diseases_100_db.json', 'r') as file:
        data = file.read()

    obj = json.loads(data)
    disease = []
    for symptom in obj:
        for attribute, value in symptom.items():
            if attribute == 'name':
                disease.append(value)

    disease.sort()

    return render(request, template_name, {'issues': disease, 'valid': True})


def wiki_search(request):
    template_name = 'common/wiki.html'
    selected = ""
    if request.method == "GET": #CHANGED TO GET REQUEST to make it availiable for profile links
        selected = request.GET['selected']  # get the selected symptom user wants to add

    with open('../database/diseases_100_db.json', 'r') as file:
        data = file.read()

    obj = json.loads(data)
    disease = []
    id = []
    for symptom in obj:
        for attribute, value in symptom.items():
            if attribute == 'name':
                disease.append(value)
            if attribute == 'id':
                id.append(value)

    # check if user input is valid
    valid = False
    issue = Issue(11)
    for j in range(len(disease)):
        if selected == disease[j]:
            valid = True
            issue = Issue(id[j])
            break

    disease.sort()

    return render(request, template_name, {'issues': disease, 'issue': issue, 'valid': valid})


# def checkbox(request):  # open checkbox page
#     template_name = 'common/checkbox.html'
#     with open(url) as csvdatei:
#         csv_reader_object = csv.reader(csvdatei)
#         data = list(csv_reader_object)  # get list from csv: [[SymptomNum1, Symptom1],[SymptomNum2,Symptom2]...]
#     data.pop(0)
#     return render(request, template_name, {'data': data})


# def submittedCheckbox(request):  # function called by click on submit button
#     template_name = 'common/exe.html'
#     with open(url) as csvdatei:
#         csv_reader_object = csv.reader(csvdatei)
#         symptomcsv = list(csv_reader_object)
#     symptomcsv.pop(0)
#
#     symptombin = []  # create binary symptom array, set every symptom to 0
#     for i in range(0, len(symptomcsv)):
#         symptombin.append(0)
#
#     for i in range(0, len(symptomcsv)):
#         if ('symptom' + symptomcsv[i][0]) in request.POST:  # change value from 0 to 1 if user selected symptom
#             if (request.POST['symptom' + str(symptomcsv[i][0])] == "on"):
#                 symptombin[i] = 1
#         i += 1
#
#     # symptom array entry = 1: symptom was selected, 0 if not
#     print(symptombin)
#     returnmsg = "SORRY, NOT IMPLEMENTED"
#     # TODO, calculate result :-)
#     return render(request, template_name, {'returnmsg': returnmsg})  # return message to exe.html
