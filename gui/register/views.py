from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import models
from django.contrib.auth.models import User
from .models import UserSymptoms,Symptoms, Symptom_list
from src.util import *
from datetime import date,timedelta
from django.contrib.auth.decorators import login_required


import numpy as np
from django.db import models
# Create your views here.
User = get_user_model()

def register(request):                  #register new user
    if request.method =='POST':
        usertype = request.POST['radio']
        email = request.POST['email']
        first_name = request.POST['first_name']  # save all user information
        age = request.POST['age']
        country = request.POST['country']
        password1 = request.POST['password']
        if User.objects.filter(username=first_name).exists():   #check if name is unique
            if User.objects.filter(email=email).exists():       #check if email is unique
                context = {
                    'namemsg': "Name already taken!",
                    'emailmsg': "Email already taken!",
                    'usertype': usertype,
                    'age': age,
                    'country': country,
                }
            else:
                context = {
                    'namemsg': "Name already taken!",
                    'usertype': usertype,
                    'email': email,
                    'age': age,
                    'country': country
                }
            return render(request, "register/register.html", context)   #return page with error
        else:
            if User.objects.filter(email=email).exists():   #only email fild has error
                context = {
                    'emailmsg': "Email already taken!",
                    'usertype': usertype,
                    'name': first_name,
                    'age': age,
                    'country': country,
                }
                return render(request, "register/register.html", context)

        user = User.objects.create_user(username = first_name,email=email,
                                        usertype=usertype,
                                        age = age, country = country, password=password1)
        user.save()
        user = authenticate(request, username=first_name, password=password1)       # after creating, authenticate and login user
        if user is not None:
            login(request, user)
        return redirect("/saveSymptoms")
    return render(request,"register/register.html")

def redirecting(request):   #redirecting to logout page
    return render(request,"register/message.html", {"msg":"SUCCESSFULLY LOGGED OUT"})

@login_required(login_url='/login/')
def profile(request):   #link to profile page
    template_name= "register/profile.html"
    user = request.user  # get user from request
    user_name = user.username
    if user.usertype == 'doc':
        return render(request, template_name, {"msg": "", "Username: " : UserSymptoms.objects.all().values('username'), "Symptoms": Symptoms.objects.filter(ownuser__in=
                                                                                              UserSymptoms.objects.all()),
                                               "UserSymptoms": UserSymptoms.objects.all()})

    else:
        return render(request, template_name, {"msg": "","Symptoms": Symptoms.objects.filter(ownuser__in=
        UserSymptoms.objects.filter(username=user_name)), "UserSymptoms": UserSymptoms.objects.filter(username=user_name)})

@login_required(login_url='/login/')
def deleteUser(request):        #delete user
    msg =""
    user = request.user
    if user.username =="admin":
        msg ="YOU CANNOT DELETE THIS USER"              #avoid delete the admin
    if not user.username =="admin":
        Symptoms.objects.filter(ownuser__username=user.username).delete()  # remove all saved symptoms
        UserSymptoms.objects.filter(username=user.username).delete()
        user.delete()                                   #delete user
        msg="DELETED <br> <h4>" + user.username +"</h4> SUCCESFULLY"
        logout(request)                                 #logout user
        LogEntry.objects.all().delete()                 #used to clear log after delete user
    return render(request, "register/message.html", {"msg": msg})

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            login(request, form.user)
            user = request.user  # get user from request
            user_name = user.username
            model = UserSymptoms.objects.all()  # need to reload the model
            context = {
                'msg': "PASSWORD SUCCESSFULLY CHANGED!",
                'Symptoms': Symptoms.objects.filter(ownuser__in=model.filter(username=user_name)),
                'UserSymptoms': model.filter(username=user_name)
            }
            return render(request, 'register/profile.html', context)
        else:
            return redirect('/change-password')
    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'register/change_password.html', args)


def create_symptoms_in_past(request, days, symptom):         #create symptom "symptom" with diagnosis "symptom" exactly num days before today
    user = request.user  #      ONLY TO CREATE VIRTUAL TESTDATA
    user_name = user.username
    userwithsymp = UserSymptoms.objects.create(username=user_name, symp_date=date.today() - timedelta(days=days),
                                               diagnosis=symptom)
    userwithsymp.save()
    s = Symptoms(Name=symptom, ownuser=userwithsymp)
    s.save()

@login_required(login_url='/login/')
def change_userinfo(request):
    if request.method == 'POST':
        if ("country") in request.POST:
            country = request.POST["country"]
            request.user.country = country
            request.user.save()
        if ("age") in request.POST:
            age = request.POST["age"]
            request.user.age = age
            request.user.save()
        return profile(request)
    else:
        return render(request, 'register/change_userinfo.html', {"selected":request.user.country})


def diseasesStat(request):  # link to diseases statistic page
    template_name = "register/diseasesStat.html"    #use django aggregation, order by name and count names. returns: list[name,count]...
    resultDisea = UserSymptoms.objects.values('diagnosis').order_by('diagnosis').annotate(count=Count('diagnosis'))

    ####Symptoms.objects.all().delete()    # #CLEAR SAVED SYMPTOMS ONLY FOR TESTING
    #####UserSymptoms.objects.all().delete()

    return render(request, template_name, {'dis': resultDisea})

def symptomsStat(request):  # link to symptom statistics page
    template_name = "register/symptomStat.html"
    resultSymp = Symptoms.objects.values('Name').order_by('Name').annotate(count=Count('Name'))
    return render(request, template_name,{'symp': resultSymp}) #pass list to statistics page and crate chart


