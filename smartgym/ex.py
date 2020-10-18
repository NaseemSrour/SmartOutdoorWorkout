from django.http import HttpResponse
from django.http import QueryDict
import json
import MySQLdb
import datetime
from django.views.decorators.csrf import csrf_exempt
REPORT_ALLOWED_ARGUMENTS = ['MACHINEID', 'SPEED', 'TIMEINTERVAL','DIR', 'ACC']


"""
def ValidateAcc(dict_values,acc_cursor):
    for arg in dict_values.keys():
        if str(arg).upper() not in ACC_ALLOWED_ARGUMENTS:
            return "ERROR - didnt recognize some Arguments please review Your request"
    #for arg in ACC_ALLOWED_ARGUMENTS:
    #    if arg not in list(dict_values.keys()):
    #        return HttpResponse("ERROR - argument : " + arg +"  is missing , please review your request")
    try:
        float(dict_values['acc'])
    except Exception as e:
        return "ERROR - ACC Argument Value is not Correct"
    try:
        acc_cursor.execute("SELECT machine.name FROM machine WHERE machine.machineID=" + dict_values['machineID'] + ";")
    except Exception as e:
        return "ERRORhaha - " + str(e)
    if acc_cursor.rowcount != 1:
        return "ERROR - Machine ID isnt Correct"
    try:
        # get User ID
        acc_cursor.execute("SELECT sessions.userID FROM sessions, activity WHERE "
                           "sessions.machineID=" + str(dict_values['machineID']) + " "
                           "AND activity.activityTime > sessions.startTime"
                           "  AND (activity.activityTime < sessions.finishTime OR sessions.finishTime IS NULL);")
        if acc_cursor.rowcount > 1:
            return "ERROR - Error founf in Sessions To many User in The Same machine"
        elif acc_cursor.rowcount == 1:
            comnd = "INSERT INTO activity(activityTime, machine, userID, speedTimeInterval, speed, acc, direction) \
             VALUES('" + str(datetime.datetime.now()) + "','" + str(dict_values['machineID']) + "','"+ str(acc_cursor.fetchone()[0]) +"', \
            NULL, NULL,'" + str(dict_values['acc']) + "', NULL);"
        else:
            comnd = "INSERT INTO activity(activityTime, machine, userID, speedTimeInterval, speed, acc, direction)\
             VALUES('" + str(datetime.datetime.now()) + "','" + str(dict_values['machineID']) + "',NULL, \
            NULL, NULL,'" + str(dict_values['acc']) + "', NULL);"
    except Exception as e:
        return "ERROR - While Parsing argument values" + str(e)
    try:
        acc_cursor.execute(comnd)
    except Exception as e:
        return "ERROR - While Inserting activity to DB  " + str(e) + comnd
    return "OK"
"""

def ValidateAndHandleReport(dict_values, speed_cursor):
    #X.X.X.X / ArduinoTesting / speed?machineID = xyxyxyxy & speed = xx & timeInterval = xxs & dir = UP/ DOWN
    for arg in dict_values.keys():
        if str(arg).upper() not in REPORT_ALLOWED_ARGUMENTS:
            return "ERROR - didnt recognize some Arguments please review Your request"
    try:
        float(dict_values['speed'])
    except Exception as e:
        return "ERROR - speed Argument Value is not Correct" + str(e)
    try:
        float(dict_values['acc'])
    except Exception as e:
        return "ERROR - ACC Argument Value is not Correct" + str(e)
    try:
        speed_cursor.execute("SELECT machine.name FROM machine WHERE machine.machineID=" + dict_values['machineID'] + ";")
    except Exception as e:
        return "ERROR -" + str(e)
    if speed_cursor.rowcount != 1:
        return "ERROR - Machine ID isnt Correct"
    try:
        # get User ID
        speed_cursor.execute("SELECT DISTINCT sessions.userID FROM sessions WHERE "
                           "sessions.machineID=" + str(dict_values['machineID']) + " "
                           "AND '" + str(datetime.datetime.now()) + "' > sessions.startTime"
                           "  AND ('" + str(datetime.datetime.now()) + "' < sessions.finishTime OR sessions.finishTime IS NULL);")
        if speed_cursor.rowcount > 1:
            return "ERROR - Error founf in Sessions To many User in The Same machine"
        elif speed_cursor.rowcount == 1:
            comnd = "INSERT INTO activity(activityTime, machine, userID, speedTimeInterval, speed, acc, direction) \
             VALUES('" + str(datetime.datetime.now()) + "','" + str(dict_values['machineID']) + "','"+ str(speed_cursor.fetchone()[0]) + "', \
            '" + str(dict_values['timeInterval']) + "', '" + str(dict_values['speed']) + "','" + str(dict_values['acc']) + "','" + str(dict_values['dir']) + "');"
        else:
            comnd = "INSERT INTO activity(activityTime, machine, userID, speedTimeInterval, speed, acc, direction)\
             VALUES('" + str(datetime.datetime.now()) + "','" + str(dict_values['machineID']) + "',NULL, \
            '" + str(dict_values['timeInterval']) + "', '" + str(dict_values['speed']) + "','" + str(dict_values['acc']) + "','" + str(dict_values['dir']) + "');"
    except Exception as e:
        return "ERROR - While Parsing argument values" + str(e)
    try:
        speed_cursor.execute(comnd)
    except Exception as e:
        return "ERROR - While Inserting activity to DB  " + str(e) + comnd
    return "OK"



