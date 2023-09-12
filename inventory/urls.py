from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.createBox,name="Create"),
    path('listBoxes',views.listBoxes,name="ListBox"),
    path('listMyBoxes',views.listMyBoxes,name="ListMyBox"),
    path('createBoxes',views.createBox,name="CreateBox"),
    path('updateBoxes',views.updateBox,name="UpdateBox"),
    path('deleteBoxes',views.deleteBox,name="DeleteBox"),
    path('registerUser',views.userAuthorization,name="RegisterUser"),
]
