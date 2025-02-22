from django.http import HttpResponse
from django.shortcuts import render
from .forms import ChatForm
from .models import Subscriber  # Import your Subscriber model

import openai
from django.conf import settings
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def coming_soon(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(f" !!!!!!!!!!!!!!!!!! email  : {email}")

        if email:  # Basic validation
            Subscriber.objects.create(email=email)  # Create a new Subscriber object
            return HttpResponse("Thank you for subscribing!") # or redirect, or render a success page
        else:
            return HttpResponse("Please enter a valid email.")

    # return render(request, 'your_app/coming_soon.html') # Render your template

def chatbot_view(request):
    response_text = ""
    if request.method == 'POST':
        # form = ChatForm(request.POST)
        response_text ="HI"
        email = request.POST.get('email')
        print("#"*20)
        print(f" email : {email}")
        if email:  # Basic validation
            sub=Subscriber.objects.create(email=email)  # Create a new Subscriber object
            sub.save()

            return HttpResponse("Thank you for subscribing!") # or redirect, or render a success page
        else:
            return HttpResponse("Please enter a valid email.")
        
        if form.is_valid():
            message = form.cleaned_data['message']
            print(f" !!!!!!!!!!!!!!!!!! message  : {message}")
            openai.api_type = "azure"
            openai.api_base = settings.AZURE_OPENAI_ENDPOINT
            openai.api_version = "2023-05-15"
            openai.api_key = settings.AZURE_OPENAI_API_KEY

            llm = AzureOpenAI(
                deployment_name=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                model_name="gpt-3.5-turbo",
                openai_api_key=settings.AZURE_OPENAI_API_KEY,
                openai_api_base=settings.AZURE_OPENAI_ENDPOINT,
                openai_api_type="azure",
                openai_api_version = "2023-05-15",
            )

            prompt = PromptTemplate(
                input_variables=["user_input"],
                template="You are a helpful assistant. Answer the following question: {user_input}",
            )

            chain = LLMChain(llm=llm, prompt=prompt)

            response_text = chain.run(message)

    # else:
        # form = ChatForm()
    return render(request, 'chatbt/chatbot2.html')

    return render(request, 'chatbt/chatbot3.html', {'form': form, 'response': response_text})
