#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:40:00 2019

@author: eltonwang
"""
import re

import uuid
import dialogflow_v2beta1 as dialogflow
from google.oauth2 import service_account


from flask import Flask
from flask import json
from flask import Response
from flask import request
from flask import jsonify


def chat_bot(_text):
    input_text = _text
    project_id = 'bot-0527'
    session_id = uuid.uuid1()

    credentials = service_account.Credentials.from_service_account_file('bot-0527-8f10a38bf932.json')

    session_client = dialogflow.SessionsClient(credentials = credentials)
    session_path = session_client.session_path(project_id, session_id)

    text_input = dialogflow.types.TextInput(text=input_text, language_code='zh-TW')
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session_path, query_input=query_input)

    return(response.query_result.fulfillment_text)


app = Flask(__name__)

@app.route("/" , methods=['POST'])
def hello():
    data = json.loads(request.get_data())
    text = re.sub('\<at\>.*\</at\>','',data['text'])
    print (text)
    response = chat_bot(text)
    t =jsonify( {"type": "message",
         "text": response})
    return t



if __name__ == "__main__":
    app.run()