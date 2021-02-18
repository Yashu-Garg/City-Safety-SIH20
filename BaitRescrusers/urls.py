"""BaitRescrusers URL Configuration

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
from django.contrib import admin
from django.urls import path
from sih import views
from django.conf.urls import url,include
from rest_framework import routers
router=routers.DefaultRouter()
router.register(r'people',views.PeopleView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('register/',views.Register),
    path('login/',views.Login),
    path('logout/',views.Logout),
    path('save_location/',views.SaveLocation),
    path('test_up/',views.UpTest),
    path('maps/',views.Map),
    path('police/',views.Police),
    url(r"maps/(?P<user_id>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$",views.MainDistress,name='distress'),
    url(r"district/mob/(?P<dis>[a-zA-Z0-9_. ]*)/",views.AndroidDistrict,name='Androiddistrict'),
    url(r"district/(?P<dis>[a-zA-Z0-9_. ]*)/",views.District,name='district'),
    path('api/',include(router.urls)),
    path('test/',views.Test),
    path('trackandroidlocation/',views.trackandroidlocation),
    path('distresssignal/',views.distresssignal),
    path('mob/maps/',views.AndroidMaps)
]

# ^[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*)/$