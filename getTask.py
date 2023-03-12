import json
import os
from flask import jsonify
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

openai.organization = os.getenv("OPENAI_ORGANIZATION")
openai.api_key = os.getenv("OPENAI_API_KEY")
COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"
task_list = []
notification_list = []
meetings_list = []

#create dictionary for todo
#create dictionary for notification
#create dictionary for meetings

def get_tasks():
    final_response = {
            'tasks' : task_list
    }
    final_res = json.dumps(final_response)
    return json.loads(final_res)


def get_notifications():
    final_response = {
            'notifications' : notification_list
    }
    final_res = json.dumps(final_response)
    return json.loads(final_res)

def get_events():
    final_response = {
            'events' : meetings_list
    }
    final_res = json.dumps(final_response)
    return json.loads(final_res)

    
#function to identify task, meeting invite, Financial deatils notification, others
def identify_type(email_content):
    question_prompt = "Classify the given email to the given types : task, events, meeting, notification and others. output only the type "
    prompt = email_content + question_prompt
    response = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        model=COMPLETIONS_MODEL
    )["choices"][0]["text"].strip(" \n")
    print(response)
    return response
# function to summarize email


#function to identify task
def identify_task(email_content):
    question_prompt = "Identify the task given in the  email and output the task and output format should be task: summarize the task in a sentance with all details, date: the date in mm/dd/yyyy format, details: details, Sender: Sender "
    prompt = email_content + question_prompt

    response = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        model=COMPLETIONS_MODEL
    )["choices"][0]["text"].strip(" \n")
    print(response)
    
    return response

def identify_meeting(email_content):
    question_prompt = "Identify the discussion topic of the meeting given in the  email and output the topic and output format should be topic: summarize the topic in a sentance with all details, date: the date in mm/dd/yyyy format, details: details, Sender: Sender "
    prompt = email_content + question_prompt

    response = openai.Completion.create(
        prompt=prompt,
        temperature=0,
        max_tokens=300,
        model=COMPLETIONS_MODEL
    )["choices"][0]["text"].strip(" \n")
    print(response)
    
    return response

def string_to_dictionary(input_string):
    lines = input_string.split('\n')
    dictionary = {}
    for line in lines:
        key_value = line.split(': ')
        key = key_value[0]
        value = key_value[1]
        dictionary[key] = value
    print(dictionary)
    return dictionary




#main function
def main(email_content):
    email_type = identify_type(email_content)
    print(email_type)
    
    if email_type.lower() == "task":
        print('taskkk')
        task_details = identify_task(email_content)
        res = string_to_dictionary(task_details)
        task_list.append(res)
        print(task_list)
        
    elif email_type.lower() == "meeting":
        meeting_details = identify_meeting(email_content)
        response = string_to_dictionary(meeting_details)
        meetings_list.append(response)
        print(meetings_list)
        
    elif email_type.lower() == "notification":
        meeting_details = identify_task(email_content)
        response = string_to_dictionary(meeting_details)
        notification_list.append(response)
        print(notification_list)
        
    final_response = {
            'message' : "sucess"
    }
    final_res = json.dumps(final_response)
    return json.loads(final_res)
        
        
        
        
        
    

