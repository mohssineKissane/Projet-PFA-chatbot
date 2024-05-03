from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from store.models import *
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
# Create your views here.

genai.configure(api_key="AIzaSyAvTlHoWMS3Cb3eI6_AhXDir460H9mQe0c")


def ask_question(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        user = request.user

        keywords = ["PC", "notebook", "ultrabook", "chromebook", "MacBook", "gaming laptop",
                    "workstation", "2-in-1 laptop", "convertible laptop", "business laptop",
                    "student laptop", "budget laptop", "high-performance laptop", "touchscreen laptop",
                    "lightweight laptop", "portable laptop", "gaming PC", "smartphone", "android phone",
                    "iPhone", "mobile phone", "cell phone", "budget smartphone", "flagship smartphone",
                    "mid-range smartphone", "premium smartphone", "Android flagship", "iOS device",
                    "smartphone accessories", "mobile accessories", "smartphone case", "screen protector",
                    "wireless charger", "Bluetooth headphones", "smartphone stand", "SIM card", "mobile data plan"
                    ]

        if any(keyword in text.lower() for keyword in keywords):
            try:
                model = genai.GenerativeModel("gemini-pro")
                chat = model.start_chat()
                response = chat.send_message(text)
                ChatBot.objects.create(
                    text_input=text, gemini_output=response.text, user=user)
                return JsonResponse({"data": {"text": response.text}})
            except Exception as e:
                print(f"Exception raised: {e}")
                return JsonResponse({"error": "An error occurred while processing your request."}, status=500)

        elif text.lower() in ["who are you", "what is your name"]:
            response_text = "I'm chotbot from TechConnect, your go-to destination for laptops and smartphones. I'm ready to assist you in finding the ideal device."

        elif text.lower() in ["my orders", "what are my orders", "give me my orders"]:
            orders = user.order_set.all() if user.is_authenticated else None
            if orders:
                response_text = "Here are your orders:\n\n"
                for order in orders:
                    response_text += f"Order ID: {order.id}\n\n"
                    response_text += f"Total Price: {order.total_price}\n\n"
                    response_text += f"Date: {order.created_at}\n\n\n"
            else:
                response_text = "You have no orders yet."
        elif "list of laptops" in text.lower():
            laptops = Product.objects.filter(category__name="Laptops")
            response_text = "Here are the available laptops:\n"
            for laptop in laptops:
                response_text += f"{laptop.name}: ${laptop.selling_price}\n"
        elif "list of smartphones" in text.lower():
            smartphones = Product.objects.filter(category__name="Smart Phones")
            response_text = "Here are the available smartphones:\n"
            for smartphone in smartphones:
                response_text += f"{smartphone.name}: ${smartphone.selling_price}\n"

        elif text.lower() in ["hello", "hi", ""]:
            response_text = "Hello! How can I assist you today?"

        elif text.lower() in ["exit", "bye"]:
            response_text = "Thank you for reaching out! Have a great day!"

        else:
            response_text = "I'm sorry, I can't answer that question."

        return JsonResponse({"data": {"text": response_text}})

    else:
        return HttpResponseRedirect(reverse("chat"))


@login_required
def chat(request):
    user = request.user
    chats = ChatBot.objects.filter(user=user)
    return render(request, "chat_bot.html", {"chat": chats})
