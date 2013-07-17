#! /usr/bin/env python3.2

import sys

gameOver = False
round = 0
players = []
scores = []
scoreLimit = 10000

def printScores():
    global gameOver
    print("Current scores:")
    for i in range(len(players)):
        print(players[i], "\n\t", scores[i],)
        if scores[i] >= scoreLimit:
            print(players[i], " is the winner!")
            gameOver = True
    print("\n")
    if gameOver:
        print("Game Over")
        sys.exit(0)


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
    scores.append(0)

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
        scores[i] += turnScore
        print("\n")
        printScores()
