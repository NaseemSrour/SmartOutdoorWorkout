import plotly.plotly as py
import plotly.graph_objs as go
from django.shortcuts import render
from django.http import HttpResponse
from django.http import QueryDict
import json
import MySQLdb
import datetime
import MySQLdb
import pandas as pd

def userspeedoverview(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    session_ID = '-1'
    flag = False
    if 'sessionID' in dic.keys():
        session_ID = dic['sessionID']
        flag = True
    username = dic['username']
    py.sign_in('miladb', 'xqZ3cjrIhsHF9YPV8XFY')  # Replace the username, and API key with your credentials.
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return "ERRORhaha - " + str(e)
    if cursor.rowcount != 1:
        return "ERROR - UserID isnt Correct"
    user_id = str(cursor.fetchone()[0])
    try:
        if flag == False:
            qu = "SELECT startTime, finishTime, sessionID FROM sessions WHERE sessions.userID="+user_id+" order by finishTime desc;"
        else:
            qu = "SELECT startTime, finishTime, sessionID FROM sessions WHERE sessions.sessionID=" + session_ID + ";"
        cursor.execute(qu)
    except Exception as e:
        return "ERRORhaha - " + str(e)
    (startTime, finishTime,sessionID) = cursor.fetchone()
    cursor.execute("select activityTime, speed from activity WHERE activity.userID="+user_id+" AND activity.activityTime < '"+ str(finishTime)+"' AND activity.activityTime > '"+str(startTime)+"';")
    rows = cursor.fetchall()

    # build Visulanum

    if cursor.rowcount > 1:
        df = pd.DataFrame([[ij for ij in i] for i in rows])
        df.rename(columns={0: 'activityTime', 1: 'speed'}, inplace=True)
        df = df.sort_values(['activityTime'], ascending=[1])
        trace1 = go.Scatter(
            x=df['activityTime'],
            y=df['speed'],
            mode='lines+markers',
            name='speed'
        )

        layout = go.Layout(
            title='Your Session Speed Overview',
            xaxis=dict(title='Time'),
            yaxis=dict(title='speed  (cm/s)')
        )
    else:
        df = pd.DataFrame([[ij for ij in i] for i in [[]]])
        df.rename(columns={0: 'activityTime', 1: 'speed'}, inplace=True)
        #df = df.sort_values(['activityTime'], ascending=[1])
        trace1 = go.Scatter(
            x=[0],
            y=[0],
            mode='lines+markers',
            name='speed'
        )

        layout = go.Layout(
            title='Your Session Speed Overview',
            xaxis=dict(title='Time'),
            yaxis=dict(title='speed  (cm/s)')
        )

    data = [trace1]
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename="Machine-speed"+str(sessionID)+".png")
    image_data = open("Machine-speed"+str(sessionID)+".png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
def useraccoverview(request):
    try:
        dic = QueryDict(request.get_full_path().split('?')[1]).dict()
        session_ID = '-1'
        flag = False
        if 'sessionID' in dic.keys():
            session_ID = dic['sessionID']
            flag = True
        username = dic['username']
        py.sign_in('miladb', 'xqZ3cjrIhsHF9YPV8XFY')  # Replace the username, and API key with your credentials.
        conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
        cursor = conn.cursor()
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return "ERRORhaha - " + str(e)
    if cursor.rowcount != 1:
        return "ERROR - UserID isnt Correct"
    user_id = str(cursor.fetchone()[0])
    try:
        if flag == False:
            qu = "SELECT startTime, finishTime, sessionID FROM sessions WHERE sessions.userID="+user_id+" order by finishTime desc;"
        else:
            qu = "SELECT startTime, finishTime, sessionID FROM sessions WHERE sessions.sessionID=" + session_ID + ";"
        cursor.execute(qu)
    except Exception as e:
        return "ERRORhaha - " + str(e)
    try:
        (startTime, finishTime,sessionID) = cursor.fetchone()
        cursor.execute("select activityTime, acc from activity WHERE activity.userID="+user_id+" AND activity.activityTime < '"+ str(finishTime)+"' AND activity.activityTime > '"+str(startTime)+"';")
    except Exception as e:
        return "Hon"
    rows = cursor.fetchall()
    if cursor.rowcount > 1:
        df = pd.DataFrame([[ij for ij in i] for i in rows])
        df.rename(columns={0: 'activityTime', 1: 'acc'}, inplace=True)
        df = df.sort_values(['activityTime'], ascending=[1])
        trace1 = go.Scatter(
            x=df['activityTime'],
            y=df['acc'],
            mode='lines+markers',
            name='acc'
        )

        layout = go.Layout(
            title='Your Session Acceleration Overview',
            xaxis=dict(title='Time'),
            yaxis=dict(title='acc  (cm/s^2)')
        )
    else:
        df = pd.DataFrame([[ij for ij in i] for i in [[]]])
        df.rename(columns={0: 'activityTime', 1: 'acc'}, inplace=True)
        # df = df.sort_values(['activityTime'], ascending=[1])
        trace1 = go.Scatter(
            x=[0],
            y=[0],
            mode='lines+markers',
            name='acc'
        )

        layout = go.Layout(
            title='Your Session Acceleration Overview',
            xaxis=dict(title='Time'),
            yaxis=dict(title='ACC  (cm/s^2)')
        )
    data = [trace1]
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig, filename="Machine-acceleration"+str(sessionID)+".png")
    image_data = open("Machine-acceleration"+str(sessionID)+".png", "rb").read()
    return HttpResponse(image_data, content_type="image/png")