"""
reporting for a speed during Time Interval 
X.X.X.X /ArduinoTesting/speed?machineID=xyxyxyxy&speed=xx&timeInterval=xxs&acc=xx
"""
def report(request):
    try:
        if request.method != 'GET':
            return HttpResponse("Please Provide The Server with GET HTTP request according to the Format")
        mydb = MySQLdb.connect("localhost", "db_username", "db_password", "db_name")
        speed_cursor = mydb.cursor()
        message = ValidateAndHandleReport(QueryDict(request.get_full_path().split('?')[1]).dict(), speed_cursor)
        mydb.commit()
        speed_cursor.close()
        mydb.close()
        return HttpResponse(message)
    except Exception as e:
        return HttpResponse(str(e))


def validate_sign_up(sign_up_cursor, body):
    """
    username , password , firstname , lastname , age , height , weight
    :return:
    """
    try:
        param_dict = dict(eval(body))
        username = param_dict["username"]
        password = param_dict["password"]
        first_name = param_dict["firstname"]
        last_name = param_dict["lastname"]
        age = param_dict["age"]
        height = param_dict["height"]
        weight = param_dict["weight"]

        # check if username already used..
        sign_up_cursor.execute("SELECT users.ID FROM users WHERE users.username='" + username + "';")
        if sign_up_cursor.rowcount == 1:
            return "User Already Exist"
        try:
            if not first_name.isalpha() or not last_name.isalpha() or int(age) > 100 or int(age) < 0 \
                    or float(height) < 0 or float(weight) < 0:
                return "WRONG ARGUMENTS"
        except Exception:
            return "WRONG ARGUMENTS"

        insert_query = "INSERT INTO users(fname, lname, age, weight, height, username, password)" \
                       " VALUES('" + first_name + "', '" + last_name + "', " + age + ", " + weight + ", " + height + ",\
                        '" + username+ "', '" + password + "');"
        try:
            sign_up_cursor.execute(insert_query)
        except Exception as e:
            return "ERROR - While Inserting User to DB  " + str(e) + insert_query
    except Exception as e:
        return "ERROR While Parsing ARGS / DB Inserting : ---> " + str(e)
    return "User Added Successfully"


@csrf_exempt
def signup(request):
    try:
        if request.method != 'POST':
            return HttpResponse("Please Provide The Server with GET HTTP request according to the Format")
    except:
        return HttpResponse("Something Went Wrong!")
    mydb = MySQLdb.connect("localhost", "db_username", "db_password", "Gym")
    sign_up_cursor = mydb.cursor()
    result = validate_sign_up(sign_up_cursor, request.body)
    mydb.commit()
    sign_up_cursor.close()
    mydb.close()
    return HttpResponse(result)


def validate_sign_in(sign_in_cursor, body):
    """
    username , password
    :return: @str : User Found / User Not Found
    """
    try:
        param_dict = dict(eval(body))
        username = param_dict["username"]
        password = param_dict["password"]
        sign_in_cursor.execute("SELECT users.ID FROM users WHERE username='" + username + "' AND\
                                                                           password='" + password +"';")
        if sign_in_cursor.rowcount == 1:
            return "User Found"
    except Exception as e:
        #return "ERROR IN PARSING PARAMETERS OR SELECTING FROM DB : -- > " + str(e)
        return body + str(e)
    return "User Not Found"


@csrf_exempt
def signin(request):
    try:
        if request.method != 'POST':
            return HttpResponse("Please Provide The Server with POST HTTP request according to the Format")
    except:
        return HttpResponse("Something Went Wrong!")
    mydb = MySQLdb.connect("localhost", "miladb", "db789*", "Gym")
    sign_in_cursor = mydb.cursor()
    result = validate_sign_in(sign_in_cursor, request.body)
    mydb.commit()
    sign_in_cursor.close()
    mydb.close()
    return HttpResponse(result)  # result = User Found / User Not Found


