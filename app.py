import os
import openai

from openaikey import key

from botinstructions import *

from flask import Flask, request, render_template

app = Flask(__name__)
openai.api_key = key

class Chatbot:
    def __init__(self, system_context: str = case_2_system_instruction):
        self.model = "gpt-4"
        self.system_context = system_context
        self.messages = []

    def get_completion_from_messages(self, messages):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message['content']

    def chat(self, user_input, debug=False):
        messages = self.messages.copy()
        messages.append({"role": "system", "content": self.system_context})
        messages.append({"role": "user", "content": user_input})

        response = self.get_completion_from_messages(messages)
        if debug:
            print("Chat History")
            for message in messages:
                print(message)

        self.messages = messages
        self.messages.append({"role": "assistant", "content": response})

        return response

chatbot = Chatbot()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        chat_response = chatbot.chat(user_input)

        # Update the chat history
        chat_history = chatbot.messages.copy()
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": chat_response})

        return render_template('index.html', chat_history=chat_history)
    else:
        return render_template('index.html', chat_history=[])

if __name__ == '__main__':
    app.run()
