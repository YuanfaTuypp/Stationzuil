"""In deze module kunnen reizigers een bericht achterlaten, deze worden weggeschreven naar een csv bestand"""

import random
import  datetime
from datetime import datetime

# Importeren van datetime om zo met datums en tijden te kunnen werken in CLI
now = datetime.now()
dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
print("date " + dt_string)
datum = now.strftime("%m/%d/%Y")
tijd = now.strftime("%H:%M:%S")

huidige_tijd = datetime.now()

# Openen van het stationsbestand en het kiezen van een willekeurig station
with open(f'stations.txt', 'r') as file:
    stations = file.read()
    lijst = list(map(str, stations.split()))

locatie = random.choice(lijst)

# Op basis van de tijd bepalen we het bericht dat de reiziger krijgt te zien
if 0 <= huidige_tijd.hour < 12:
    groet = ("Goedemorgen! U bevindt zich op Station " + locatie)
elif 12 <= huidige_tijd.hour < 18:
    groet = ("Goedemiddag! U bevindt zich op Station " + locatie)
else:
    groet = ("Goedenavond! U bevindt zich op Station " + locatie)

# Weergave van de begroeting aan de reizigers
print(groet)

# Optionele invoer van de naam van de reiziger
naam = input('Voer uw naam in (of druk op Enter om anoniem te blijven):\n')
if not naam:
    naam = 'Anoniem' # Als er geen naam wordt ingvuld, wordt het anoniem

# Invoer van het bericht door de reiziger met een limiet van 140 tekens
while True:
    bericht = input(f'Hallo {naam}, voer hier uw bericht in (max 140. tekens):\n')

    if len(bericht) > 140:
        print('Je hebt meer dan 140 tekens gebruikt. Probeer het opnieuw!')
    else:
        break

# Open het csv bestand en sla de informatie op
f=open("stationzuil.csv", 'a')
f.write(f'{naam};{bericht};{datum};{tijd};{locatie} \n')
f.close()


print("Uw bericht is ontvangen, bedankt!")
#Feedback eerste poging command lines, 140 tekens max . Aanvullende delen inleveren. + github pushcommit alles