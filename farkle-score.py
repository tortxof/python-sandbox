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

def undoScores():
    global round
    round = 0
    while True:
        for i in range(len(players)):
            print(i, players[i])
            print(scores[i])
        while True:
            try:
                selectedPlayer = int(input("Edit which player: "))
                break
            except ValueError:
                print("Not an integer. Try again")
        if selectedPlayer >= 0 and selectedPlayer < len(players):
            scores[selectedPlayer].pop()
        else:
            break

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
        if len(scores[i]) >= round:
            continue
        while True:
            try:
                print(players[i], "'s turn.")
                turnScore = int(input("Score for this turn: "))
                break
            except ValueError:
                print("Not an integer. Try again.\n")
        if turnScore >= 0:
            scores[i].append(turnScore)
            print("\n")
            printScores()
        else:
            undoScores()
            break
    if gameOver():
        print("Game Over!")
        sys.exit(0)
