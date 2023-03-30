import random

# This class sets all related to living together in an apartment
class WgLeben:
    def __init__(self): #in call function?
        self.leben = {}
        self.leben['ordentlich'] = None
        self.leben['kochen'] = None
        self.leben['einkaufen'] = None
        self.leben['not_zweck_wg'] = None
        self.leben['haustier'] = None
        self.leben['rauchen'] = None
        self.leben['vegetarian'] = None
        
    # return: list with things apartment doesn't want in user
    def noGo(self): # not in use
        return []

    # set random values to variables
    def generate_random(self):
        self.leben['ordentlich'] = random.choice([True, False]) # ob die wg/person ordentlich ist
        self.leben['kochen'] = random.choice([True, False]) # gemeinsam kochen/nicht
        self.leben['einkaufen'] = random.choice([True, False]) # gemeinsam enikaufen/nicht
        self.leben['not_zweck_wg'] = random.choices([True, False], weights=[0.9, 0.1])[0] # ob man was zusammen unternimmt
        if self.leben['not_zweck_wg']:
            self.gemeinsam = random.sample(["hacer fiesta", "tener noche de cine", "tener noche de juegos", "cocinar juntos", "tarde de café", "comer fuera", "salir a pasear", "salir de fiesta"],2)
        self.leben['haustier'] = random.choice([True, False]) # ob man eins haben kann
        self.leben['rauchen'] = random.choice([True, False]) 
        self.leben['vegetarian'] = random.choice([True, False])
        return self
        
    # return: unknown variable's key
    def unknown(self):
        list_keys = [key for key in self.leben if self.leben[key] == None]
        if len(list_keys) == 0:
          return None
        else: 
          return random.choice(list_keys)

    # ---- return text messages ----
    # return: text neat (or not)
    def getNeat(self):
        if self.leben['ordentlich']: 
            return "la limpieza y el orden son importantes para nosotros. "
        return "somos bastante desordenados.  "

    # return: text cooking together (or not)
    def getCooking(self):
        if self.leben['kochen']:
            return "nos gusta cocinar juntos. "
        return "cada uno cocina para sí mismo. "
    
    # return: text groceries together (or not)
    def getGroceries(self):
        if self.leben['einkaufen']: 
            return "tenemos un plan de compras. "
        return "cada uno compra para sí mismo. "

    # return: things to do together (or not)
    def getTogether(self):
        if self.leben['not_zweck_wg']: 
            return "nos gusta {} y {} juntos. ".format(self.gemeinsam[0],self.gemeinsam[1])
        return "cada uno pasa el tiempo por su cuenta. "

    # return: if pets are allowed in apartment
    def getPet(self): 
        if self.leben['haustier']:
            return "estamos de acuerdo con mascotas. "
        return "tengo una alergia contra pelusas y no admitimos mascotas. "
    
    # return: if smoking is allowed in the apartment
    def getSmoke(self):
        if self.leben["rauchen"]:
            return random.choice(["estamos de acuerdo con fumadores. ", "Algunos de nosotros fumamos. "])
        return "no estamos de acuerdo con fumadores. En este piso no se fuma. "

    # return: eating habits (vegetarian, vegan. etc.)
    def getVeggie(self):
        if self.leben["vegetarian"]:
            return random.choice(["todos somos veganos. ", "Todos somos vegetarianos. ", "Algunos de nosotros somos veganos. ", "Algunos de nosotros somos vegetariaons. "])
        return random.choice(["comemos carne y pescado. ", "No comemos carne, pero sí pescado. "])