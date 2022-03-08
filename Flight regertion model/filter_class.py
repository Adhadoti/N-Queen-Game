import sqlite3

class filters:

    def __init__(self, to,from_):

        self._to = to
        self.departure=from_

    def search(to,from_):

        connection = sqlite3.connect("flight_info.db")
        cursor = connection.cursor()
        wildcard ='%'+from_+'%'
        wildcard2 ='%'+to+'%'

        for flights_from in cursor.execute("SELECT * FROM flight_info WHERE flight_from LIKE ? AND flight_to LIKE ?",(wildcard, wildcard2,)):
            print("{}-{}\n".format(flights_from[0],flights_from[1]))
            print("Available flights would be: \n{} airline which is on time \nprice={} \nWith {} stops\nRating={}".format(flights_from[3],flights_from[5],flights_from[2],flights_from[6]))


    def search2(to, from_,rating,price):
        count=0
        connection = sqlite3.connect("flight_info.db")
        cursor = connection.cursor()
        wildcard = '%' + from_ + '%'
        wildcard2 = '%' + to + '%'
        wildcard3 = '%' + rating + '%'
        wildcard4 = '%' + price + '%'

        for flights_from in cursor.execute("SELECT * FROM flight_info WHERE flight_from LIKE ? AND flight_to LIKE ? AND airline_rating LIKE ? AND price LIKE ?", (wildcard, wildcard2,wildcard3,wildcard4,)):
            print("{}-{}\n".format(flights_from[0], flights_from[1]))
            print("Available flights would be: \n{} airline which is on time \nprice={} \nWith {} stops\nRating={}".format(flights_from[3], flights_from[5], flights_from[2], flights_from[6]))
            count+=1

        if(count==0):
            print("There were no available flights that match the filter")