def getnumberofrepeats(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    session_ID = '-1'
    flag = False
    if 'sessionID' in dic.keys():
        session_ID = dic['sessionID']
        flag = True
    username = dic['username']
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return HttpResponse("ERRORhaha - " + str(e))
    if cursor.rowcount != 1:
        return HttpResponse("ERROR - UserID isnt Correct")
    user_id = str(cursor.fetchone()[0])
    try:
        if flag == False:
            qu = "SELECT repeats FROM sessions WHERE sessions.userID=" + user_id + " order by finishTime desc;"
        else:
            qu = "SELECT repeats FROM sessions WHERE sessions.sessionID=" + session_ID + ";"
        cursor.execute(qu)
    except Exception as e:
        return "ERRORhaha - " + str(e)
    try:
        repeats = cursor.fetchone()
        return HttpResponse(str(repeats[0]))
    except:
        return HttpResponse('0')


def realtimerepeats(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    username = dic['username']
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return HttpResponse("ERRORhaha - " + str(e))
    if cursor.rowcount != 1:
        return HttpResponse("ERROR - UserID isnt Correct")
    user_id = str(cursor.fetchone()[0])
    try:
        qu = "SELECT startTime, sessionID FROM sessions WHERE sessions.userID=" + user_id + " AND sessions.finishTime is NULL;"
        cursor.execute(qu)
    except Exception as e:
        return HttpResponse("ERRORhaha - " + str(e))
    try:
        (startTime, sessionID) = cursor.fetchone()
        cursor.execute(
            "select direction from activity WHERE activity.userID=" + user_id + " AND activity.activityTime > '" + str(startTime) + "';")
        rows = cursor.fetchall()
        counter = 0
        if len(rows) >= 1:
            curr_direction = str(rows[0][0])
            for direction in rows:
                if curr_direction is None:
                    curr_direction = str(direction[0])
                elif direction[0] is not None:
                    if str(direction[0]) != str(curr_direction):
                        counter += 1
                        curr_direction = str(direction[0])
        return HttpResponse(str(int(counter)/2))
    except:
        return HttpResponse(" ")

def getnumberofsets(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    session_ID = '-1'
    flag = False
    if 'sessionID' in dic.keys():
        session_ID = dic['sessionID']
        flag = True
    username = dic['username']
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return HttpResponse("ERRORhaha - " + str(e))
    if cursor.rowcount != 1:
        return HttpResponse("ERROR - UserID isnt Correct")
    user_id = str(cursor.fetchone()[0])
    try:
        if flag == False:
            qu = "SELECT sets FROM sessions WHERE sessions.userID=" + user_id + " order by finishTime desc;"
        else:
            qu = "SELECT sets FROM sessions WHERE sessions.sessionID=" + session_ID + ";"
        cursor.execute(qu)
    except Exception as e:
        return "ERRORhaha - " + str(e)
    try:
        sets = cursor.fetchone()
        return HttpResponse(str(sets[0]))
    except:
        return HttpResponse('0')


def userhistory(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    username = dic['username']
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return HttpResponse("None")
    if cursor.rowcount != 1:
        return HttpResponse("None")
    user_id = str(cursor.fetchone()[0])
    try:
        qu = "SELECT sessionID, machineID, startTime, finishTime FROM sessions WHERE sessions.userID=" + user_id + ";"
        cursor.execute(qu)
    except Exception as e:
        return HttpResponse("None")
    USER_SESSIONS_DICT={}
    sessions = cursor.fetchall()
    try:
        for session in sessions:
            session_date = str(session[2]).split(' ')[0]
            try:
                qu = "SELECT name, park FROM machine WHERE machine.machineID=" + str(session[1]) + ";"
                cursor.execute(qu)
            except Exception as e:
                return HttpResponse("None")
            inner_cursor = cursor.fetchone()
            machine_name = str(inner_cursor[0])
            park_id = str(inner_cursor[1])
            try:
                qu = "SELECT location FROM park WHERE park.parkID=" + str(park_id) + ";"
                cursor.execute(qu)
            except Exception as e:
                return HttpResponse("None")
            park_inner_cursor = cursor.fetchone()
            park_details = str(park_inner_cursor[0])
            session_time = str(round(float(((datetime.datetime.strptime(str(session[3]), "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(str(session[2]), "%Y-%m-%d %H:%M:%S")).total_seconds())/60.0),2))
            USER_SESSIONS_DICT[str(session[0])] = (machine_name, park_details, session_time, session_date)
    except Exception as e:
        return HttpResponse("None")
    final_response = ""
    try:
        str_keys_list = USER_SESSIONS_DICT.iterkeys()
        int_keys_list = [int(x) for x in str_keys_list]
        int_keys_list.sort(reverse=True)
        for sess in int_keys_list:
            final_response += str(sess) + " -"+str(USER_SESSIONS_DICT[str(sess)][3])+" (" +str(USER_SESSIONS_DICT[str(sess)][2]) + " minutes) @ " +str(USER_SESSIONS_DICT[str(sess)][0]) + " ," +str(USER_SESSIONS_DICT[str(sess)][1]) + "\n"
        return HttpResponse(final_response)
    except Exception as e:
        return HttpResponse("None")

def getcalories(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    session_ID = '-1'
    flag = False
    if 'sessionID' in dic.keys():
        session_ID = dic['sessionID']
        flag = True
    username = dic['username']
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return HttpResponse("ERRORhaha - " + str(e))
    if cursor.rowcount != 1:
        return HttpResponse("ERROR - UserID isnt Correct")
    user_id = str(cursor.fetchone()[0])
    try:
        if flag == False:
            qu = "SELECT calories FROM sessions WHERE sessions.userID=" + user_id + " order by finishTime desc;"
        else:
            qu = "SELECT calories FROM sessions WHERE sessions.sessionID=" + session_ID + ";"
        cursor.execute(qu)
    except Exception as e:
        return "ERRORhaha - " + str(e)
    try:
        calories = cursor.fetchone()
        return HttpResponse(str(calories[0]))
    except:
        return HttpResponse('0')


def getnsessiontime(request):
    dic = QueryDict(request.get_full_path().split('?')[1]).dict()
    session_ID = '-1'
    flag = False
    if 'sessionID' in dic.keys():
        session_ID = dic['sessionID']
        flag = True
    username = dic['username']
    conn = MySQLdb.connect(host="localhost", user="miladb", passwd="db789*", db="Gym")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
    except Exception as e:
        return HttpResponse("ERRORhaha - " + str(e))
    if cursor.rowcount != 1:
        return HttpResponse("ERROR - UserID isnt Correct")
    user_id = str(cursor.fetchone()[0])
    try:
        if flag == False:
            qu = "SELECT startTime, finishTime FROM sessions WHERE sessions.userID=" + user_id + " order by finishTime desc;"
        else:
            qu = "SELECT startTime, finishTime FROM sessions WHERE sessions.sessionID=" + session_ID + ";"
        cursor.execute(qu)
    except Exception as e:
        return "ERRORhaha - " + str(e)
    try:
        time = cursor.fetchone()
        start_time = str(time[0])
        finish_time = str(time[1])
        session_time = str((datetime.datetime.strptime(finish_time,
                                                       "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S")).total_seconds())
        return  HttpResponse(session_time)

    except:
        return HttpResponse('0')






