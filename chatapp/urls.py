
# from django.contrib import admin
# from django.urls import path, include
# from chatapp.views import *
# from django.conf import settings


# urlpatterns = [
    
#     path("", home,name="home"),
    
# ]

# urls.py
from django.urls import path
from .views import chat_view,answer_view,answer_from_doc_view,chat_doc_view

urlpatterns = [
    path('chat/', chat_view, name='chat'),
    path('chat_doc/', chat_doc_view, name='chatdoc'),
    path('answer/', answer_view, name='answer'),
    path('answer_doc/', answer_from_doc_view, name='answerfromdoc'),
    
]