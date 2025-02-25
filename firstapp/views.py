from django.http import HttpResponse,JsonResponse
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
from django.views.decorators.csrf import csrf_exempt
import json

def get_azureopenai_response(msg):
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
    members=["Akshay ", "Gaurav"]
    data={
        "about":" We are the developers driving the technical backbone of our IT consulting and project initiatives. Our team brings deep expertise in a variety of technologies, allowing us to build robust and scalable solutions. We collaborate closely with our consulting team and clients to translate strategic visions into tangible, functional applications, ensuring every project meets and exceeds expectations.",
        "mission":"Our mission is to deliver exceptional quality services that consistently exceed customer expectations. We are dedicated to providing value-driven solutions that empower our clients to achieve their goals, fostering long-term partnerships built on trust and satisfaction.",
        "address":"xyz , city , state , pincode !!",
        "email":"sample@company.com",
        "phone":"xxx-xxx-xxxx",
        "service1":"Expert IT consulting to streamline operations and enhance your competitive edge. We analyze your current infrastructure and deliver tailored solutions for growth.",
        "service2":"We provide expert legal advisory, guiding clients through complex legal landscapes. Our alternative services offer innovative solutions, adapting to evolving legal and business needs.",
        "service3":"Ensuring your systems run smoothly with proactive maintenance and rapid support. We minimize downtime, maximizing your operational efficiency."
        }
    msg=msg.strip()
    if msg=='team':
        st="<h5> Our Team Members :</h5><ul>"
        for member in members:
            st+=f"<li><p>{member}</p></li>"
        st+="</ul>"
        return st
    elif msg in data:
        return f"<p>{data[msg]}</p>"
    else:
        return "<p> Logic will be added soon</p>"
    
        # return data[msg]+"""<button class="menu-option-button btn btn-outline-warning" data-value="mainmenu" data-key="submenu" fdprocessedid="wtlikr">Back to Main Menu</button>"""


def get_bot_response(request):
    messages = ChatMessage.objects.all() 
    if request.method == 'GET':
        data = {
            'message': 'This is a GET request response.',
            'status': 'success',
            'items': [
                {'id': 1, 'name': 'Item 1'},
                {'id': 2, 'name': 'Item 2'},
            ],
        }
        return JsonResponse(data)

    elif request.method == 'POST':
        message = request.POST.get('message')

        # print(message)
        if message:
            # Your bot logic here (replace with your actual implementation)
            # bot_response = f"bot: You said: {message}"  # Example response
            # ChatMessage.objects.create(sender='user', message=message).save() #save user msg

            bot_response = get_azureopenai_response(message)
            
            # if bot_response:
                # ChatMessage.objects.create(sender='bot', message=bot_response).save() #save bot responses
            
            return JsonResponse({'bot_response': bot_response})
        else:
            return JsonResponse({'error': 'Message not provided.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

def comming_soon(request):
    messages = ChatMessage.objects.all() 
    if request.method == 'POST':
        # form = ChatForm(request.POST)
        email = request.POST.get('email')
        print("#"*20)
        print(f" email : {email}")
        if email:  # Basic validation
            sub=Subscriber.objects.create(email=email,subscribed_at=datetime.now())  # Create a new Subscriber object
            sub.save()
            res={"msg":"Thank you for subscribing!","status":"success"}
            print(res)
            return render(request, 'chatbt/chatbot2_change.html',{'res':res})
        else:
            res={"msg":"Please enter a valid email.","status":"warning"}
            print(res)
            return render(request, 'chatbt/chatbot2_change.html',{'res':res})
    
    return render(request, 'chatbt/chatbot2_change.html',{'messages': messages})


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
        return render(request, 'chatbt/chatbot.html', {'messages': messages,'form': form, })
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['message']

        ChatMessage.objects.create(sender='user', message=user_message).save() #save user msg

        responses = generate_chatbot_response(user_message)

        for response in responses:
            ChatMessage.objects.create(sender='bot', message=response).save() #save bot responses
        # form = ChatForm()

        return redirect('/Qlaws/test2/')


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
