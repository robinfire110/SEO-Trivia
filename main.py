# from __future__ import annotations
import requests
# import tkinter
import json
import sqlalchemy as db
import random
import time
import pandas as pd
import re


class TriviaGame:
    def __init__(self):
        self.data = self.get_data()
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
            # Print Question
            print(question)
            # Display Answers
            # print(self.question_answer_dict[question])
            for index in range(len(self.question_answer_dict[question]["answers"])):
                print("{}. {}".format(index, self.question_answer_dict[question]["answers"][index]))

            while True:
                try:
                    player_answer = int(input("Please input answer number: "))
                    if self.question_answer_dict[question]["answers"][player_answer] == \
                            self.question_answer_dict[question]["correct_answer"]:
                        self.params.append(1)
                        print("Correct\n")
                    else:
                        self.params.append(0)
                        print("Wrong :(\n")
                    break
                except TypeError:
                    print("Not an integer. Please try again")
                except:
                    print("Answer out of range. Please try again")

                    # Run
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
        total_correct = self.params.count(1)
        self.params.insert(0, row_num)
        total_time = time.time() - self.start_time
        self.params.append(total_time)
        self.params.append(total_correct / 10)
        self.params.append((total_correct / 10) * (900 / total_time) * 100)
        e.execute("INSERT INTO game (id,Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Total_Time,Percentage,Total_Score) VALUES "
                       "({},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(
                        self.params[0], self.params[1], self.params[2], self.params[3], self.params[4], self.params[5],
                        self.params[6], self.params[7], self.params[8], self.params[9], self.params[10],
                        self.params[11], self.params[12], self.params[13]))

    def get_data(self):
        response = requests.get("https://opentdb.com/api.php?amount=10")
        data = response.json()
        return data

    # Replace characters
    def replace_invalid_characters(self, string):
        string = string.replace("&#039;", "\'")
        string = string.replace("&quot;", "\"")
        string = string.replace("&amp;", "&")
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


# Setup Database


# Print Database
# print(engine.execute("SELECT * FROM game").fetchall())

# Run loop for game


# print("Total Time: " + str(time.time()-start_time))

t = TriviaGame()
engine = db.create_engine('sqlite:///data_base_name.sql')
res = engine.execute("SELECT * FROM game").fetchall()
print(res)
