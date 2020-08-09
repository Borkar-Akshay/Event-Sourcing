from flask import Flask, request, jsonify, render_template # pip install flask
from werkzeug.exceptions import BadRequest
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

try:
    conn = sqlite3.connect(database='sample.db')
    sql = 'CREATE TABLE event(Type VARCHAR(50), Value INT)'
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.close()
except:
    pass


@app.route('/')
def home():
    return render_template('Home.html')


# Show all events in json fromat
@app.route('/events', methods=['GET'])
def Get_Events():
    conn = sqlite3.connect(database='sample.db')
    sql = 'SELECT * FROM event'
    cur = conn.cursor()
    cur.execute(sql)
    allEvents = cur.fetchall()
    list_event = []
    for each in allEvents:
        typ = each[0]
        val = each[1]
        event = {'Type': typ, 'Value': val}
        list_event.append(event)
    cur.close()
    conn.close()
    return jsonify(list_event)


# Post new event
@app.route('/event', methods=['POST', 'GET'])
def New_Event():
    if request.method == 'POST':
        x = request.form['Type']
        y = int(request.form['Value'])
        if (1 <= y <= 5) and (x == 'INCREMENT') or (1 <= y <= 5) and (x == 'DECREMENT'):
            conn = sqlite3.connect(database='sample.db')
            sql = 'INSERT INTO event(Type,Value) VALUES(?,?)'
            cur = conn.cursor()
            cur.execute(sql, (x, y))
            conn.commit()
            cur.close()
            conn.close()
            return render_template('Home.html')
            # return jsonify({'Type': Type, 'Value': Value})
        else:
            return render_template('Bad_Input.html')
    else:
        return render_template('Form.html')


@app.route('/value', methods=['GET'])
def Current_Value():
    conn = sqlite3.connect(database='sample.db')
    sql = 'SELECT * FROM event'
    cur = conn.cursor()
    cur.execute(sql)
    allEvents = cur.fetchall()
    sum = 0
    for each in allEvents:
        typ = each[0]
        val = each[1]
        if typ == 'INCREMENT':
            sum = sum + val
        else:
            sum = sum - val
    cur.close()
    conn.close()
    return render_template('Current_Value.html', value=sum)
    # return str(sum)


@app.route('/value/:<n>')
def tth_Value(n):
    try:
        t = int(n)
        if t == 0:
            return render_template('Current_Value.html', value=0)
            # return '0'
        elif 0 < t <= Total_events():
            conn = sqlite3.connect(database='sample.db')
            sql = 'SELECT * FROM event'
            cur = conn.cursor()
            cur.execute(sql)
            allEvents = cur.fetchmany(t)
            sum = 0
            for each in allEvents:
                typ = each[0]
                val = each[1]
                if typ == 'INCREMENT':
                    sum = sum + val
                else:
                    sum = sum - val
            cur.close()
            conn.close()
            return render_template('Current_Value.html', value=sum)
            # return str(sum)
        elif t > Total_events():
            return Current_Value()
        elif t < 0:
            return BadRequest()
    except:
        return BadRequest()


def Total_events():
    conn = sqlite3.connect(database='sample.db')
    sql = 'SELECT * FROM event'
    cur = conn.cursor()
    cur.execute(sql)
    allEvents = cur.fetchall()
    length = len(allEvents)
    cur.close()
    conn.close()
    return length


if __name__ == '__main__':
    app.run(debug=True)
