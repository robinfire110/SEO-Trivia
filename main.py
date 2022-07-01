#from __future__ import annotations
import requests
import tkinter
import json
import sqlalchemy
import random

#API
response = requests.get("https://opentdb.com/api.php?amount=10")
data = response.json()
# print(data)

list_of_questions = data["results"]
for index in range(0, len(list_of_questions)):
  #Replace Broken Characters
  list_of_questions[index]["question"] = list_of_questions[index]["question"].replace("&#039;", "\'")
  list_of_questions[index]["question"] = list_of_questions[index]["question"].replace("&quot;", "\'")

  #Print Question
  print(list_of_questions[index]["question"])
  
  #Create Answer List
  list_of_answers = []
  correct_answer = list_of_questions[index]['correct_answer']
  correct_answer = correct_answer.replace("&#039;", "\'")
  correct_answer = correct_answer.replace("&quot;", "\'")
  list_of_answers.append(correct_answer)
  for answer in list_of_questions[index]['incorrect_answers']:
    answer = answer.replace("&#039;", "\'")
    answer = answer.replace("&quot;", "\'")
    list_of_answers.append(answer)
  random.shuffle(list_of_answers)

  #Display Answers
  for answer_index in range(len(list_of_answers)):
    print("{}. {}".format(answer_index, list_of_answers[answer_index]))

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
