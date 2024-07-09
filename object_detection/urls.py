from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('obj_dtc', views.obj_dtc, name='obj_dtc')
    
]


