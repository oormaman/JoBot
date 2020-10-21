import time
import telepot
from telepot.loop import MessageLoop
from client import messageController
from client.messageController import init_professional_affiliation_keyboard, send_new_jobs_btn, send_cv_btn, \
    send_new_jobs_and_add_mail_btn, delete_mail_from_db_btn
from server import jobsDBLogic
from server.mailController import check_if_its_currect_mail_adress
from server.userDbLogic import check_if_user_exist_in_db, set_new_mail, \
    delete_mail, set_new_professional_affiliation, check_if_user_already_have_mail


def on_chat_message(msg):
    print(msg)
    content_type, chat_type, chat_id = telepot.glance(msg)
    check_if_user_exist_in_db(msg)
    user_id = str(msg["chat"]["id"])
    if check_if_its_currect_mail_adress(msg["text"]):
       mail = msg["text"]
       add_new_mail(chat_id, mail)
    elif msg["text"] == '/start':
        show_intro_msg(chat_id)
    elif msg["text"] == '/deleteMail':
        delete_mail(chat_id)
    else:
        unknown_message(user_id)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print("query data:"+query_data)
    if query_data in affiliation_list:
        set_new_professional_affiliation(from_id, query_data)
        keyboard = send_new_jobs_btn()
        bot.sendMessage(from_id, messageController.answer_for_user("professional_affiliation_choosen", from_id),reply_markup=keyboard)
    elif  query_data =="get_new_jobs":
        print_jobs_description_to_user(from_id)
    elif query_data =="before_add_email_msg":
        bot.sendMessage(from_id, messageController.answer_for_user("before_add_email_msg", from_id))
    elif query_data == "email_added_successfully":
        keyboard = delete_mail_from_db_btn()
        bot.sendMessage(from_id, messageController.answer_for_user("email_added_successfully", from_id),reply_markup=keyboard)
    elif query_data == "delete_mail":
        delete_mail(from_id)

def add_new_mail(user_id,mail):
    keyboard=delete_mail_from_db_btn()
    bot.sendMessage(user_id, messageController.answer_for_user("email_added_successfully", user_id),reply_markup=keyboard)
    set_new_mail(user_id, mail)

def show_intro_msg(user_id):
    message_for_user = messageController.answer_for_user("/start", user_id)
    keyboard = init_professional_affiliation_keyboard()
    bot.sendMessage(user_id, message_for_user, reply_markup=keyboard)

def delete_mail(user_id):
    keyboard = send_new_jobs_btn()
    if check_if_user_already_have_mail(user_id):
        bot.sendMessage(user_id, messageController.answer_for_user("delete_mail", user_id), reply_markup=keyboard)
    else:
        bot.sendMessage(user_id, messageController.answer_for_user("mail_didnt_exist_in_db", user_id), reply_markup=keyboard)

def unknown_message(user_id):
    keyboard=send_new_jobs_btn()
    bot.sendMessage(user_id, messageController.answer_for_user("unknown_message", user_id),reply_markup=keyboard)

def print_jobs_description_to_user(user_id):
    response = jobsDBLogic.get_exist_job(user_id)
    for job_tupple in response:
        job_description = job_tupple[3]
        link = job_tupple[2]
        keyboard = send_cv_btn(link)
        bot.sendMessage(user_id, job_description, reply_markup=keyboard)
    keyboard = send_new_jobs_and_add_mail_btn()
    bot.sendMessage(user_id, messageController.answer_for_user("new_jobs_not_found", user_id), reply_markup=keyboard)


affiliation_list = ["software_student","electrical_student","mechanical_student","industrial_and_management"]
TOKEN = ""
bot = telepot.Bot(TOKEN)

def run_telegram_chat():
    MessageLoop(bot, {'chat': on_chat_message,
                      'callback_query': on_callback_query}).run_as_thread()
    print('Listening ...')
    while True:
        time.sleep(10)