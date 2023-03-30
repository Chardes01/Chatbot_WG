import random

# This class creates a person with specific variables
class Person:
    def __init__(self):
        # dictionary with all info about a person
        self.characteristics = {}
        self.characteristics['name'] = None # string: name of individual
        self.characteristics['age'] = None # int: age of individual
        self.characteristics['job'] = [None,None] # string: name of job. "NO" if they don't work
        self.characteristics['education'] = None # string: study name
        self.characteristics['hobbies'] = None # string (list?): hobbies
        #self.characteristics['social'] = None
        self.characteristics['presence'] = None # bool
        self.characteristics['wg-experience'] = None # bool
        self.list_educations = ["Profeción docente", "Medicina", "Ley", "Medicina veterinaria", "Historia", "ADE", "Matemáticas", "Informática", "Deportes", "Biología", "Ingeniería mecánica", "Geografía", "Inglés", "Química", "Farmacia"]
        
    # use:      user data
    # returns:  a random characteristic that doesn't have a value yet 
    #           None if all characteristics are known
    def unknown(self):
        list_keys = [key for key in self.characteristics if self.characteristics[key] == None or (key == 'job' and not self.characteristics[key][0] == False and self.characteristics[key][1] == None)]
        if len(list_keys) == 0:
          return None
        else: 
          return random.choice(list_keys)

    # use:      initialisation for apartment people
    # returns:  self
    def initialize_random(self):
        self.characteristics['name'] = random.choice(["Juan", "Jose", "Hugo", "Pablo", "Àlvaro", "Javier", "Diego", "Mateo", "Santiago", "Joaquín", "Pedro", "Juan", "Enrique", "Nicolas", "Norberto", "Guzmán", "Miguel", "Alejandro", "Daniel", "Sebastian", "Alberto", "Cayetano", "Martin", "Rafael", "Francisco", "Gustavo", "Gabriel", "Samuel", "Ivan", "Ander", "Valerio", "Armando", "Christian", "Omar", "Nano", "Nando", "Benjamín", "Raúl", "César", "Lorenzo", "Rodolfo", "Sergio", "Álex", "Carlos", "Bruno", "Marcos", "Adrian", "María", "María Antonia", "María Jose", "María Paz", "Lucía", "Paula", "Elena", "Andrea", "Isabel", "Martina", "Elisa", "Antonia", "Manuela", "Claudia", "Rosa", "Cayetana", "Emilia", "Azucena", "Valentina", "Christina", "Camila", "Clara", "Rafaela", "Luciana", "Marian", "Gabriella", "Micaela", "Miguela", "Carla", "Rebeca", "Marina", "Nadia", "Rocío", "Sara", "Marifer", "Sofía", "Marta", "Lucía", "Valeria", "Luna", "Ana", "Ana Paula", "Adriana", "Lia", "Alma", "Alba"]) # list of spanish names, doppelt oder nicht belegen
        self.characteristics['age'] = random.choice(range(18,30))
        list_jobs = ["cartero/a", "profesor/-a", "maestro/a", "tutor/-a", "vendedor/-a", "camarero/a", "cocinero/a", "trabajador/a manual", "fisioterapeuta", "enfermero/a", "asistente médico/a", "secretario/a", "entrenador/-a", "educador/-a", "pedagogo/a", "jardinero/a", "peluquero/a"]
        job_exist = random.choices([False, True], weights=[0.3,0.7])[0]
        if job_exist:
            self.characteristics['job'] = [True, random.choice(list_jobs)]
        else:
            self.characteristics['job'] = [False,False]
        self.characteristics['education'] = random.choice(self.list_educations)
        self.characteristics['hobbies'] = random.choice(["tocar el piano", "leer", "escuchar música", "jugar al fútbol", "bailar", "jugar al balonmano", "jugar al baloncesto", "quedar con amigos"])
        self.characteristics['presence'] = random.choice([True, False])
        self.characteristics['wg-experience'] = random.choice([True, False])
        return self

    # variable person: boolean, true if 1st person, false if anything else
    # return: string, name of person
    def getName(self, person=True):
        if person: 
            return random.choice(["me llamo {}. ", "mi nombre es {}. ", "soy {}. "]).format(self.characteristics['name'])
        else: 
            return self.characteristics['name']
    
    # variable person: boolean, true if 1st person, false if anything else
    # return: string, age or person
    def getAge(self, person=True):
        if person:
            return "tengo {} años. ".format(str(self.characteristics['age']))
        else: 
            return str(self.characteristics['age'])

    # variable person: boolean, true if 1st person, false if anything else
    # return: string, if person has a job & the job they have
    def getJob(self, person=True):
        if person: 
            if self.characteristics['job'][0]:
                return random.choice(["mi profesión es {}. ", "trabajo como {}. "]).format(self.characteristics['job'][1])
            else: 
                return "yo no trabajo. "
        else: 
            if self.characteristics['job'][0]:
                return self.characteristics['job'][1]
            else:
                return ""

    # variable person: boolean, true if 1st person, false if anything else
    # return: string, what person studies
    def getEducation(self, person=True):
        if person:
            return "Estudio {}.".format(self.characteristics['education'])
        else: 
            return self.characteristics['education']

    # variable person: boolean, true if 1st person, false if anything else
    # return: string, the hobby of person
    def getHobbies(self, person=True):
        if person:
            return random.choice(["en mi tiempo libre me gusta {}. ", "mi hobby es {}. "]).format(self.characteristics['hobbies'])
        else: 
            return self.characteristics['hobbies']

    # variable person: boolean, true if 1st person, false if anything else
    # return: string, if person plans on staying at the appartment regularily of plans on being absent 
    def getPresence(self, person=True): 
        if person:
            if self.characteristics['presence']:
                return random.choice(["voy a pasar mucho tiempo en el piso. ", "pasaré la mayoría de los fines de semana en el piso compartido. "])
            else:
                return 'no'
        else: 
            return self.characteristics['presence']
                
    # return: string, person has experience 
    def getExperience(self):
        if self.characteristics['wg-experience'] == True:
            return 'yes'
        else:
            return 'no'

