#from __future__ import annotations
import requests
#import tkinter
import json
import sqlalchemy as db
import random
import time
import pandas as pd
import re

#API
def get_data():
    response = requests.get("https://opentdb.com/api.php?amount=10")
    data = response.json()
    return data

#Replace characters
def replace_invalid_characters(string):
    string = string.replace("&#039;", "\'")
    string = string.replace("&quot;", "\"")
    string = string.replace("&amp;", "&")
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
start_time = time.time()

#Setup Database
engine = db.create_engine('sqlite:///data_base_name.db')
if not engine.has_table("game"):
    engine.execute("CREATE TABLE game (id INT(8) NOT NULL default 0, Q1 BOOLEAN default 0, Q2 BOOLEAN default 0, Q3 BOOLEAN default 0, Q4 BOOLEAN default 0, Q5 BOOLEAN default 0, Q6 BOOLEAN default 0, Q7 BOOLEAN default 0, Q8 BOOLEAN default 0, Q9 BOOLEAN default 0, Q10 BOOLEAN default 0, Total_Time FLOAT(24) default 0, Percentage FLOAT(24) default 0, Total Score FLOAT(24) default 0);")
    engine.execute(f"INSERT INTO game (id) VALUES (1);")
else:
    #Get Row number
    row_num = engine.execute("SELECT COUNT(*) from game").fetchall()
    temp = re.findall(r'\d+', str(row_num[0]))
    res = list(map(int, temp))
    row_num = res[0]+1
    engine.execute(f"INSERT INTO game (id) VALUES ({row_num});")

#Print Database
#print(engine.execute("SELECT * FROM game").fetchall())

#Run loop for game
for index in range(0, len(list_of_questions)):
    #Replace Broken Characters
    list_of_questions[index]["question"] = replace_invalid_characters(list_of_questions[index]["question"])

    #Print Question
    print(list_of_questions[index]["question"])
    
    #Display Answers
    list_of_answers = display_answers(list_of_questions)

    #Get Input
    check_answer(list_of_answers, list_of_questions)

#print("Total Time: " + str(time.time()-start_time))