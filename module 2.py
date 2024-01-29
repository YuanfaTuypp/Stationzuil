from datetime import datetime
import psycopg2

# Vragen naar moderatornummer en naam
# Als de mail en naam niet kloppen word er opnieuw gevraagd
while True:
    moderatornummer = int(input('Voer je moderator nummer in:\n'))
    naam = input('Voer je naam in:\n')

    # Verbinden met sql database
    connection_string = "host='172.187.132.139' dbname='stationzuil' user='postgres' password='Aardappel25@'"
    with psycopg2.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            # zoek in sql of moderatornummer en naam overeenkomen/bestaan
            moderatornummer1 = "SELECT moderatornummer FROM moderator WHERE naam = %s;"
            cursor.execute(moderatornummer1, (naam,))
            result = cursor.fetchone()

            if result:
                # Als naam en nummer overeen komen, open de berichten
                moderatornummer_database = result[0]
                if moderatornummer == moderatornummer_database:
                    print('Berichten worden geopend:\n')
                    file = open("stationzuil.csv", 'r')
                    list = file.readlines()
                    file.close()

                    for bericht in list:
                        #  'sep=;' verdeeld het csv bestand met ';'
                        if bericht != 'sep=;\n':
                            bericht = bericht.strip().split(';')
                            print(bericht)
                            print(f'naam:{bericht[0]}, bericht:\n{bericht[1]}')
                            beoordeling = input('Bericht goedkeuren of afkeuren?\n')

                            # Als er wat anders staat dan een van de keuzes word er opnieuw gevraagd
                            while beoordeling != 'goedkeuren' and beoordeling != 'afkeuren':
                                beoordeling = input('Onjuiste keuze, probeer het nog maals!\n')

                            naam = bericht[0]
                            test = bericht[1]
                            datum = bericht[2]
                            tijd = bericht[3]
                            station = bericht[4]

                            now = datetime.now()
                            beoordelingsdatum = now.strftime("%m/%d/%Y")
                            beoordelingstijd = now.strftime("%H:%M:%S")


                            # Voeg data toe in sql database
                            query = """INSERT INTO Bericht (moderatornummer, naam, datum, tijd, station, bericht, beoordeling, beoordelingsdatum, beoordelingstijd) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
                            data = (
                                moderatornummer, naam, datum, tijd, station, test, beoordeling, beoordelingsdatum,
                                beoordelingstijd)
                            cursor.execute(query, data)

                    with open("stationzuil.csv", 'w') as file:
                        file.write("sep=;\n")

                # komt niet overeen, afsluiten
                else:
                    print('Moderatornummer bestaat niet of moderatornummer komt niet overeen met uw naam. \nOpnieuw aub.')

            # komt niet overeen, afsluiten
            else:
                print('Moderatornummer bestaat niet of moderatornummer komt niet overeen met uw naam. \nOpnieuw aub.')
    break
print('Dat waren alle berichten, dankjewel.')

