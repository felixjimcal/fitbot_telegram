import enum
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import stripe
from telebot import *

from db.DBManager import *
from secret_files import pass_keys

stripe.api_key = pass_keys.pass_keys.STRIPE_TEST_API_KEY
bot = telebot.TeleBot(pass_keys.pass_keys.TELEGRAM_TEST_TOKEN)

DEMO = '🥕 Demo 🏋️'
SIGN_UP = 'Sign Up 🆕'
LOG_IN = 'Log In 👤'
DIET = 'Dieta 🥕'
ROUTINE = 'Rutina 🏋️'
PROFILE = 'Profile 👤'
SETTINGS = 'Settings ⚙️'

ACTUAL_ROUTINE = 'Actual'
CHANGE_ROUTINE = 'Change'
GO_BACK = 'Back 🔙'

FIT_BOT_EMAIL = 'fitbotweb@gmail.com'
WARNING_ROUTINE_MESSAGE = "⚠️ Advertencia ⚠️\n Esta es un rutina de ejemplo y no debe utilizarse como referencia personal."
WRONG_ANSWER = "Vaya! No es la respuesta que esperaba, probemos otra vez..."

user_message = ""
last_markup = None
is_demo = False

last_inline_keyboard = None
prev_inline_keyboard = None


class GymExperience(enum.Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


class DailyActivity(enum.Enum):
    Sentado = 1
    Moderada = 2
    Activo = 3
    MuyActivo = 4


class PlanObjective(enum.Enum):
    Bajar = 1
    Mantener = 2
    Ganar = 3


# class MuscleGroups(enum.Enum):
#     CHEST = 0
#     BACK = 1
#     ARMS = 2
#     ABS = 3
#     LEGS = 3
#     SHOULDERS = 5


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        text = "Hola, " + message.from_user.first_name + "! 👋" + "\n"
        bot.send_message(message.chat.id, text)

        global last_markup
        last_markup = new_user_welcome_markup()
        bot.send_message(message.chat.id, "¿En qué puedo ayudarte?", reply_markup=last_markup)

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Fail in main:', ex.args, 'line:', exc_tb.tb_lineno)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        global user_message
        user_message = message

        if message.text == DEMO:
            choosing_demo()
        elif message.text == LOG_IN:
            login()
        elif message.text == SIGN_UP:
            sign_up()
        elif message.text == DIET:
            if is_demo:
                demo_diet()
            else:
                pass
        elif message.text == ROUTINE:
            if is_demo:
                demo_routine()
            else:
                routine_menu()
        elif message.text == PROFILE:
            bot.send_message(message.chat.id, "Aquí van las opciones de PERFIL")
        elif message.text == SETTINGS:
            bot.send_message(message.chat.id, "Aquí van las opciones de AJUSTES")
        else:
            bot.send_message(message.chat.id, WRONG_ANSWER, reply_markup=last_markup)

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Fail in main:', ex.args, 'line:', exc_tb.tb_lineno)


def routine_menu():
    global last_markup
    last_markup = types.ReplyKeyboardMarkup()

    text = ""
    routine = DBManager.load_customer_routine(user_message.chat.id)
    if len(routine) > 0:
        pass  # TODO: Print routine
        # btn_change = types.KeyboardButton(CHANGE_ROUTINE)
        # btn_back = types.KeyboardButton(GO_BACK)
        # last_markup.row(btn_change, btn_back)
        # bot.send_message(user_message.chat.id, "Selecciona una opción:", reply_markup=last_markup)
    else:
        text += "Vamos a crear una rutina de entrenamiento. \n Por favor, responde a las siguientes preguntas:"
        bot.send_message(user_message.chat.id, text)
        routine_form()


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == '3':
        # TODO:  Devolver excel o pantallazo
        pass
    elif call.data == '4':
        # TODO:  Devolver excel o pantallazo
        pass
    elif call.data == '5':
        # TODO:  Devolver excel o pantallazo
        pass
    elif call.data == '99':
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "¿En qué puedo ayudarte?")


def routine_form():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='3 Días', callback_data=3))
    markup.add(telebot.types.InlineKeyboardButton(text='4 Días', callback_data=4))
    markup.add(telebot.types.InlineKeyboardButton(text='5 Días', callback_data=5))
    markup.add(telebot.types.InlineKeyboardButton(text='Salir', callback_data=99))
    bot.send_message(user_message.chat.id, text="Cuántos días vas a entrenar?", reply_markup=markup)

    global last_inline_keyboard
    last_inline_keyboard = markup


