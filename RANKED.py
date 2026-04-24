import json
import os

DATA_FILE = "data.json"

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(players, f)

def load_data():
    global players

    try:
        with open(DATA_FILE, "r") as f:
            players.update(json.load(f))
    except:
        players = {}

players = {}
START_ELO = 200

def add_player(name):
    if name in players:
        return False
    players[name] = START_ELO
    save_data()
    return True


def show_players():
    return players


def update_elo_2v2(p1, p2, p3, p4, score_diff, k=6):
    team1 = (p1 + p2) / 2
    team2 = (p3 + p4) / 2

    e1 = 1 / (1 + 10 ** ((team2 - team1) / 400))
    e2 = 1 / (1 + 10 ** ((team1 - team2) / 400))

    multiplier = 1 + (score_diff / 15)
    multiplier = min(multiplier, 1.8)

    change1 = k * multiplier * (1 - e1)
    change2 = k * multiplier * (0 - e2)

    return (
        p1 + change1,
        p2 + change1,
        p3 + change2,
        p4 + change2
    )

def play_match(p1, p2, p3, p4, score_diff, team1_wins=True):
    r1, r2, r3, r4 = (
        players[p1],
        players[p2],
        players[p3],
        players[p4]
    )

    new_r1, new_r2, new_r3, new_r4 = update_elo_2v2(
        r1, r2, r3, r4, score_diff
    )

    if not team1_wins:
        new_r1, new_r2, new_r3, new_r4 = new_r3, new_r4, new_r1, new_r2

    players[p1] = round(new_r1)
    players[p2] = round(new_r2)
    players[p3] = round(new_r3)
    players[p4] = round(new_r4)

    save_data()

def leaderboard():
    return sorted(players.items(), key=lambda x: x[1], reverse=True)