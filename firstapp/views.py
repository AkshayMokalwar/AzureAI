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
    return "reply  "+msg

def get_bot_response(request):
    messages = ChatMessage.objects.all() 
    print(f" last msg  : {messages}")
    # Get the user's IP address
    
    if request.method == 'GET':
        ip_address = request.session.session_key

        # # In case of proxies, you might need to check HTTP_X_FORWARDED_FOR
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip_address = x_forwarded_for.split(',')[0]  # Get the first IP from the list
        # else:
        #     ip_address = request.META.get('REMOTE_ADDR')
      
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
            
            ChatMessage.objects.create(sender='user', message=message).save() #save user msg
            if '1'  in message or message.strip()=='1':
                bot_response="""<ol type="I">
                                    <li>Company Details</li>
                                    <li>Our Services</li>
                                    <li>Contact Us</li>
                                    <li>Back to Main Menu</li>
                                </ol>"""
            elif '2'  in message or message.strip()=='2':
                    bot_response="""<ol type="I">
                                        <li>Company Details</li>
                                        <li>Our Services</li>
                                        <li>Contact Us</li>
                                        <li>Back to Main Menu</li>
                                    </ol>"""
            else:
                bot_response = get_azureopenai_response(message)
            
            if bot_response:
                ChatMessage.objects.create(sender='bot', message=bot_response).save() #save bot responses
            
            return JsonResponse({'bot_response': f"bot : {bot_response}"})
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
            success_msg="Thank you for subscribing!"# or redirect, or render a success page
            render(request, 'chatbt/chatbot2_change.html',{'s_msg':success_msg})
        else:
            failed_msg="Please enter a valid email."
            render(request, 'chatbt/chatbot2_change.html',{'f_msg':failed_msg})
    
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
