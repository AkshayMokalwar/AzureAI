from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import ChatForm
from .models import Subscriber , ChatMessage
 # Import your Subscriber model
from datetime import datetime 
import openai
from django.conf import settings
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def comming_soon(request):
    response_text = ""
    if request.method == 'POST':
        # form = ChatForm(request.POST)
        response_text ="HI"
        email = request.POST.get('email')
        print("#"*20)
        print(f" email : {email}")
        if email:  # Basic validation
            sub=Subscriber.objects.create(email=email,subscribed_at=datetime.now())  # Create a new Subscriber object
            sub.save()

            return HttpResponse("Thank you for subscribing!") # or redirect, or render a success page
        else:
            return HttpResponse("Please enter a valid email.")
        
    return render(request, 'chatbt/chatbot2.html')


def generate_chatbot_response(user_message):
    user_message = user_message.lower()
    if "hello" in user_message:
        return ["Hi there!", "How can I help you?"]
    elif "how are you" in user_message:
        return ["I'm doing well, thank you!", "How about you?"]
    else:
        return ["I'm not sure I understand.", "Could you please rephrase?"]
    

def chatbot(request):
    if request.method == 'GET':
        messages = ChatMessage.objects.all() #Get all messages
        form = ChatForm()
        return render(request, 'chatbt/chatbot3.html', {'messages': messages,'form': form, })
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['message']

        ChatMessage.objects.create(sender='user', message=user_message).save() #save user msg

        responses = generate_chatbot_response(user_message)

        for response in responses:
            ChatMessage.objects.create(sender='bot', message=response).save() #save bot responses
        # form = ChatForm()

        return redirect('/chatbot/test2/')


def chatbot_view(request):
    response_text = ""
    if request.method == 'POST':
        form = ChatForm(request.POST)
        
        if form.is_valid():

            message = form.cleaned_data['message']
            print(f" !!!!!!!!!!!!!!!!!! message  : {message}")
            response_text +=f"chatbot : {message}"

            # openai.api_type = "azure"
            # openai.api_base = settings.AZURE_OPENAI_ENDPOINT
            # openai.api_version = "2023-05-15"
            # openai.api_key = settings.AZURE_OPENAI_API_KEY

            # llm = AzureOpenAI(
            #     deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            #     model_name="gpt-3.5-turbo",
            #     openai_api_key=settings.AZURE_OPENAI_API_KEY,
            #     openai_api_base=settings.AZURE_OPENAI_ENDPOINT,
            #     openai_api_type="azure",
            #     openai_api_version = "2023-05-15",
            # )

            # prompt = PromptTemplate(
            #     input_variables=["user_input"],
            #     template="You are a helpful assistant. Answer the following question: {user_input}",
            # )

            # chain = LLMChain(llm=llm, prompt=prompt)

            # response_text = chain.run(message)

    else:
        form = ChatForm()
    return render(request, 'chatbt/chatbot3.html', {'form': form, 'response': response_text})
