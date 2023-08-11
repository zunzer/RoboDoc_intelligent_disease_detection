from django.db import models
import json
# Create your models here.


class Issue:

    Portion = 0

    def __init__(self, IssueId):
        name = '../database/Diseases/Issue{}.json'.format(IssueId)
        with open(name) as json_file:
            data = json.load(json_file)
            #   Keys = ['Description', 'DescriptionShort', 'MedicalCondition', 'Name', 'PossibleSymptoms', 'ProfName', 'Synonyms', 'TreatmentDescription']
            self.Description = data['Description']
            self.DescriptionShort = data['DescriptionShort']
            self.MedicalCondition = data['MedicalCondition']
            self.Name = data['Name']
            symptom_str = data['PossibleSymptoms']
            self.PossibleSymptoms = symptom_str.replace(',', ', ').replace(',  ', ', ') # parse symptoms, so they are properly separated
            self.TreatmentDescription = data['TreatmentDescription']


class Symptom_list(models.Model):
    Name = models.CharField(max_length=200)

    class Meta:
        db_table = 'symptom_list'


class UserSymptoms(models.Model):
    username = models.CharField(max_length=200)
    symp_date = models.DateField()
    diagnosis = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Symptoms(models.Model):
    Name = models.CharField(max_length=200)
    ownuser = models.ForeignKey(UserSymptoms,on_delete=models.CASCADE)

    class Meta:
        ordering = ['Name']

    def __str__(self):
        return self.Name

'''
    how to work with this ? 

            -> get Issue:      myissue = issue(ID)

                now get Infos for Issue:

                    myissue.Description -> str: Description  ...

                    ...
    minimal ~¹²³

'''