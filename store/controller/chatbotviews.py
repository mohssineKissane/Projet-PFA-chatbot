from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from store.models import *
from django.http import HttpResponseRedirect, JsonResponse
import google.generativeai as genai
from google.generativeai.types.generation_types import StopCandidateException
from django.db import connection


genai.configure(api_key="Enter your API kEY gimini")


def fetch_keywords():
    with connection.cursor() as cursor:
        cursor.execute("SELECT keyword, category FROM keywords")
        return cursor.fetchall()


@login_required
def ask_question(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        user = request.user

        # Fetch keywords from the database
        keywords = fetch_keywords()
        matched_keyword = None

        # Check if any keyword matches the user input
        for keyword, category in keywords:
            if keyword.lower() in text.lower():
                matched_keyword = category
                break

        common_queries = {
            "who are you": "I'm chatbot from TechConnect, your go-to destination for laptops and smartphones. I'm ready to assist you in finding the ideal device.",
            "what is your name": "I'm chatbot from TechConnect, your go-to destination for laptops and smartphones. I'm ready to assist you in finding the ideal device.",
            "hello": "Hello! How can I assist you today?",
            "hi": "Hello! How can I assist you today?",
            "exit": "Thank you for reaching out! Have a great day!",
            "bye": "Thank you for reaching out! Have a great day!"
        }

        if text.lower() in common_queries:
            response_text = common_queries[text.lower()]

        elif text.lower() in ["my orders", "what are my orders", "give me my orders"]:
            orders = user.order_set.all() if user.is_authenticated else None
            if orders:
                response_text = "Here are your orders:\n\n"
                for order in orders:
                    response_text += f"Order ID: {order.id}\n"
                    response_text += f"Total Price: ${order.total_price}\n"
                    response_text += f"Date: {order.created_at}\n\n"
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

        elif matched_keyword:
            try:
                model = genai.GenerativeModel("gemini-pro")
                chat = model.start_chat()
                response = chat.send_message(text)
                ChatBot.objects.create(
                    text_input=text, gemini_output=response.text, user=user)
                return JsonResponse({"data": {"text": response.text}})
            except StopCandidateException as e:
                print(f"StopCandidateException: {e}")
                response_text = "I'm having trouble processing your request right now. Please try again later."
            except Exception as e:
                print(f"Exception raised: {e}")
                response_text = "An error occurred while processing your request."

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
