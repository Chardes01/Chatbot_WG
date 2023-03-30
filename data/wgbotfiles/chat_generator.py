import random
from .wg import WG
import re

# This chat generates the response of the bot
class Chat_generator:
    def __init__(self,wg):
        self.memory = []
        self.experience_question = []
        self.key = None
        self.possibleKeys = { # list of possible words for every key
            'name':["nombre", "llam"], 
            'age': ["edad", "años", "anos"],
            'vegetarian': ["vegetarian", "vegan", "carne", "pescado"],
            'job' : ['trabaj', "carrera"],
            'education': ['educacion', "estudia", "educación"],
            'hobbies' :[ "pasatiempos", "tiempo libre"],
            "presence": ['presente'],
            'wg-experience':['experience', "experiencia"],
            'ordentlich':["limpio", "orden" ],
            "kochen": ["cocinar"],
            "einkaufen":["compra"],
            "not_zweck_wg":["juntos"],
            "haustier":["mascota", "perro", "perra", "gato"],
            "rauchen":["fuma", "tabaco"],
            "wg-properties": ["persona", "banos", "baños", "salon", "salón", "living", "kitchen", "cocina ", "habitación", "habitacion", "jardin", "jardín", "garten", "terraza", "balcón", "balcon", "wifi", "cuesta", "localiza", "transport","cuesta", "costa"]}
        #self.numPerson = None
        self.dictQuests = {
            "name": ["¿Cómo te llamas? ", "¿Cuál es tu nombre? "],
            "age": ["¿Cuántos años tienes? ", "¿Qué edad tienes? "],
            "job": ["¿En qué trabajas? ", "¿Cuál es tu profesión? "],
            "jobExist": ["¿Tienes trabajo?"],
            "education": ["¿Qué estás estudiando? ", "¿Qué estudias? "],
            "hobbies": ["¿Cuáles son sus hobbies?", "¿Qué haces en tu tiempo libre? "],
            "presence": ["Planeas estar en el piso regularmente? "],
            "wg-experience": ["¿Ya tienes experiencia en pisos compartidos? ", "¿Has vivido ya en un piso compartido? "],
            "ordentlich": ["¿Te importa la limpieza?", "¿Te importa el orden?"],
            "kochen": ["¿Te gusta cocinar con otros? ", "¿Te gusta cocinar en equipo? "],
            "einkaufen": ["¿Te gusta hacer la compra para la casa?"], 
            "not_zweck_wg": ["¿Buscas un piso para fiestas?", "¿Estás buscando un piso para fiestas?", "¿Planeas pasar tiempo con nosotros en el piso?"],
            "haustier": ["¿Tienes una mascota?"],
            "rauchen": ["¿Eres una pesona fumadora?"],
            "vegetarian": ["¿Eres una persona vegetariana?"]
        }
        self.füllwörter = ['hola','si', 'absolutamente', 'seguro', 'claro', 'como no','sì','sí','siempre','no', 'para nada', 'que va','buen','bien','perfect']
        self.wg = wg
        self.name = ["nombre", "llam"]
        self.nachfragen = False
        self.keys = self.wg.get_all_keys()
        self.already_answered = {}
        self.already_asked = {}
        for key in self.keys:
            self.already_answered[key] = False
            self.already_asked[key] = 0
        self.first_key = False
        self.end = False
        self.time = 0
        self.ok_or_not = False
        
    
    # return: random question to a random keyword
    def question(self):
        self.first_key = True
        if not len(self.memory) == 0:
            key = self.memory[0]
            self.memory.pop(0)
        else:
            key = self.wg.getKey()
    
        while key and self.already_asked[key] >= 2: 
            self.wg.setUserValue(key, "no information")
            key = self.wg.getKey()

        if key:
            del self.keys[self.keys.index(key)]
            self.keys.insert(0, key)
            self.already_asked[key] += 1
            
            if key == 'job' and not self.wg.getUserValue(key)[0]:
                key = 'jobExist' #ändern zu jobExist
            
            return random.choice(self.dictQuests[key])

        else:
            self.end = True
            return ""

    # return: last text of chatbot
    def endText(self):
        counter = 0
        counter_alike = 0
        for key in self.wg.getWünsche().leben:
            if not self.wg.getWünsche().leben[key] == "no information":
                counter += 1
                if self.wg.getWünsche().leben[key] == self.wg.getLife().leben[key]:
                    counter_alike += 1
        if counter < 0.5 * len(self.wg.getLife().leben) or counter_alike < 0.5*counter:
            return "creo que no encajamos, pero gracias por tu interés "
        else:
            return "creo que eres la persona que buscamos. Pásate mañana por el piso. Te esperamos! "

    # answer: text from user
    # return: if answer of user is responded as true or false
    def true_false_cases(self, answer):
        false_expressions = ['no', 'para nada', 'que va', 'de ninguna manera']
        for s in false_expressions:
            if re.search(s, answer.lower()):
                return False

        true_expressions = ['si', 'absolutamente', 'seguro', 'claro', 'como no', 'sì', 'sí', 'siempre', 'por que no']
        for s in true_expressions:
            if re.search(s, answer.lower()):
                return True

        return None

    # answer: text from user
    # return: list of keys in answer of user
    def getKeys(self, answer):
        listOfKeys = []
        
        for key in self.possibleKeys:
            if key == 'wg-properties':
                for x in self.possibleKeys[key]:
                    if re.search(x, answer.lower()):
                        listOfKeys.append(x)
            else:
                x_key = False
                if re.search(key, answer.lower()):
                    x_key = True
                for x in self.possibleKeys[key]:
                    if re.search(x, answer.lower()):
                        x_key = True

                if x_key:
                    listOfKeys.append(key)

        return listOfKeys

    # key: keyword the text of user has
    # answer: text of user
    # fist_key: boolean, if key is also general key
    # return: value of variable from user text
    def search_sentence(self, key, answer, first_key):
        value = None
        behind = None
        answer = answer.lower()
        #standart antworten abfragen: No, si...,quatsch antworten
        # -- NAME ANALISIS --
        if key == 'name':

            expressions = ['me llamo', 'mi nombre es', 'soy ([A-Za-z]+)']
            for s in expressions:
                if re.search(s, answer):
                    value =  re.sub(r'.*(' + s + r' )([A-Za-z]+(\b|$))(.*)',r'\2', answer)
                    return value
            if first_key:
                reg_name = r'(\W*)(\w+)((\W*)|(\W*)y t(u|ú|ù)[?]*(\W*))$'
                m = re.match(reg_name, answer)
                if m:
                    if m.start() == 0 and m.end() == len(answer):
                        return re.sub(reg_name, r'\2', answer)
                    
        # -- AGE ANALISIS --
        if key == 'age':
            ex2 = []
            if first_key:
                reg_name = r'(\W*)([0-9]+)((\W*)|(\W*)y t(u|ú|ù)[?]*(\W*))$'
                m = re.match(reg_name, answer)
                if m:
                    if m.start() == 0 and m.end() == len(answer):
                        return re.sub(reg_name, r'\2', answer)
                else: ex2 = ['tengo ([0-9]+)']
            
            expressions = ['tengo ([0-9]+) a(ñ|n)os','soy ([0-9]+)()'] + ex2
            for s in expressions:
                if re.search(s, answer):
                    value =  re.sub(r'.*' + s + r'(.*)',r'\1', answer)
                    return value

        # -- JOB ANALISIS --
        if key == 'job':
            value_1 = self.wg.getUserValue(key)[0] 
            value_2 = value_1
            reg_name = []
            if first_key:
                if value_1 == None:
                    value_2 = self.true_false_cases(answer)
                reg_name = ['(como)','(en)']
            
            if not value_2 == False:    
                expressions = ['mi profesi(ó|o)n es','trabajo (como)'] + reg_name
                for s in expressions:
                    if re.search(s,answer):
                        value =  re.sub(r'.*' + s + r' (la |el )?([A-Za-z]+(\b|$))(.*)',r'\3', answer)
                        return [True,value]
            if value_1 != value_2 and value_2 == False:
                return [False, False]
            if value_1 != value_2 and value_2 == True:
                self.memory.append('job')
                return [True, None]
            return None

        # -- EDUCATION ANALISIS --
        if key == 'education':
            if first_key:
                list_of_studies = self.wg.get_list_of_studies() + ["cognitive science"]
                for study in list_of_studies:
                    study = study.lower()
                    m = re.search(study, answer)
                    if m:
                        return study
          
            expressions = ['estudio'] 
            for s in expressions:
                if re.search(s,answer):
                    value =  re.sub(r'.*(' + s + r' )([A-Za-z]+(\b|$))(.*)',r'\2', answer)
                    return value

        # -- HOBBY ANALISIS --
        if key == 'hobbies':
            expressions = ['en mi tiempo libre', 'mis hobbies son', 'me gusta']
            for s in expressions:
                if re.search(s, answer):
                    return True

        # -- OTHER KEYS ANALISIS --
        if key == 'presence' or key == 'wg-experience' or key == 'ordentlich' or key == 'kochen' or key == 'einkaufen' or key == 'not_zweck_wg' or key == 'haustier' or key == 'rauchen' or key == 'vegetarian':
            if first_key and self.ok_or_not:
                value = self.true_false_cases(answer)
                if value:
                    return self.wg.getLife().leben[key]
                if value == False:
                    return bool(1-self.wg.getLife().leben[key])
            if first_key:
                return self.true_false_cases(answer)
    
    # values: str, values of response of user
    # return: reaction from answers of user
    def react_on_user_answer(self, values):
        question = False
        reaction = ""
        tell_property = False
        keys = []
        for key in values:
            tell = False
            
            # -- NAME RESPONSE --
            if key == 'name':
                if self.time != 1:
                    reaction += "alright "
                tell = True
                reaction += values[key].capitalize() + ", "

            # -- AGE RESPONSE --
            if key == 'age':
                tell = random.choice([True,False])

                try:
                    user_age_str = values[key]
                    user_age = int(user_age_str)
                    ages = []
                    for num in range(self.wg.getPeopleInt()):
                        ages.append(self.wg.getBewohnerValue(num,'age'))
                    
                    if user_age < min(ages):
                        reaction += "eres la persona más joven, "
                    elif user_age == min(ages):
                        reaction += "eres de las personas más jovenes, "
                    elif user_age > max(ages):
                        reaction += "eres la persona más mayor, "
                    elif user_age == max(ages):
                        reaction += "eres de las personas más mayores, "
                    else:
                        reaction += "entonces eres de nuestra edad, "
                
                except ValueError:
                    reaction += "bueno, "

            # -- JOB RESPONSE --
            if key == 'job':
                if values[key][0] and not values[key][1]:
                    reaction += "que bien, " + self.question()
                    question = True
                else: 
                    tell = random.choice([True,False])

                if not values[key][0]:
                    reaction += "asi te puedes enfocar mas en los estudios, "
                if values[key][1]:
                    reaction += values[key][1] + " suena como un buen trabajo, "
            
            # -- EDUCATION RESPONSE --
            if key == 'education':
                tell = random.choice([True,False])
                reaction += values[key] + random.choice([" me parece muy interesante. ", "... no creo que podría estudiarlo."])
            
            # -- HOBBY RESPONSE --
            if key == 'hobbies':
                tell = random.choice([True,False])
                reaction += random.choice(["eso a mi tambien me gusta. ", "suena interesante. "]) #keine ahnung was man da schreiben soll
            
            # -- EXPERIENCE RESPONSE --
            if key == 'experience':
                tell = True
            
            # -- PRESENCE RESPONSE --
            if key == 'presence':
                counter = 0
                for x in range(self.wg.getPeopleInt()):
                    if self.wg.getResidents(x).getPresence(False):
                        counter += 1
                if counter >= (self.wg.getPeopleInt())*0.66:
                    reaction += "nos gusta pasar el tiempo juntos. "
                else: 
                    reaction += "nos gusta ser mas independientes. "

            # -- OTHER KEYWORDS RESPONSES --
            if key == 'ordentlich' or key == 'kochen' or key == 'einkaufen' or key == 'not_zweck_wg' or key == 'haustier' or key == 'rauchen' or key == 'vegetarian':
                tell = True
                if values[key] == self.wg.getLife().leben[key]:
                    reaction += "bueno, "
                else: reaction += "que pena... "
                    
            # -- TRUE/FALSE RESPONSES --
            if tell and not self.already_answered[key]:
                    keys.append(key)
                    tell_property = True

        return reaction, tell_property, keys, question
                                
    # return: standart response if the sentence of user wasn't understood
    def not_understood(self):
        if not self.nachfragen:
            self.nachfragen = True #um nur einmal nachzufragen und nicht mehrmals
            list_of_questions = ["¿Puedes repetir en otras palabras? No te he entendido. "]
            return True,random.choice(list_of_questions)
        else: 
            return False,""
            
    # answer: text of user
    # return: regognises the person in which the answer is written (to know in which person the response should be adressed as)
    def getPerson(self,answer):
        answer = answer.lower()
       
        #if mitbewohner name oder ihr oder dein mitbewohner return 3
        numPerson2s = [' tu', ' tus', ' te']
        numPerson2p = [' vuestra', ' vuestro', ' vuestras', ' vuestros', ' vosotros', ' vosotras']
        numPerson3s = [' su', ' sus', ' se', ' él', ' ella',' compa(n|ñ)er(o|a)'] + self.wg.get_names_bewohner()
        numPerson3p = [' ellas',' ellos', ' os', 'compa(n|ñ)er(o|a)s']
        
        for num in numPerson2p:
            if re.search(num, answer):
                return (num,2)
        
        for num in numPerson3p:
            if re.search(num, answer):
                return (num,4)

        for num in numPerson3s:
            if re.search(num, answer):
                return (num,3)

        for num in numPerson2s:
            if re.search(num, answer):
                return (num,1)

        return (None,1)      
   
    # answer: text of user
    # return: process answer and generate a matching response
    def process_answer(self, answer): # auch unabhängig vom key?
        if self.time == 0:
            response = "Hola "
        else: response = ""
        self.time += 1
        response_behind = ""
        question = False
        nothing = True
        values = {}
        understood= False

        # store information of user
        for key in self.keys:
            user_value = self.search_sentence(key, answer, self.first_key)
            self.first_key = False
            if not user_value == None:
                understood = True
                self.wg.setUserValue(key, user_value)
                values[key] = user_value
        self.ok_or_not = False
        tell_property = False
        keys = []
        other_keys = []

        if re.search("gracias", answer.lower()):
            response += "De nada. "

    	# write reaction if understood
        if understood:
            reaction, tell_property, keys, question =  self.react_on_user_answer(values)
            response += reaction
            if len(response) >= 1:
                response = response[0].capitalize() + response[1:]

        # when questions are raised or if answer was not understandable
        if re.search(r'[?]', answer) or not understood:
            other_keys = self.getKeys(answer) # or not understood: or in behind and
        
        if tell_property:
            for key in keys.__reversed__():
                if key not in other_keys:
                    other_keys.insert(0,key)  
            
        if len(other_keys) == 0 and re.search(r'[?]', answer):
            other_keys = [self.keys[0]]

        elif len(other_keys) == 0 and response == "":
            if re.search("interes", answer.lower()) or self.time <= 2:
                        other_keys.append("interes")
            else:
                for x in self.füllwörter:
                    if re.search(x, answer.lower()):
                        other_keys.append('füllwörter')
                        break
        
        name_mates, person_original = self.getPerson(answer)
        random_tell = True
        counter_random_tell = 0

        # messages for facts about the apartment
        while(random_tell):
            understood = True
            random_tell = False
            
            for key in other_keys:
                response_1 = ""
                person = person_original

                # ---- KEYWORDS TO PERSON ---- 
                # Name of User
                if key == 'nombre' or key == "llam" or key == 'name':
                    self.already_answered['name'] = True
                    # first person sentence
                    if person == 1:
                        response_1 += self.wg.getResidents(0).getName()
                    
                    # first person sentence + plural
                    if person == 2:
                        response_1 += self.wg.getResidents(0).getName()[:-2] + " y mis compañeros de piso "
                        person = 4
                    
                    # first person plural sentence
                    if person == 3:
                        person = 4

                    # third person plural sentence
                    if person == 4: 
                        response_1 += "se llaman "
                        for x in range(1,self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1: 
                                response_1 += "y " + self.wg.getResidents(x).getName(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getName(False) + ", "
                    
                # Age of User
                elif key == 'edad' or key == "años" or key == 'age' or key == "anos":
                    # first person sentence
                    if person == 1:
                        self.already_answered['age'] = True
                        response_1 += self.wg.getResidents(0).getAge()

                    # second person plural sentence
                    if person == 2:
                        response_1 += "somos "
                        for x in range(self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1: 
                                response_1 += "y " + self.wg.getResidents(x).getAge(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getAge(False) + ", "
                    
                    # third person sentence
                    if person == 3:
                        list_names = self.wg.get_names_bewohner()
                        if name_mates in list_names:
                            index = list_names.index(name_mates) + 1
                            response_1 += name_mates + " tiene " + self.wg.getResidents(index).getAge(False) + 'años. '
                        else:
                            person = 4
            
                    # third person plural sentence
                    if person == 4:
                        response_1 += "mis compañeros de piso son "
                        for x in range(1,self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1: 
                                response_1 += "y " + self.wg.getResidents(x).getAge(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getAge(False) + ", "

                # Does user have a job?/ job of the WG
                elif key == 'trabaj' or key == 'job' or key == "carrera":
                    self.already_answered['job'] = True
                
                    if person == 1:
                        self.already_answered['job'] = True
                        response_1 += self.wg.getResidents(0).getJob()
                    
                    if person == 2:
                        response_1 += self.wg.getResidents(0).getJob()[:-2] + " y mis compañeros de piso "
                        person = 4
                    
                    if person == 3:
                        list_names = self.wg.get_names_bewohner()
                        if name_mates in list_names:
                            index = list_names.index(name_mates) + 1
                            response_1 += name_mates 
                            if self.wg.getResidents(index).getJob(False) != "":
                                response_1 += " trabaja como " + self.wg.getResidents(index).getJob(False) + '. '
                            else: 
                                response_1 += " no trabaja. "
                        else:
                            person = 4
                    
                    if person == 4:
                        jobs = ""
                        for x in range(1,self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1 and self.wg.getResidents(x).getJob(False) != "": 
                                jobs += "y " + self.wg.getResidents(x).getName(False) + " como " + self.wg.getResidents(x).getJob(False) + '. '
                            elif self.wg.getResidents(x).getJob(False) != "": 
                                jobs += self.wg.getResidents(x).getName(False) + " como " + self.wg.getResidents(x).getJob(False) + ", "
                        if jobs == "":
                            jobs = "nadie de ellos trabaja. "
                        response_1 += jobs
                    
                
                # education
                elif key == 'educacion' or key == "estudia" or key == 'education' or key == "educación":
                    if person == 1:
                        self.already_answered['education'] = True
                        response_1 += self.wg.getResidents(0).getEducation()

                    if person == 2:
                        response_1 += "estudiamos "
                        for x in range(self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1: 
                                response_1 += "y " + self.wg.getResidents(x).getEducation(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getEducation(False) + ", "

                    if person == 3:
                        list_names = self.wg.get_names_bewohner()
                        if name_mates in list_names:
                            index = list_names.index(name_mates) + 1
                            response_1 += name_mates + " estudia " + self.wg.getResidents(index).getEducation(False) + '. '
                        else:
                            person = 4
                        
                    if person == 4:
                        response_1 += "estudian "
                        for x in range(1, self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1: 
                                response_1 += "y " + self.wg.getResidents(x).getEducation(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getEducation(False) + ", "

                # Hobbies of user/WG
                elif key == 'hobbies' or key == "pasatiempos" or key == "tiempo libre":
                    if person == 1: 
                        self.already_answered['hobbies'] = True
                        response_1 += self.wg.getResidents(0).getHobbies()

                    if person == 2:
                        response_1 += "nos gusta "
                        for x in range(self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1:  
                                response_1 += "y " + self.wg.getResidents(x).getHobbies(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getHobbies(False) + ", "
                    if person == 3:
                        list_names = self.wg.get_names_bewohner()
                        if name_mates in list_names:
                            index = list_names.index(name_mates) + 1
                            response_1 += "A " + name_mates + " le gusta " + self.wg.getResidents(index).getHobbies(False) + '. '

                    if person == 4:
                        response_1 += "les gusta "
                        for x in range(1,self.wg.getPeopleInt()):
                            if x == self.wg.getPeopleInt()-1: 
                                response_1 += "y " + self.wg.getResidents(x).getHobbies(False) + '. '
                            else: 
                                response_1 += self.wg.getResidents(x).getHobbies(False) + ", "

                # How much time do they plan on interacting in the WG
                elif key == 'presente' or key == "presence":
                    self.already_answered['presence'] = True
                    if person == 1:
                        response_1 += self.wg.getResidents(0).getPresence()
                    if person == 2:
                        person = 4
                    if person == 3:
                        person = 4
                    if person == 4:
                        counter = 0
                        for x in range(self.wg.getPeopleInt()):
                            if self.wg.getResidents(x).getPresence(False):
                                counter += 1
                        if counter >= (self.wg.getPeopleInt())*0.66:
                            response_1 += "nos gusta pasar el tiempo juntos. "
                        else: 
                            response_1 += "nos gusta ser mas independientes. "

                # Experience in WG
                elif key == 'experience' or key == 'wg-experience' or key == "experiencia":
                    self.already_answered['experience'] = True
                    if not self.wg.getUserValue('wg-experience') == True: 
                        counter = 0
                        for x in range(self.wg.getPeopleInt()):
                            if self.wg.getResidents(x).getPresence(False):
                                counter += 1
                        if counter >= self.wg.getPeopleInt()*0.66:
                            response_1 += "no te preocupes, te enseñamos lo básico. "
                        else: 
                            response_1 += "algunos de nosotros tampoco tuvimos experiencia previa, pero ahora nos va bien. "
                    else: "experiencia nunca viene mal :D "

                # ---- KEYWORDS TO WG INFORMATION ----
                # -- Only output
                # Number of people living
                elif key == "persona":
                    response_1 += self.wg.getPeople()
                # Number of bathrooms in WG
                elif key == "banos" or key == "baños":
                    response_1 += self.wg.getBathroom()
                # Number of livingrooms
                elif key == "salon" or key == "salón" or key == "living":
                    response_1 += self.wg.getLiving()
                # Kitchen text
                elif key == "cocina ": 
                    response_1 += self.wg.getKitchen()
                # Room text
                elif key == "habitación" or key == "habitacion":
                    response_1 += self.wg.getRoomDim()
                elif key == "cuesta" or key == "costa":
                    response_1 += self.wg.getPrice()
                # Garten text
                elif key == "jardin" or key == "jardín":
                    response_1 += self.wg.getGarten()
                # Balcon text
                elif key == "terraza" or key == "balcón" or key == "balcon":
                    response_1 += self.wg.getBalcon()
                # Wifi text
                elif key == "wifi":
                    response_1 += self.wg.getWiFi()
                # Location text
                elif key == "localiza":
                    response_1 += self.wg.getLocation()
                # Transport text
                elif key == "transport":
                    response_1 += self.wg.getTransport()

                # ---- Live in the WG ----
                # Keyword neat/tidy
                elif key == "limpio" or key ==  "orden" or key == "ordentlich":
                    self.already_answered['ordentlich'] = True
                    response_1 += self.wg.getLife().getNeat()
                elif key == "cocinar" or key == "kochen":
                    self.already_answered['kochen'] = True
                    response_1 += self.wg.getLife().getCooking()
                elif key == "compra" or key == "einkaufen":
                    response_1 += self.wg.getLife().getGroceries()
                    self.already_answered['einkaufen'] = True
                elif key == "juntos" or key == "not_zweck_wg":
                    response_1 += self.wg.getLife().getTogether()
                    self.already_answered['not_zweck_wg'] = True
                elif key == "mascota" or key == "perro" or key == "perra" or key == "gato" or key =="haustier":
                    response_1 += self.wg.getLife().getPet()
                    self.already_answered['haustier'] = True
                elif key == "fuma" or key == "tabaco" or key == "rauchen":
                    response_1 += self.wg.getLife().getSmoke()
                    self.already_answered['rauchen'] = True
                elif key == "vegetarian" or key == "vegan" or key == "carne" or key == "pescado" or key == "vegetarian":
                    response_1 += self.wg.getLife().getVeggie()
                    self.already_answered['vegetarian'] = True
                elif key == "interes": 
                    response_1 += "me alegra saber que te interesa el cuarto. Vamos a hablar un poco mas para ver si conviviríamos bien! "
                elif key == "füllwörter":
                    nothing = False
                    response_1 += "entonces... "
                else:
                    response_1 += ""

                if not response_1 == "":
                    response += response_1[0].capitalize() + response_1[1:]
            
            if response == "":
                understood = False

            weights = [0.2, 0.1, 0.5, 0.2]
            
            # if answer was not understood, ask again
            if not understood:
                ask_again, ask_again_question = self.not_understood()
                if not ask_again:
                    understood = True
                    weights = [0.4, 0.2, 0.4, 0]                    
                elif not self.end:
                    response = ask_again_question

            # make a question or encourage user to ask something
            if understood and counter_random_tell < 1:
                if not nothing:
                    weights = [0.4, 0.1, 0.5, 0]
                self.nachfragen = False
                case = random.choices([1, 2, 3, 4], weights=weights)[0]

                if case == 1 and not self.end and not question:
                    list_life = [i for i in self.wg.getLife().leben if not self.already_answered[i]]
                    if len(list_life) == 0:
                        case = random.choices([2, 3], weights=[0.2, 0.8])[0]
                    else: 
                        life_key = random.choice(list_life)
                        other_keys = [life_key]
                        random_tell = True
                        counter_random_tell += 1
                        response_behind = "¿Está bien para ti?"
                        self.ok_or_not = True
                        self.first_key = True
                        del self.keys[self.keys.index(life_key)]
                        self.keys.insert(0, life_key)

                if case == 2 and not self.end and not question:
                    response += "Si quieres saber algo mas sobre la vivienda puedes preguntar ahora. "

                if case == 3 and not self.end and not question: 
                    response += self.question() 
    
        response = response + response_behind
        
        if self.end:
            response += self.endText()
        
        return response, self.end
        