def new_user_welcome_markup():
    global last_markup
    last_markup = types.ReplyKeyboardMarkup()
    btn_demo = types.KeyboardButton(DEMO)
    btn_login = types.KeyboardButton(LOG_IN)
    btn_sign_up = types.KeyboardButton(SIGN_UP)
    last_markup.row(btn_demo, btn_login, btn_sign_up)
    return last_markup


def logged_user_markup():
    global last_markup
    last_markup = types.ReplyKeyboardMarkup()
    btn_diet = types.KeyboardButton(DIET)
    btn_routine = types.KeyboardButton(ROUTINE)
    btn_profile = types.KeyboardButton(PROFILE)
    btn_settings = types.KeyboardButton(SETTINGS)
    last_markup.row(btn_diet, btn_routine, btn_profile, btn_settings)
    return last_markup


def choosing_demo():
    global last_markup, is_demo
    is_demo = True
    last_markup = types.ReplyKeyboardMarkup()
    btn_diet = types.KeyboardButton(DIET)
    btn_routine = types.KeyboardButton(ROUTINE)
    last_markup.row(btn_diet, btn_routine)
    bot.send_message(user_message.chat.id, "Selecciona una opción:", reply_markup=last_markup)


def demo_diet():
    text = "Demo" + DIET
    bot.send_message(user_message.chat.id, text)

    user_gender = "Varón ♂️" if bool(random.getrandbits(1)) else "Mujer ♀️"
    user_age = random.randint(18, 65)
    user_height = random.randint(155, 200)
    user_weight = random.randint(50, 160)
    user_activity = DailyActivity(random.randint(1, 4)).name
    user_objective = PlanObjective(random.randint(1, 3)).name

    text = "Voy a asumir algunos datos... \n"
    text += "Genero: " + user_gender + '\n'
    text += "Edad: " + str(user_age) + '\n'
    text += 'Altura: ' + str(user_height) + 'cm 📏' + '\n'
    text += "Peso: " + str(user_weight) + '\n'
    text += 'Actividad diaria: ' + user_activity + '\n'
    text += user_objective + " peso" + '\n'
    text += "Margen de calorias entre 1234 - 5678"
    bot.send_message(user_message.chat.id, text)

    bot.send_message(user_message.chat.id, promo())

    global last_markup
    last_markup = new_user_welcome_markup()
    bot.send_message(user_message.chat.id, "En que puedo ayudarte?", reply_markup=last_markup)


def demo_routine():
    text = "Demo" + ROUTINE
    bot.send_message(user_message.chat.id, text)

    training_days = random.randint(3, 4)
    level = GymExperience(random.randint(1, 3)).name
    text = "Voy a asumir algunos datos... \n"
    text += "Días de gym: " + str(training_days) + "\n"
    text += "Nivel: " + level
    bot.send_message(user_message.chat.id, text)

    # TODO: Nombres ejercicios a links de video con ejemplo movimiento
    if training_days == 3:
        text = full_body_day_1() + "\n" + full_body_day_2()
    elif training_days == 4:
        if level == 1:
            text = full_body_day_1() + "\n" + full_body_day_2() + "\n" + full_body_day_3()
        elif level == 2:
            text = torso_day_1() + '\n' + pierna_day_1() + "\n" + full_body_day_3()
        else:
            text = push() + '\n' + pull() + '\n' + pierna_day_1()
    elif training_days == 5:
        text = torso_day_1() + '\n' + pierna_day_1() + '\n' + torso_day_1() + '\n' + pierna_day_1()

    text += " \n \n 1 minuto de descanso después de cada serie 🕐"
    bot.send_message(user_message.chat.id, text, parse_mode='html')  # PARSE MESSAGE FOR LINKS
    bot.send_message(user_message.chat.id, WARNING_ROUTINE_MESSAGE)

    bot.send_message(user_message.chat.id, 'Disfruta de esta y muchas ventajas disponibles como: ' + '\n' + promo())

    global last_markup
    last_markup = new_user_welcome_markup()
    bot.send_message(user_message.chat.id, "En que puedo ayudarte?", reply_markup=last_markup)


def promo():
    text = '🌮 Plan de comidas personalizado 🌯' + '\n'
    text += '📝 Lista completa de alimentos 🛒' + '\n'
    text += '🏋 Rutinas para casa 🏠 o gym' + '\n'
    text += '🤸 Plan de cardio 🏃' + '\n'
    text += '📽 Vídeos de ejercicios y técnica ✏' + '\n'
    text += '👩‍💻 Soporte por correo 24/7 ✉' + '\n'
    return text


def full_body_day_1():
    text = '---- Día 1 --- \n'
    text += "<a href='https://www.google.com/'>Press Banca</a> 4 x 10" + '\n'
    text += 'Dominadas 4 x 10' + '\n'
    text += 'Sentadilla 4 x 10' + '\n'
    text += 'Peso Muerto Romano 4 x 10' + '\n'
    text += 'Press Militar 4 x 10' + '\n'
    return text


