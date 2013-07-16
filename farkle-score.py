#! /usr/bin/env python3.2

print("Enter player names. Enter blank line for no new players.")
players = []

while True:
    newplayer = input('Player name: ')
    if newplayer != '':
        players.append(newplayer)
    else:
        break

print("\nPlayers:")
for i in players:
    print(i)

