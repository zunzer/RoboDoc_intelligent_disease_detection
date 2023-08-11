from django.urls import path, include #added include

from . import views

'''
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
'''

app_name = 'common'
urlpatterns = [
    path('', views.home, name='home'),
    path('results', views.results, name='results'),
    path('query', views.query),                     # added path to query function in views.py
    path('add', views.add),                         # added path to add function in views.py
    path('delete', views.delete),                   # added path to delete function in views.py
    path('wiki', views.wiki),                       # added path to wiki function in views.py
    path('wiki_search', views.wiki_search),         # added path to wiki_search function in views.py
    path('',include("django.contrib.auth.urls")),   # use the django authentication system
    path('saveSymptoms', views.saveSysmptoms),      # added path to saveSymptoms function in views.py
    path('deleteSaved', views.deleteSavedSymptom),  # added path to saveSymptoms function in views.py
    # path('checkbox', views.checkbox),  # added path to checkbox function in views.py
    # path('submittedCheckbox', views.submittedCheckbox),  # added path to submitted function in views.py
]
