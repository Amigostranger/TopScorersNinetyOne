from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db():
    return sqlite3.connect('scores.db')



@app.route('/score/<name>', methods=['GET'])
def get_score(name):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT score FROM scores WHERE name = ?", (name,))
    result = cursor.fetchall()

    conn.close()

    return jsonify(result)


@app.route('/top', methods=['GET'])
def top_scores():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, score FROM scores")
    records = cursor.fetchall()

    conn.close()

    max_score = records[0][1]

    for i in range(len(records)):
        score = records[i][1]
        if score > max_score:
            max_score = score

    top_people = []

    for i in range(len(records)):
        if records[i][1] == max_score:
            top_people.append(records[i][0])

    return jsonify({
        "top_scorers": top_people,
        "score": max_score
    })


if __name__ == "__main__":
    app.run(debug=True)