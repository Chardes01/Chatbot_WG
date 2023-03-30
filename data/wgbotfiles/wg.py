import random
from .person import Person 
from .wgLeben import WgLeben

# This class sets and returns everything related to physical variables of the apartment
class WG:
    # initialisation of information about apartment
    def __init__(self, num,kitchen,space,price):
        self.num = num # number of people in apartment
        self.user = Person()
        self.bewohner = [Person().initialize_random() for i in range(self.num)]
        self.badezimmer = random.choice(range(1, 4))
        self.wohnzimmer = random.choice([True, False])
        self.küche = kitchen
        self.zimmer = space # meters of room
        self.garten = random.choice([True, False])
        self.terrasse = random.choice([True, False])
        self.wlan = random.choices([True, False], weights=[0.8, 0.2])[0]
        self.preis = price# random.choice(range(250,450))
        self.lage = "centro"
        self.anbindung = random.choice(range(1, 5)) # öffentliche verkehrsmittel
        self.wgLeben = WgLeben().generate_random()
        self.wgWünsche = WgLeben()
        self.noGo = self.wgLeben.noGo()
        self.time = 0.2 #am Anfang mit größerer Wahrscheinlichkeit fragen zu person, später wg leben

    # return: get new key
    def getKey(self):
        u1 = self.user.unknown()
        u2 = self.wgWünsche.unknown()
        if u1 == None:
            key = u2
        elif u2 == None:
            key = u1
        else: 
            key = random.choices([u1,u2], weights=[1-self.time, self.time])[0]
        if self.time < 0.5:
            self.time += 0.1
        return key

    # return: list with all keys
    def get_all_keys(self):
        keys = []
        for key in self.user.characteristics:
            keys.append(key)
        for key in self.wgWünsche.leben:
            keys.append(key)
        return keys
    
    # return: list with all names in apartment
    def get_names_bewohner(self):
        names = []
        for person in self.bewohner[1:]:
            names = names + [person.characteristics['name'].lower()]
        return names

    # return: list with all possible studies of person
    def get_list_of_studies(self):
        return self.user.list_educations

    # variable key: string, keyword of characteristic list in person
    # return: value of characteristic in keyword key
    def getUserValue(self, key):
        if key in self.user.characteristics:
            return self.user.characteristics[key]
        else: 
            return self.wgWünsche.leben[key]

    # variable n: int, number of person in apartment
    # variable key: string, keyword of characteristic list in person
    # return: value of characteristic in person n in keyword key
    def getBewohnerValue(self, n, key):
        return self.bewohner[n].characteristics[key]
    
    # variable n: int, number of person in apartment
    # variable key: string, keyword of characteristic list in person
    # set value of characteristic in person n in keyword key
    def setUserValue(self, key, value):
        if key in self.user.characteristics:
            self.user.characteristics[key] = value
        else:
            self.wgWünsche.leben[key] = value

    # variable n: int, number of person in apartment
    # return: person n of apartment
    def getResidents(self, n):
        return self.bewohner[n]

    # return: class wgLeben
    def getLife(self):
        return self.wgLeben 
    
     # return: class wgLeben
    def getWünsche(self):
        return self.wgWünsche
    
    # return: number of people in apartment
    def getPeopleInt(self):
        return self.num
        
    # ---- return text messages ----
    # return: number of people in apartment
    def getPeople(self):
        return random.choice(["Es un piso compartido de {} personas. ", "Seríamos {} personas. "]).format(str(self.num+1))

    # return: number of bathrooms
    def getBathroom(self):
        if self.badezimmer == 1:
            return "Hay un baño. "
        else: 
            return "Hay dos baños. "

    # return: if there is a living room or not
    def getLiving(self):
        if self.wohnzimmer: 
            return "Hay un salón. "
        return "No hay un salón. "

    # return: text for kitchen
    def getKitchen(self):
        return "Hay una cocina con todo incluido. "

    # return: dimension of room for user
    def getRoomDim(self):
        return "La habitación tiene {} mtrs. ".format(self.zimmer)

    # return: if there is a garden
    def getGarten(self):
        if self.garten:
            return "Hay un jardín. "
        return "No hay un jardín. "

    # return: if there is a balcony
    def getBalcon(self):
        if self.terrasse:
            return random.choice(["Tenemos terraza. ", "Hay una terraza. "])
        return random.choice(["No tenemos terraza. ", "No hay terraza. "])

    # return: if there is wifi
    def getWiFi(self):
        if self.wlan:
            return random.choice(["Hay wifi. ", "Tenemos wifi. "])
        return random.choice(["No hay wifi. ", "No tenemos wifi. "])
    
    # return: price of room
    def getPrice(self):
        return random.choice(["Cuesta {} euros al mes. ", "La habitación está a {}€/mes. "]).format(self.preis)

    # return: location of apartment in around the city
    def getLocation(self):
        return random.choice(["Se encuentra en el {} de la ciudad. " ,"Está localizada en el {} de la cuidad. "]).format(self.lage)

    # return: public transport availability
    def getTransport(self):
        return random.choice(["El transporte está a {} minutos a pie. ", " La parada de metro y tranvía 'Sol' está a {} minutos. "]).format(self.anbindung)


