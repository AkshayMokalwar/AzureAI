# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.comming_soon, name='home'),
    # path('home/', views.chatbot_view, name='chatbot'),
    # path('test2/', views.chatbot, name='chatbot'),
    path('get_bot_response/',views.get_bot_response)

]

# chatbot/forms.py