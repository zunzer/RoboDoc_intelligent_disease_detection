import json

from rest_framework.views import APIView
from rest_framework.response import Response

from common.views import suggester, robodoc
from common.models import Issue, UserSymptoms, Symptoms, Symptom_list

# Create your views here.


class SymptomsView(APIView):

    def get(self, request, *args, **kwargs):
        data = Symptom_list.objects.all().values()
        return Response(data)


class DiagnosisView(APIView):

    def get(self, request, *args, **kwargs):
        # get submitted symptoms
        symptoms = json.loads(request.GET['symptoms'])

        # make single prediction based on submitted symptoms
        dis_prob = robodoc.predict_single(symptoms)
        dis_prob = sorted(dis_prob.items(), key=lambda x: x[1])
        # get disease with highest prob
        diseases = dis_prob[-1]

        issue = Issue(diseases[0])
        issue_json = {
            'Name': issue.Name,
            'Description': issue.Description,
            'DescriptionShort': issue.DescriptionShort,
            'PossibleSymptoms': issue.PossibleSymptoms,
            'MedicalCondition': issue.MedicalCondition,
            'TreatmentDescription': issue.TreatmentDescription,
        }
        return Response(issue_json)