def full_body_day_2():
    text = '---- Día 2 --- \n'
    text += 'Fondos Paralelas 4 x 10' + '\n'
    text += 'Remo En Polea 4 x 10' + '\n'
    text += 'Hip Thrust 4 x 10' + '\n'
    text += 'Curl Femoral 4 x 10' + '\n'
    text += 'Press Militar 4 x 10' + '\n'
    return text


def full_body_day_3():
    text = '---- Día 3 --- \n'
    text += 'Cruce Poleas 4 x 10' + '\n'
    text += 'Dominadas 4 x 10' + '\n'
    text += 'Sentadilla 4 x 10' + '\n'
    text += 'Peso Muerto Romano 4 x 10' + '\n'
    text += 'Press Militar 4 x 10' + '\n'
    return text


def torso_day_1():
    text = '---- Día 1 --- \n'
    text += 'Press Banca 4 x 10' + '\n'
    text += 'Dominadas 4 x 10' + '\n'
    text += 'Press Militar 4 x 10' + '\n'
    text += 'Face Pull 4 x 10' + '\n'
    text += 'Brazos 4 x 10' + '\n'
    return text


def pierna_day_1():
    text = '---- Día 1 --- \n'
    text += 'Sentadilla 4 x 10' + '\n'
    text += 'Peso Muerto Romano 4 x 10' + '\n'
    return text


def push():
    text = '---- Push Day --- \n'
    text += 'Empujes 4 x 10' + '\n'
    return text


def pull():
    text = '---- Pull Day --- \n'
    text += 'Tracciones 4 x 10' + '\n'
    return text


def login():
    if DBManager.is_customer_in_db(user_message.chat.id):
        global is_demo
        is_demo = False
        text = "Selecciona una opción"
        bot.send_message(user_message.chat.id, text, reply_markup=logged_user_markup())
    else:
        text = "Me parece que no nos conocemos, volvamos a intentarlo..."
        bot.send_message(user_message.chat.id, text, reply_markup=new_user_welcome_markup())


def sign_up():
    try:
        # bot.send_message(user_message.chat.id, "El plan incluye: \n" + promo())
        products = stripe.Product.list(limit=3)
        for product in products.data:
            price = stripe.Price.list(product=product.id)
            bot.send_invoice(user_message.chat.id, product.name, product.description, product.id, pass_keys.pass_keys.STRIPE_TEST_BOT_TOKEN, 'EUR', [types.LabeledPrice(price.data[0].currency.upper(), price.data[0].unit_amount)], need_email=True)
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Fail in main:', ex.args, 'line:', exc_tb.tb_lineno)


@bot.pre_checkout_query_handler(func=lambda message: True)
def pre_checkout(message):
    try:
        global user_message
        user_message = message
        # customer = stripe.Customer.create(email=message.order_info.email, name=message.from_user.first_name)
        charge = stripe.Charge.create(amount=message.total_amount, currency="EUR", metadata={'telegram_id': message.from_user.id, 'receipt_email': message.order_info.email})
        if charge is not None and charge.last_response.code == 200:
            text = "Hello, \n There is a link to download the receipt of the last purchase: \n" + charge.receipt_url
            email_user(message.order_info.email, text)
            if not DBManager.insert_customer(message.from_user.id, message.from_user.first_name, message.order_info.email, charge.created):
                raise Exception("Error inserting user in db")

            bot.answer_pre_checkout_query(message.id, True)
            bot.send_message(message.from_user.id, acknowledgment())
            login()
    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Fail in main:', ex.args, 'line:', exc_tb.tb_lineno)


def email_user(user_email, text_to_send):
    sender_address = FIT_BOT_EMAIL
    sender_pass = pass_keys.pass_keys.FIT_BOT_EMAIL_PWD
    receiver_address = user_email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'FitBot Receip'  # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(text_to_send, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def acknowledgment():
    text = "🎉 ¡Muchísimas grácias por tu confianza! 🎉 \n"
    text += "Acabamos de enviarte un email con el estracto de tu factura, si no aparece en tu bandeja, revisa la carpeta de SPAM,\n"
    text += "Si tienes alguna duda puedes mandarnos un correo a " + FIT_BOT_EMAIL + ".\n"
    text += "De parte de todo el equipo de FitBot esperamos poder proporcionarte el mejor servicio.\n"
    text += "Vamos a por ello!"
    return text


if __name__ == "__main__":
    DBManager()
    print("Running bot...")
    bot.infinity_polling()
