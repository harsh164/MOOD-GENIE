import serial
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ['https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('pis2019-1d8caca8db36.json', scope)

client = gspread.authorize(credentials)

sheet = client.open('Pis').sheet1


lst_for_happy_a = []  # I might not use this  (a=Heart rate)
for i in range(80, 121):
    lst_for_happy_a.append(i)
lst_for_neutral_a = []
for i in range(60, 80):
    lst_for_neutral_a.append(i)
lst_for_stress_a = []
for i in range(100, 130):
    lst_for_stress_a.append(i)

lst_for_happy_b = []  # I might not use this   (b=GSR sensor)
for i in range(400, 600):
    lst_for_happy_b.append(i)
lst_for_neutral_b = []
for i in range(100, 200):
    lst_for_neutral_b.append((i))
lst_for_stress_b = []
for i in range(300, 400):
    lst_for_stress_b.append(i)

lst_for_happy_c = []  # I might not use this    (c=temperature)
start_happy = 28
step = 0.01
lst_for_happy_c = [start_happy + (x*step) for x in range(0, 400)]
lst_for_neutral_c = []
start_neutral = 30
lst_for_neutral_c = [start_neutral+(x*step) for x in range(0, 100)]
lst_for_stress_c = []
start_stress = 31
lst_for_stress_c = [start_stress+(x*step) for x in range(0, 120)]


def find(element, lst):
    for i in lst:
        if i == lst:
            return True
    return False


try:

    ar = serial.Serial(port='COM6', baudrate=9600)

except Exception:

    ar = serial.Serial('COM4', baudrate=9600)

while True:

    out = (ar.readline().split())

    file = open('pis_project', 'w')
    a = out[2]
    a = int(a.decode('utf-8'))

    #  a = float(out[:index])  # you have to look to it

    #  out = float(out[index + 1:])
    #  index = out.find(",")

    b = out[0]
    b = int(b.decode('utf-8'))

    c = out[1]
    c = float(c.decode('utf-8'))

    a_find_neutral = find(a, lst_for_neutral_a)
    b_find_neutral = find(b, lst_for_neutral_b)
    c_find_neutral = find(c, lst_for_neutral_c)

    a_find_stress = find(a, lst_for_stress_a)
    b_find_stress = find(b, lst_for_stress_b)
    c_find_stress = find(c, lst_for_stress_c)

    a_find_happy = find(a, lst_for_happy_a)
    b_find_happy = find(b, lst_for_happy_b)
    c_find_happy = find(c, lst_for_happy_c)

    if a_find_happy and b_find_happy and c_find_happy:
        file.write("Happy")
        MOD = "happy"
        print("Happy")

    elif a_find_stress and b_find_stress and c_find_stress:
        file.write("Stress")
        MOD = "stress"
        print("Stress")

    else:
        file.write("Neutral")
        print("Neutral")
        MOD = "neutral"
    """payload = {'MOOD': MOD, 'BPM':a, 'TEMP':c, 'GSR':b}
    resp = requests.post("https://my-json-server.typicode.com/VaibhavGupta-19341/PIS_Major_Project/posts", json=payload)
    #  print(resp.json())"""
    print("here")
    row = [a, b, c, MOD]
    print("hello")
    print(row)
    try:
        sheet.insert_row(row, 2)
    except Exception:
        time.sleep(10)
