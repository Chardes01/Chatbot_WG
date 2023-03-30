from data.wgbotfiles.wg import WG
from data.wgbotfiles.chat_generator import Chat_generator
import jsonpickle

# This class initiates a bot
class Bot:

    name = 'WG2'
    avatar = 'avatar/wg2.jpg'
        
    # if first time in chat, give the flat advertisment
    def welcome(self, session):
        session.data['end'] = False
        wg = WG(num=2,kitchen=1,space=15,price=340)
        wg_encoded = jsonpickle.encode(wg)
        session.data['wg'] = wg_encoded
        chat_generator = Chat_generator(wg)
        chat_encoded = jsonpickle.encode(chat_generator)
        session.data['chat_generator'] = chat_encoded
        return """Buscamos un compañero/ una compañera de piso. Como Julia se muda con su novio, tenemos una habitación libre en nuestro piso compartido a partir del 01.10.2023.
                La habitación tiene 15m2 y cuesta 340€ (todos los gastos incluidos: electricidad, gas, internet).Vivirías con un compañero. El piso está situado en el centro.
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
            
