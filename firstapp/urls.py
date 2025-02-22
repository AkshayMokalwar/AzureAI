# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.comming_soon, name='chatbot'),
    # path('home/', views.chatbot_view, name='chatbot'),
    path('test2/', views.chatbot, name='chatbot'),

]

# chatbot/forms.py