from flask import Flask, render_template, request, redirect
from RANKED import players, add_player, play_match, load_data, save_data

import os

load_data()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        add_player(name)
        save_data()
        return redirect("/")

    return render_template("add.html")


@app.route("/leaderboard")
def lb():
    sorted_players = sorted(players.items(), key=lambda x: x[1], reverse=True)
    return render_template("leaderboard.html", players=sorted_players)


@app.route("/match")
def match():
    return render_template("match.html", players=players.keys())


@app.route("/play-match", methods=["POST"])
def play_match_route():
    p1 = request.form["p1"]
    p2 = request.form["p2"]
    p3 = request.form["p3"]
    p4 = request.form["p4"]

    # 🧠 BEFORE MATCH (ELO snapshot)
    before_match = {
        p1: players[p1],
        p2: players[p2],
        p3: players[p3],
        p4: players[p4]
    }

    # 🧠 BEFORE RANKS
    before_sorted = sorted(players.items(), key=lambda x: x[1], reverse=True)
    before_ranks = {
        name: rank
        for rank, (name, _) in enumerate(before_sorted)
    }

    score1 = int(request.form["score1"])
    score2 = int(request.form["score2"])

    diff = min(abs(score1 - score2), 10)
    team1_wins = score1 > score2

    play_match(p1, p2, p3, p4, diff, team1_wins)
    save_data()

    # 🧠 AFTER MATCH (ELO delta)
    delta = {
        p1: players[p1] - before_match[p1],
        p2: players[p2] - before_match[p2],
        p3: players[p3] - before_match[p3],
        p4: players[p4] - before_match[p4]
    }

    # 🧠 AFTER RANKS
    after_sorted = sorted(players.items(), key=lambda x: x[1], reverse=True)
    after_ranks = {
        name: rank
        for rank, (name, _) in enumerate(after_sorted)
    }

    # 🧠 MOVEMENT (rank change)
    movement = {
        name: before_ranks.get(name, 0) - after_ranks.get(name, 0)
        for name in players
    }

    return render_template(
        "leaderboard.html",
        players=after_sorted,
        delta=delta,
        movement=movement
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)