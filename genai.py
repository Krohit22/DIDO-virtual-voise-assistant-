import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

def GenoAI(user_question):
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    persona ="""
        You are a Kiko assistant that will use the chat history and the image
        provided by the user to answer its questions. Your job is to answer
        questions and if user ask who are you or what's your name then just say "i am kiko made by krishna rajpurohit".

        Use few words on your answers. Go straight to the point. Do not use any
        emoticons or emojis.

        Be friendly and helpful. Show some personality.
        """ 
    response = chat.send_message( persona +"here is the question asked by the user: "+ user_question)
    
    return response.text