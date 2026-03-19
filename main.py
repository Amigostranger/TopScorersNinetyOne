import sqlite3


def read_file(filename):
    file = open(filename, 'r')
    data = file.read()
    file.close()
    return data


def parse_csv(data):
    lines = data.strip().split('\n')
    records = []

    for i in range(1,len(lines)):
        parts = lines[i].split(',')

        name = parts[0].strip()
        score = float(parts[2].strip())

        records.append((name, score))

    return records


def create_database():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            name TEXT,
            score REAL
        )
    ''')

    conn.commit()
    conn.close()


def insert_records(records):
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()

    for i in range(len(records)):
        name = records[i][0]
        score = records[i][1]

        cursor.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))

    conn.commit()
    conn.close()


def get_top_scorers(records):
    max_score = records[0][1]

    for i in range(len(records)):
        score = records[i][1]
        if score > max_score:
            max_score = score

    top_people = []

    for i in range(len(records)):
        if records[i][1] == max_score:
            top_people.append(records[i][0])

    # bubble sort
    n = len(top_people)
    for i in range(n):
        for j in range(0, n - i - 1):
            if top_people[j] > top_people[j + 1]:
                temp = top_people[j]
                top_people[j] = top_people[j + 1]
                top_people[j + 1] = temp

    return top_people, max_score


def print_output(top_people, max_score):
    for i in range(len(top_people)):
        print(top_people[i])

    if int(max_score) == max_score:
        print("Score:", int(max_score))
    else:
        print("Score:", max_score)


def main():
    create_database()

    data = read_file('TestData.csv')
    records = parse_csv(data)

    insert_records(records)

    top_people, max_score = get_top_scorers(records)
    print_output(top_people, max_score)


if __name__ == "__main__":
    main()