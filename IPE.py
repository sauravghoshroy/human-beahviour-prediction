#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# Name of the project: Individual Programming Exercise: (IPE)
# Description: A program that "predicts" human behavior using a simple game.
# File Name: IPE.py
# File Description: Python code for IPE program.
# Author: Saurav Ghosh Roy
# Last Updated: Thu 7 Feb, 2021
"""
#imports standard libraries to execute terminal commands from python
import sys, subprocess

#installs and imports 3rd party package (pyinputplus) for input validation
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinputplus'])
import pyinputplus as pyip 

#imports function from local source package to generate random number using linear congruence method
from mypackage.function import (rand_num_gen)

#declares global variables
throw00, throw01, throw10, throw11 = 0, 0, 0, 0 #throwij stores the number of times the human player chooses i given that in the previous bid his/her bid was j
last_player_throw = None #last throw made by player during the game
computer_wins, player_wins, draws = 0, 0, 0 #number of games won by the computer, player and the number of games that were draw

#defines functions used in script
def random_throw(x):
    """ generates a random throw for the computer"""
    computer_throw = {x <= 2 ** 31 : 0, x > (2 ** 31) : 1}[True]
    return computer_throw

def learnt_throw(x):
    """ generates a throw for the computer based on learning """
    computer_throw = {last_player_throw == 0 : {throw10 > throw00: 1, throw10 < throw00 : 0, throw10 == throw00 : random_throw(x)}[True],
                      last_player_throw == 1 : {throw11 > throw01: 1, throw11 < throw01 : 0, throw11 == throw01 : random_throw(x)}[True],
                      last_player_throw == None : random_throw(x)}[True]
    return computer_throw

#provides user the option to manually enter seed before starting game
seed = pyip.inputInt(prompt = "\n\nEnter any integer as initial seed or press the enter/return key to use default seed (1234):", blank = True)
if seed == "" or seed == 1234 : seed = 1234
print("Initial seed has been set to",seed,"\n\n- - - - - - - - <<< Game Starts Here >>> - - - - - - - -") 

#greets user with welcome message
print("\nWelcome to Human Behavior Prediction by Saurav Ghosh Roy")
#stores random number generated with initial seed 
random_number = rand_num_gen(seed)

#starts the game in an infinite loop until program is killed or player chooses not to start a new game
while True:    
    #gets game type, easy or difficult, from user 
    game_type = int(pyip.inputChoice(['1','2'], prompt="\nPlease choose the type of game (1: Easy, 2: Difficult):"))
    #gets number of game moves from player
    game_moves = pyip.inputInt(prompt="Enter number of moves:", greaterThan=0)
    #resets computer & user's score to 0 at the start of new game
    computer_score, player_score = 0, 0
    #game rounds start here
    for move in range(1, game_moves+1) :
        #makes computer's move before asking user to make a move for each round
        computer_move = {game_type == 1 : random_throw(random_number), game_type == 2 : learnt_throw(random_number)}[True]        
        #gets user's move for each round
        player_move = int(pyip.inputChoice(['0','1'], prompt="\nROUND {round} Choose your move for round: {round}, (0 or 1):".format(round=move)))
        #declares the winner of the round
        winner = {player_move == computer_move : "Machine", player_move != computer_move : "Player"}[True]
        #calculates total computer & user score at end of each round
        computer_score = {winner == "Machine": computer_score+1, winner == "Player": computer_score}[True]
        player_score = {winner == "Machine": player_score, winner == "Player": player_score+1}[True]
        #reports the outcome of each round - user's move, computer's move, winner, score in digits and score graph
        print("Player Move =", player_move, "Machine Move =", computer_move, ".", winner, "wins!\nYou:", player_score, "Computer:", computer_score,
              "\nPLAYER:", "*"*player_score, "\nCOMPUTER:", "*"*computer_score, "\n\n")        
        #updates the throw00, throw01, throw10 and throw11 global variables
        (throw00, throw01, throw10, throw11) = {player_move == 0 and last_player_throw == 0 : (throw00 + 1, throw01, throw10, throw11),
                                                player_move == 0 and last_player_throw == 1 : (throw00, throw01 + 1, throw10, throw11),
                                                player_move == 1 and last_player_throw == 0 : (throw00, throw01, throw10 + 1, throw11),
                                                player_move == 1 and last_player_throw == 1 : (throw00, throw01, throw10, throw11 + 1),
                                                last_player_throw == None : (throw00, throw01, throw10, throw11)}[True]
        #updates the last_player_throw global variable
        last_player_throw = {player_move == 0 : 0, player_move == 1 : 1}[True] 
        #stores new random number at the beginning of each round using the random number from previous round
        random_number = rand_num_gen(random_number)            
    #reports outcome of the game - game result and final score
    print({game_type == 1 and player_score > computer_score  : "Player Wins! Easy Game is over final result Player: {ps} - Computer: {cs}",
           game_type == 1 and player_score < computer_score  : "Machine Wins! Easy Game is over final result Player: {ps} - Computer: {cs}",
           game_type == 2 and player_score > computer_score  : "Player Wins! Difficult Game is over final result Player: {ps} - Computer: {cs}",
           game_type == 2 and player_score < computer_score  : "Machine Wins! Difficult Game is over final result Player: {ps} - Computer: {cs}",
           game_type == 1 and player_score == computer_score : "It was a tie! Easy Game is over final result Player: {ps} - Computer: {cs}"+
                                                               "\nPlay against the computer and see if you are able to beat it!",
           game_type == 2 and player_score == computer_score : "It was a tie! Difficult Game is over final result Player: {ps} - Computer: {cs}"+
                                                               "\nPlay against the computer and see if you are able to beat it!"}[True]
                                                               .format(cs = computer_score, ps = player_score))   
    #updates number of games won by the computer, player and the number of games that were draw
    computer_wins, player_wins, draws = {player_score < computer_score : computer_wins + 1, player_score >= computer_score : computer_wins}[True],\
                                        {player_score > computer_score : player_wins + 1, player_score <= computer_score : player_wins}[True],\
                                        {player_score == computer_score : draws +1, player_score != computer_score : draws}[True]
    #asks if user wants to play a new game or not
    play_again = pyip.inputChoice(["Y", "YES", "N", "NO"], prompt="\nDo you want to start a new game? Yes (Y) No (N): ")    
    #reports tally of game results, thanks the user and exits program because user does not want to play a new game
    if play_again == "N" or play_again == "NO":
        print({draws > 0 : "\nTotal Draws: {d} ".format(d = draws), draws <= 0 : "\n"}[True])
        print("Total Player Wins: {pw}\nTotal Computer Wins: {cw}\n\nThanks for playing. Hope to see you again!\n"
              .format(pw = player_wins, cw = computer_wins))
        break