def disStatsprivate(request):  # link to diseases statistic page
    user_name = request.user.username
    template_name = "register/disStatsprivate.html"    #use django aggregation, order by name and count names. returns: list[name,count]...
    resultDisea = UserSymptoms.objects.filter(username=user_name).values('diagnosis').order_by('diagnosis').annotate(count=Count('diagnosis'))
    print(resultDisea)
    ####Symptoms.objects.all().delete()    #uncomment if you want to clear statistics and databases for test purposes
    #####UserSymptoms.objects.all().delete()

    return render(request, template_name, {'dis': resultDisea})

def sysStatsprivate(request):  # link to symptom statistics page
    template_name = "register/sysStatsprivate.html"
    user_name = request.user.username
    #resultSymp = Symptoms.objects.filter(user_name=user_name).values('Name').annotate(count=Count('Name'))
    res = Symptoms.objects.filter(ownuser__username=user_name).values('Name').annotate(count=Count('Name'))
    #resultSymp = Symptoms.objects.values('Name').order_by('Name').annotate(count=Count('Name'))
    print(res)
    #trysymp = UserSymptoms.objects.values('id','symp_date').intersection(Symptoms.objects.values('ownuser__symp_date'))
    #print(trysymp)

    return render(request, template_name,{'symp': res}) #pass list to statistics page and crate chart


def ageStats(request):
    template_name = "register/ageStats.html"    #use django aggregation, order by name and owner name. returns: list[name,owner]...
    query= Symptoms.objects.values_list("Name", "ownuser__username")
    agesymptoms= []
    for i in query:
        if User.objects.filter(username=i[1]).exists():
            age = User.objects.values('age').filter(username = i[1])
            elem = [i[0]]
            elem.append(int(age[0]["age"]))
            agesymptoms.append(elem)            #replace each owner with owners age

    colors = ["color: #03cafc", "color: #0341fc", "color:#0a68ff", "color:#044bbd", "color:#032152"]    #colors for each bar
    totwenty, tofourty, tosixty, toeighty, toonehundred = [],[],[],[],[]  #arrays for each age group

    for i in agesymptoms:        #insert symptoms in right age group
        if i[1] <= 20:
            totwenty.append(i[0])
        elif i[1] <= 40:
            tofourty.append(i[0])
        elif i[1] <= 60:
            tosixty.append(i[0])
        elif i[1] <= 80:
            toeighty.append(i[0])
        else:
            toonehundred.append(i[0])
    a=[find_most_common_symptom_per_age(totwenty)]  #find the most common symptom in each age group
    a.append(find_most_common_symptom_per_age(tofourty))
    a.append(find_most_common_symptom_per_age(tosixty))
    a.append(find_most_common_symptom_per_age(toeighty))
    a.append(find_most_common_symptom_per_age(toonehundred))

    data =  []      # give each symptom a color of the color array
    while a:
        i = a.pop(0)
        data.append(i)
        if(len(i) == 2):
            color = colors.pop(0)
            i.append(color)
            for j in a:         #draw bars with same symptoms with the same color
                if (i[0] == j[0]):
                    j.append(color)

    return render(request, template_name, {'data':data})


def mapStats(request):
    a = list(Symptoms.objects.values_list('Name', 'ownuser__username'))  # get Sympotoms name and owner
    res = []
    for i in a:
        if User.objects.filter(username=i[1]).exists():
            country = User.objects.values('country').filter(username = i[1])     #replace owner in list with its country
            elem = [i[0]]
            elem.append(str(country[0]["country"]))
            res.append(elem)

    counterRes = count_symptoms_per_country(res)        #count how number of each symptom each country has
    commonRes  = find_most_common_symptom_per_country(counterRes)   #for each country search for the most common
    context = {
        "country": commonRes,    # country needs to be called with {{country| save}} to allow all ascii chars
    }
    template_name = "register/mapStats.html"
    return render(request, template_name, context)

def timeStats(request):
    #create_symptoms_in_past(request, 1, "Fever")

    template_name = "register/timeStat.html"
    symptomsanddates= Symptoms.objects.values_list('ownuser__symp_date','Name').filter(ownuser__username = request.user.username)
    qset = symptomsanddates.order_by('ownuser__symp_date').annotate(Count('Name'), Count('ownuser__symp_date'))

    symptoms = UserSymptoms.objects.values_list('symptoms__Name').filter(username = request.user.username).order_by('symptoms__Name').distinct()

    symparray = []              #array with symptoms
    if(len(symptoms) == 0 ):       #no symptoms
        return render(request, template_name, {'msg' : "NO SYMPTOMS TO SHOW"})
    for i in range(0,len(symptoms)):
        symparray.append(symptoms[i][0])    #fill array

    date1 = qset[0][0]              #get earliest symptom date
    date2 = qset[len(qset)-1][0]    #get last entered symptom date
    print(date1, date2)
    i = 0
    datearray = []
    while ((date.today()- timedelta(days=i))+ timedelta(days=1)>=date1):
        datearray.append(f"{date.today() - timedelta(days=i):%d.%m.%Y}")   #generate a date array from first-1 date to today
        i=i+1
    datearray.reverse()     #order the array from first to last
    b = np.zeros((len(datearray), len(symptoms)+1), dtype=object)   #create data matrice with zeros
    for k in range (0,len(datearray)):
        b[k][0] = datearray[k]      #initialize first row only with dates

    count = 1
    for l in qset:      #iterate trough symptoms
        for i in symparray:     #search the row that belongs to the symptom
            if i == l[1] :
                dateElem = (l[0] - date1).days+1    # calculate date for the element
                b[dateElem][count] = l[2]           #insert count
            count += 1                        #next row
        count = 1                                   #start with first row

    context = {
        'symptoms' : symparray,                 #data needs to be called with {{data| save}} to allow all ascii chars
        'data' : np.array2string(b, separator=', ').replace("\'","\""),     #convert array to chart compatible string
    }
    return render(request,template_name,context)
