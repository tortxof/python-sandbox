#! /usr/bin/env python3.2

import sys

round = 0
players = []
scores = []
scoreLimit = 10000

def printScores():
    print("Current scores:")
    for i in range(len(players)):
        playerScore = sum(scores[i])
        print(players[i], "\n\t", playerScore)
        if playerScore >= scoreLimit:
            print(players[i], " is the winner!")
    print("\n")

def gameOver():
    over = False
    for i in range(len(players)):
        if sum(scores[i]) >= scoreLimit:
            over = True
    return(over)

print("Enter player names. Enter blank line for no new players.")

while True:
    newplayer = input('Player name: ')
    if newplayer != '':
        players.append(newplayer)
    else:
        break
print("\n")

print("\nPlayers:")
for i in players:
    print(i)
print("\n")

for i in range(len(players)):
    scores.append([])

while True:
    round += 1
    print("Round ", round)
    for i in range(len(players)):
        while True:
            try:
                print(players[i], "'s turn.")
                turnScore = int(input("Score for this turn: "))
                break
            except ValueError:
                print("Not an integer. Try again.\n")
        scores[i].append(turnScore)
        print("\n")
        printScores()
    if gameOver():
        print("Game Over!")
        sys.exit(0)
