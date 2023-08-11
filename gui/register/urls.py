"""gui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
"""
from django.urls import path
from register import views as registerview
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", registerview.register),   #added register, deleteUser and redirectig
    path("deleteUser/", registerview.deleteUser),
    path("profile/", registerview.profile),
    path("diseasesStat/", registerview.diseasesStat),
    path("disStatsprivate/", registerview.disStatsprivate),
    path("symptomsStat/", registerview.symptomsStat),
    path("sysStatsprivate/", registerview.sysStatsprivate),
    path("timeStats/", registerview.timeStats),
    path("redirecting/", registerview.redirecting),
    url(r'^change-password/$', registerview.change_password, name='change_password'),
    url("change-userinfo/", registerview.change_userinfo),
    url("ageStats/", registerview.ageStats),
    path("mapStats/", registerview.mapStats),
]