def HandleStartSession(dict_val, cursor):
    try:
        for key in dict_val.keys():
            if key != "machineID" and key != "username":
                return "Error with request Format"
        machineID = dict_val['machineID']
        username = dict_val['username']
        cursor.execute("SELECT users.ID FROM users WHERE username='" + username + "';")
        if cursor.rowcount != 1:
            return "User Not Found"
        user_ID = str(cursor.fetchone()[0])
        cursor.execute("SELECT machine.machineID FROM machine WHERE machineID=" + machineID + ";")
        if cursor.rowcount != 1:
            return "Machine Not Found"
        insert_query = "INSERT INTO sessions(userID, startTime, finishTime,machineID) VALUES('" + user_ID + "', '" + str(datetime.datetime.now()) + "', NULL, " + machineID + ");"
    except Exception as e:
        return "ERROR - " + str(e)
    try:
        cursor.execute(insert_query)
        return "Thank You."
    except Exception as e:
        return "ERROR - While Inserting User to DB " + str(e)


@csrf_exempt
def startsession(request):
    try:
        if request.method != 'GET':
            return HttpResponse("Please Provide The Server with GET HTTP request according to the Format")
    except:
        return HttpResponse("Something Went Wrong!")
    try:
        mydb = MySQLdb.connect("localhost", "db_username", "db_password", "db_name")
        start_session_cursor = mydb.cursor()
        message = HandleStartSession(QueryDict(request.get_full_path().split('?')[1]).dict(), start_session_cursor)
        mydb.commit()
        start_session_cursor.close()
        mydb.close()
        return HttpResponse(message)
    except Exception as e:
        return HttpResponse(str(e))


def HandleEndSession(dict_val, cursor):
    try:
        for key in dict_val.keys():
            if key != "machineID" and key != "username" and key != "sets" and key != "repeats":
                return "Error with request Format"
        machineID = dict_val['machineID']
        username = dict_val['username']
        number_of_sets = 0
        number_of_repeats = 0
        try:
            number_of_sets = int(dict_val['sets'])
            number_of_repeats = int(dict_val['repeats'])
        except:
            pass
        try:
            cursor.execute("SELECT users.ID, weight FROM users WHERE username='" + username + "';")
            if cursor.rowcount != 1:
                return "User Not Found"
            user = cursor.fetchone()
            user_ID = str(user[0])
            user_weight = 0
            user_weight = int(str(user[1]))
            cursor.execute("SELECT machine.machineID FROM machine WHERE machineID=" + machineID + ";")
        except Exception as e:
            return "kokowawa"
        if cursor.rowcount != 1:
            return "Machine Not Found"
        cursor.execute("SELECT sessions.sessionID FROM sessions WHERE machineID=" + machineID + " AND userID='" + user_ID +"' AND finishTime is NULL;")
        if cursor.rowcount != 1: # change to != 1 when develop
            return "SESSION Not Found"
        session_ID = str(cursor.fetchone()[0])
        total_calories = (0.0925*user_weight*number_of_repeats) / 15
        update_query = "UPDATE sessions SET finishTime ='" + str(datetime.datetime.now()) + "', sets = " + str(number_of_sets) + ", repeats = "+str(number_of_repeats)+", calories="+str(total_calories)+" WHERE sessionID=" + str(session_ID) + ";"

    except Exception as e:
        return "ERRORkiki - " + str(e)
    try:
        cursor.execute(update_query)
        return "Done"
    except Exception as e:
        return "ERROR - While Inserting User to DB " + str(e)


@csrf_exempt
def endsession(request):
    try:
        if request.method != 'GET':
            return HttpResponse("Please Provide The Server with GET HTTP request according to the Format")
    except:
        return HttpResponse("Something Went Wrong!")
    try:
        mydb = MySQLdb.connect("localhost", "db_username", "db_password", "db_name")
        end_session_cursor = mydb.cursor()
        message = HandleEndSession(QueryDict(request.get_full_path().split('?')[1]).dict(), end_session_cursor)
        mydb.commit()
        end_session_cursor.close()
        mydb.close()
        return HttpResponse(message)
    except Exception as e:
        return HttpResponse(str(e))


"""
Reporting for new activity and movment in the machine
X.X.X.X/Arduino/acc?machineID=xyxyxyxy&acc=xxx

def acc(request):
    try:
        if request.method != 'GET':
            return HttpResponse("Please Provide The Server with GET HTTP request according to the Format")
        mydb = MySQLdb.connect("localhost", "db_username", "db)password", "db_name")
        acc_cursor = mydb.cursor()
        message = ValidateAcc(QueryDict(request.get_full_path().split('?')[1]).dict(), acc_cursor)
        mydb.commit()
        acc_cursor.close()
        mydb.close()
        return HttpResponse(message)
    except Exception as e:
        return HttpResponse(str(e))
"""

