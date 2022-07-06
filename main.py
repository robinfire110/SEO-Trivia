# from __future__ import annotations
import requests
# import tkinter
import json
import sqlalchemy as db
import random
import time
import pandas as pd
import re
import os


class TriviaGame:
    def __init__(self):
        #Start Game
        os.system("clear")
        print("Welcome to the Amazing Blazing Trivia Extravaganza!")
        print("---------------------------------------------------")
        
        #Select Topic
        print("Topic Selection")
        print("---------------------------------------------------")
        self.topic = self.get_topic()
        #print(self.topic)
        print("---------------------------------------------------")
        
        #Select Difficulty
        print("Difficulty Selection")
        print("---------------------------------------------------")
        self.difficulty = self.get_difficulty()
        #print(self.difficulty)
        print("---------------------------------------------------")

        #Get Questions
        print(f"Topic: {self.topic['name']} | Difficulty: {self.difficulty}")
        print("---------------------------------------------------")
        self.data = self.get_data(self.topic, self.difficulty)
        self.question_answer_dict = {}
        self.list_of_questions = []

        # replace invalid characters
        for question in self.data["results"]:
            question["question"] = self.replace_invalid_characters(question["question"])
            self.list_of_questions.append(question)
            self.question_answer_dict[question["question"]] = {}
        self.correct_answers = []

        self.parse_answers()
        self.start_time = time.time()
        self.params = []
        for question in self.question_answer_dict:
            #Header
            print("\n---------------------------------------------------")
            print(f"Question {len(self.params)+1}")
            print("---------------------------------------------------\n")

            # Print Question
            print(question)
            # Display Answers
            # print(self.question_answer_dict[question])
            for index in range(len(self.question_answer_dict[question]["answers"])):
                print("{}. {}".format(index+1, self.question_answer_dict[question]["answers"][index]))

            while True:
                try:
                    player_answer = int(input("Please input answer number: "))
                    if self.question_answer_dict[question]["answers"][player_answer-1] == \
                            self.question_answer_dict[question]["correct_answer"]:
                        self.params.append(1)
                        print("\nCORRECT!")
                    else:
                        self.params.append(0)
                        print("\nINCORRECT!\nThe correct answer was {}".format(self.question_answer_dict[question]["correct_answer"]))
                    break
                except TypeError:
                    print("Not an integer. Please try again")
                except:
                    print("Answer out of range. Please try again")

        # Database
        e = db.create_engine('sqlite:///data_base_name.db')
        inspector = db.inspect(e)
        if not inspector.has_table("game"):
            e.execute(
                "CREATE TABLE game (id INT(8) NOT NULL default 0, Q1 BOOLEAN default 0, Q2 BOOLEAN default 0, Q3 BOOLEAN default 0, Q4 BOOLEAN default 0, Q5 BOOLEAN default 0, Q6 BOOLEAN default 0, Q7 BOOLEAN default 0, Q8 BOOLEAN default 0, Q9 BOOLEAN default 0, Q10 BOOLEAN default 0, Total_Time FLOAT(24) default 0, Percentage FLOAT(24) default 0, Total_Score FLOAT(24) default 0);")
            # engine.execute(f"INSERT INTO game (id) VALUES (1);")
        
        # Get Row number
        row_num = e.execute("SELECT COUNT(*) from game").fetchall()
        temp = re.findall(r'\d+', str(row_num[0]))
        res = list(map(int, temp))
        row_num = res[0] + 1

        #Other Values
        total_correct = self.params.count(1)
        self.params.insert(0, row_num)
        total_time = time.time() - self.start_time
        self.params.append(total_time)
        self.params.append(total_correct / 10)
        self.params.append((total_correct / 10) * (900 / total_time) * 100)

        #Insert into Database
        e.execute("INSERT INTO game (id,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Total_Time,Percentage,Total_Score) VALUES "
                       "({},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                        self.params[0], self.params[1], self.params[2], self.params[3], self.params[4], self.params[5],
                        self.params[6], self.params[7], self.params[8], self.params[9], self.params[10],
                        self.params[11], self.params[12], self.params[13]))

    def get_data(self, topic, difficulty):
        url = "https://opentdb.com/api.php?amount=10"

        #Add Parameters
        if topic['id'] != 0:
            url += (f"&category={topic['id']}")
        if difficulty != "Any Difficulty":
            url += (f"&difficulty={difficulty.lower()}")

        #Get Questions
        response = requests.get(url)
        data = response.json()
        return data

    def get_topic(self):
        topic_list = (requests.get("https://opentdb.com/api_category.php").json())['trivia_categories']
        topic_list.insert(0, {'id': 0, 'name': 'Any Topic'}) #Add any topic to the beginning
        topic_length = len(topic_list)
        for index in range(topic_length):
            print(f"{index+1}. {topic_list[index]['name']}")
        
        #Loop until they select a topic
        while True:
            try:
                topic_selection = input(f"Please select a topic (1-{topic_length}): ")
                topic_selection = int(topic_selection)
                if topic_selection > 0 and topic_selection <= topic_length:
                    return topic_list[topic_selection-1]
                    break
                else:
                    print(f"Please select a number within range! ")
            except:
                print("Not an integer. Please try again")

    def get_difficulty(self):
        difficulty_list = ["Any Difficulty", "Easy", "Medium", "Hard"]
        for index in range(len(difficulty_list)):
            print(f"{index+1}. {difficulty_list[index]}")
        
        #Loop until they select difficulty
        while True:
            try:
                difficutly_selection = input("Please select difficulty (1-4): ")
                difficutly_selection = int(difficutly_selection)
                if difficutly_selection > 0 and difficutly_selection <= 4:
                    return difficulty_list[difficutly_selection-1]
                    break
                else:
                    print(f"Please select a number within range! ")
            except:
                print("Not an integer. Please try again")

    # Replace characters
    def replace_invalid_characters(self, string):
        string = string.replace("&#039;", "\'")
        string = string.replace("&quot;", "\"")
        string = string.replace("&amp;", "&")
        string = string.replace("&shy;", "-")
        return string

    # Display Question and Answers (returns list of answers)
    def parse_answers(self):
        # Create Answer List
        for question_index in range(len(self.list_of_questions)):
            list_of_answers = []
            # print("index" + str(question_index))
            correct_answer = self.replace_invalid_characters(self.list_of_questions[question_index]['correct_answer'])
            list_of_answers.append(correct_answer)
            # print("inside parse answer" + self.list_of_questions[question_index]["question"])
            self.question_answer_dict[self.list_of_questions[question_index]["question"]][
                "correct_answer"] = correct_answer
            for answer in self.list_of_questions[question_index]['incorrect_answers']:
                answer = self.replace_invalid_characters(answer)
                list_of_answers.append(answer)
            random.shuffle(list_of_answers)

            # add answer to q_a_dict
            self.question_answer_dict[self.list_of_questions[question_index]["question"]]["answers"] = list_of_answers
        # print("after for loop, in parse answers" + str(self.question_answer_dict))

#Run Program
run = True
while run:
    t = TriviaGame()
    engine = db.create_engine('sqlite:///data_base_name.db')
    res = engine.execute("SELECT * FROM game").fetchall()

    #Print Results
    res = res.pop()
    print("\n---------------------------------------------------")
    print("Final Results:")
    print(f"Accuracy: {res[12]*100}%")
    final_time = time.strftime("%M:%S", time.gmtime(res[11]))
    print(f"Time Taken: {final_time} (M:S)")
    print(f"Final Score: {int(res[13])}")
    print("---------------------------------------------------")

    #Play Again?
    while True:
        again = input("Would you like to play again? (y/n): ")
        if again == "n":
            run = False
            os.system("clear")
            print("Thanks for playing!")
            break
        elif again != "y":
            print("Please input y or n.")
        else:
            break

