from flask import Flask, request, jsonify, render_template  # pip install flask
from werkzeug.exceptions import BadRequest
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return render_template('home.html')


# Show all events in json fromat
@app.route('/events', methods=['GET'])
def get_events():
    list_event = []
    for each in all_events():
        typ = each[0]
        val = each[1]
        event = {'Type': typ, 'Value': val}
        list_event.append(event)
    return jsonify(list_event)


# Post new event
@app.route('/event', methods=['POST', 'GET'])
def new_event():
    if request.method == 'POST':
        x = request.form['Type']
        y = int(request.form['Value'])
        if (1 <= y <= 5) and (x == 'INCREMENT') or (1 <= y <= 5) and (x == 'DECREMENT'):
            insert_event(x, y)
            return render_template('home.html')
            # return jsonify({'Type': x, 'Value': y})
        else:
            return render_template('InputError.html')
    else:
        return render_template('form.html')


@app.route('/value', methods=['GET'])
def current_value():
    sum = 0
    for each in all_events():
        typ = each[0]
        val = each[1]
        if typ == 'INCREMENT':
            sum = sum + val
        else:
            sum = sum - val
    return render_template('Value.html', value=sum)
    # return str(sum)


@app.route('/value/:<n>')
def tth_value(n):
    try:
        t = int(n)
        if t == 0:
            return render_template('Value.html', value=0)
            # return '0'
        elif 0 < t <= all_events(length=t):
            sum = 0
            for each in all_events(t_events=t):
                typ = each[0]
                val = each[1]
                if typ == 'INCREMENT':
                    sum = sum + val
                else:
                    sum = sum - val
            return render_template('Value.html', value=sum)
            # return str(sum)
        elif t > all_events(length=t):
            return current_value()
        elif t < 0:
            return BadRequest()
    except:
        return BadRequest()


try:
    conn = sqlite3.connect(database='sample.db')
    sql = 'CREATE TABLE event(Type VARCHAR(50), Value INT)'
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.close()
except:
    pass


def insert_event(x, y):
    conn = sqlite3.connect(database='sample.db')
    sql = 'INSERT INTO event(Type,Value) VALUES(?,?)'
    cur = conn.cursor()
    cur.execute(sql, (x, y))
    conn.commit()
    cur.close()
    conn.close()


def all_events(t_events=None, length=None):
    conn = sqlite3.connect(database='sample.db')
    sql = 'SELECT * FROM event'
    cur = conn.cursor()
    cur.execute(sql)
    if t_events is None and length is not None:
        events = len(cur.fetchall())
    elif length is None and t_events is not None:
        events = cur.fetchmany(t_events)
    else:
        events = cur.fetchall()
    cur.close()
    conn.close()
    return events


if __name__ == '__main__':
    app.run(debug=True)
