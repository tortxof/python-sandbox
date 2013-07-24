#! /usr/bin/env python3

import sys

round = 0
players = []
winners = []
scores = []
scoreLimit = 10000

def printScores():
    print("\nCurrent scores:")
    for i in range(len(players)):
        playerScore = sum(scores[i])
        print(players[i], "\n\t", playerScore)

def printRoundScores():
    print("\nScores per round:")
    for i in range(len(players)):
        print(i, players[i])
        print(scores[i])

def gameOver():
    over = False
    for i in range(len(players)):
        if sum(scores[i]) >= scoreLimit:
            winners.append(i)
            over = True
    return(over)

def undoScores():
    global round
    round = 0
    while True:
        printRoundScores()
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

print("Enter player names. Enter blank line for no new players.\n")

while True:
    newplayer = input('Player name: ')
    if newplayer != '':
        players.append(newplayer)
    else:
        break

print("\nPlayers:")
for i in players:
    print(i)

for i in range(len(players)):
    scores.append([])

while True:
    round += 1
    for i in range(len(players)):
        if len(scores[i]) >= round:
            continue
        print("\nRound", round)
        while True:
            try:
                print(players[i] + "'s turn.")
                turnScore = int(input("Score for this turn: "))
                break
            except ValueError:
                print("Not an integer. Try again.\n")
        if turnScore >= 0:
            scores[i].append(turnScore)
            printScores()
        else:
            undoScores()
            break
    if gameOver():
        print("""
##################
### Game Over! ###
##################
""")
        printRoundScores()
        printScores()
        print("\nWinners:")
        for i in winners:
            print(players[i])
        sys.exit(0)
