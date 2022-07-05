#from __future__ import annotations
import requests
#import tkinter
import json
#import sqlalchemy
import random

#API
def get_data():
    response = requests.get("https://opentdb.com/api.php?amount=10")
    data = response.json()
    return data

#Replace characters
def replace_invalid_characters(string):
    string = string.replace("&#039;", "\'")
    string = string.replace("&quot;", "\"")
    return string

#Display Question and Answers (returns list of answers)
def display_answers(list_of_questions):
    #Create Answer List
    list_of_answers = []
    list_of_answers.append(replace_invalid_characters(list_of_questions[index]['correct_answer']))
    for answer in list_of_questions[index]['incorrect_answers']:
        answer = replace_invalid_characters(answer)
        list_of_answers.append(answer)
    random.shuffle(list_of_answers)

    #Display Answers
    for answer_index in range(len(list_of_answers)):
        print("{}. {}".format(answer_index, list_of_answers[answer_index]))
    return list_of_answers
    
#Check Answer
def check_answer(list_of_answers, list_of_questions):
    correct_answer = list_of_questions[index]['correct_answer']
    while True:
        try:
            player_answer = int(input("Please input answer number: "))
            if list_of_answers[player_answer] == correct_answer:
                print("Correct\n")
            else:
                print("Wrong :(\n")
            break
        except TypeError:
            print("Not an integer. Please try again")
        except:
            print("Answer out of range. Please try again") 

#Run
data = get_data()
list_of_questions = data["results"]
for index in range(0, len(list_of_questions)):
    #Replace Broken Characters
    list_of_questions[index]["question"] = replace_invalid_characters(list_of_questions[index]["question"])

    #Print Question
    print(list_of_questions[index]["question"])
    
    #Display Answers
    list_of_answers = display_answers(list_of_questions)

    #Get Input
    check_answer(list_of_answers, list_of_questions)