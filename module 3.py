from tkinter import *
import tkinter as tk
import psycopg2
import requests
import random

# met tkinter zien we een scherm
root = tk.Tk()
root.title('NS Stationhal scherm')
root.state('zoomed')
root.configure(bg='#FFC917')

# verbinden met sql database
connection_string = "host='172.187.132.139' dbname='stationzuil' user='postgres' password='Aardappel25@'"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor()

def get_random_station():
    # random een station halen om laten zien waar de klanten nu zijn
    cursor.execute("SELECT station FROM bericht ")
    stations = cursor.fetchall()
    return random.choice(stations)[0]

def update_label():
    # station met weer en tempuratuur. Hier gebruikt API en Label
    global random_station, label
    random_station = get_random_station()

    api_key = '6d731359b48effba425c7f0c3fc66e15'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={random_station}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    weather = data["weather"][0]["description"]
    temperatuur_kelvin = data["main"]["temp"]
    temperatuur = int(temperatuur_kelvin - 273.15)

    weerstation.config(text=f'{weather},\n{temperatuur}°C')
    label.config(text=f"Beste reizigers \nWelkom op station {random_station}")

weerstation = tk.Label(root, font=("Arial", 16), fg="#003082", text="")
weerstation.pack(padx=20, pady=20)

label = tk.Label(root, text="", bg="light yellow", fg="#003082", font=("Arial", 26))
label.pack(padx=20, pady=20)

update_label()


# verbinden met sql database en informatie uithalen over bericht
cursor = conn.cursor()
cursor.execute( """ SELECT naam, datum, tijd, station, bericht from bericht WHERE beoordeling = 'goedkeuren'
ORDER BY datum ASC, tijd ASC LIMIT 5 """)

result = cursor.fetchall()

for row in result:

    naam=row[0]
    datum=row[1]
    tijd=row[2]
    station=row[3]
    bericht=row[4]


    # met frame een rechthoek krijgen voor teksten
    my_frame = tk.Frame(root, borderwidth=2)
    my_frame.pack(padx=20, pady=20, side=LEFT)

    label1 = tk.Label(my_frame, font=("Arial", 12), bg="#FFC917", fg="#003082", text=f'{naam}  {datum},{tijd} \n {station}')
    label1.pack(side=tk.TOP, padx=10)

    label_with_image = tk.Label(my_frame)


    # informatie uithalen over faciliteiten van station
    cursor.execute(""" SELECT ov_bike, elevator, park_and_ride, toilet from station_service WHERE station_city = %s""",(station,))
    result = cursor.fetchall()


    image1 = PhotoImage(file='fiets1.png')
    image2 = PhotoImage(file='lift1.png')
    image3 = PhotoImage(file='pr1.png')
    image4 = PhotoImage(file='wc1.png')
    image_list = [image1, image2, image3, image4]

    label_list = []


    # zoek naar of faciliteiten wel of niet bij de stations horen, tellen met 'cnt'
    cnt = 0
    for i in result:
        for j in i:
            if j:
                if 0 <= cnt < len(image_list):
                    image = image_list[cnt]
                    label = tk.Label(my_frame, image=image)
                    label.image = image
                    label.pack(padx=0.1, pady=0.1)
                    label_list.append(label)
                else:
                    print("Invalid index: ", cnt)
            cnt += 1


    # station van berichten met weer en temperatuur
    city = station
    api_key = '6d731359b48effba425c7f0c3fc66e15'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(url)
    data = response.json()

    weather = data["weather"][0]["description"]
    temperatuur_kelvin = data["main"]["temp"]

    temperatuur = int(temperatuur_kelvin - 273.15)

    weer=tk.Label(my_frame, font=("Arial", 12), fg="#003082", text=f'{weather},\n{temperatuur}°C')
    weer.pack()

    label2 = tk.Label(my_frame, font=("Arial", 16), bg="#FFC917", fg="#003082", text=f'{bericht}', relief="solid",
                      width=20, height=10, wraplength=200, justify="left")
    label2.pack(padx=10)

# afsluiten
root.mainloop()
