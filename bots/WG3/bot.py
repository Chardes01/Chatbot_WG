from data.wgbotfiles.wg import WG
from data.wgbotfiles.chat_generator import Chat_generator
import jsonpickle

# This class initiates a bot
class Bot:

    name = 'WG3'
    avatar = 'avatar/wg3.jpg'
        
    # if first time in chat, give the flat advertisment
    def welcome(self, session):
        session.data['end'] = False
        wg = WG(num=5,kitchen=1,space=18,price=390)
        wg_encoded = jsonpickle.encode(wg)
        session.data['wg'] = wg_encoded
        chat_generator = Chat_generator(wg)
        chat_encoded = jsonpickle.encode(chat_generator)
        session.data['chat_generator'] = chat_encoded
        return """Buscamos un compañero/ una compañera de piso. En nuestro piso compartido, una habitación bonita quedará libre a partir del 01.10.23, porque nuestra compañera María Jose se va de la ciudad para hacer un máster.
                La habitación tiene 18m2 y cuesta 390€ (todos los gastos incluidos: electricidad, gas, internet). Vivirías con 4 compañeros. El piso está situado cerca de la universidad.
                Esperamos tu mensaje si nuestro anuncio te parece atractivo."""

    # last_user_message: text message from user
    # return: bot text message
    def chat(self, last_user_message, session):
        if not session.data['end']:
            wg_encoded = session.data['wg']
            wg = jsonpickle.decode(wg_encoded)
            chat_encoded = session.data['chat_generator']
            chat_generator= jsonpickle.decode(chat_encoded)

            answer,end = chat_generator.process_answer(last_user_message)

            if end:
                session.data['end'] = True
            wg_encoded = jsonpickle.encode(wg)
            session.data['wg'] = wg_encoded
            chat_encoded = jsonpickle.encode(chat_generator)
            session.data['chat_generator'] = chat_encoded
            
            return answer,False

        else:
            return "",True
            
