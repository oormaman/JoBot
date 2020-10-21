import textwrap
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from server import jobsDBLogic
from server.userDbLogic import get_user_affiliation, get_total_job_that_the_user_viewed


def answer_for_user(user_msg, user_id):
    if(user_msg=="/start"):
         return 'ברוכים הבאים לבוט גוב.' \
                '\nאנא בחר קטגורייה בה תרצה לצפות.'
    elif(user_msg=="professional_affiliation_choosen"):
        return "שיוך מקצועי התקבל במערכת - "+print_professional_affiliation(user_id)+"\n על מנת להתעדכן במשרות חדשות,\n תוכל להוסיף מייל לקבלת עדכונים אודות משרות חדשות או שתוכל לבדוק כבר מחר משרות חדשות."
        # return 'שיוך מקצועי התקבל במערכת-"+ "\n על מנת לראות משרות חדשות,\n אנא לחץ על הכפתור "צפייה במשרות חדשות". '
    elif(user_msg=="/getNewJobs"):
              job_obj = text_message_design(jobsDBLogic.get_exist_job(user_id))
              return job_obj
    elif (user_msg == "new_jobs_not_found"):
        return "הבוט פירסם עבורך "+get_total_job_that_the_user_viewed(user_id) +" משרות .\n על מנת להתעדכן במשרות חדשות,\n תוכל להוסיף מייל לקבלת עדכונים אודות משרות חדשות או שתוכל לבדוק כבר מחר משרות חדשות."
    elif (user_msg == "before_add_email_msg"):
        return "בהודעה הבאה שלך אנא רשום את המייל שלך בלבד.לדוגמא: \n example@gmail.com \nבעת הוספת המייל הנך מאשר קבלת דיוור מצוות joBot.\nתוכל להסיר תמיד את המיילים עי לחיצה על:\n /deleteMail "
    elif (user_msg == "email_added_successfully"):
        return "מייל נוסף בהצלחה.\n במידה והנך מעוניין להסיר את המייל מהמאגר שלנו, אנא לחץ /deleteMail"
    elif (user_msg == "delete_mail"):
        return "מייל הוסר מהמאגר, לא תקבל יותר עדכונים למייל."
    elif (user_msg == "unknown_message"):
        return 'סליחה...לא הבנתי אותך 🙄 \nלחץ על הכפתור "צפייה במשרה חדשה" בשביל לראות משרות חדשות '
    elif (user_msg == "mail_didnt_exist_in_db"):
        return "לא קיים מייל במאגר הנתונים."
    return ''

def print_professional_affiliation(user_id):
    ans=get_user_affiliation(user_id)
    if ans=="software_student":
        return "סטודנט לתוכנה"
    if ans=="electrical_student":
        return "סטודנט לחשמל"
    if ans=="mechanical_student":
        return "סטודנט למכונות"
    if ans=="industrial_and_management":
        return "סטודנט לתעשייה וניהול"
    return ""

def get_new_job(user_id):
    jobsDBLogic.get_exist_job(user_id)

def text_message_design(msg):
    job_obj = {}
    job_site_name=msg[5]
    print(job_site_name)
    site_that_not_support_in_preview_msg={"one1"}
    if msg is not None:
        if job_site_name in site_that_not_support_in_preview_msg:
            job_name="שם משרה: "+msg[1]
            job_description="תיאור: "+'\n'+msg[3]
            value=job_name+'\n' + job_description+'\n'
            wrapper = textwrap.TextWrapper(width=50)
            string = wrapper.fill(text=value)
            job_obj['content'] =value
            job_obj['link'] = msg[2]
            return job_obj
        job_obj['content'] = msg[2]
        job_obj['link'] = msg[2]
        return job_obj
    else:
        return None

def init_professional_affiliation_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='סטודנט לתוכנה', callback_data='software_student')],
        [InlineKeyboardButton(text='סטודנט לחשמל', callback_data='electrical_student')],
        [InlineKeyboardButton(text='סטודנט למכונות', callback_data='mechanical_student')],
        [InlineKeyboardButton(text='סטודנט לתעשייה וניהול', callback_data='industrial_and_management')],
    ])
    return keyboard

def send_new_jobs_btn():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='לחץ כאן לצפייה במשרות חדשות', callback_data='get_new_jobs')],
    ])
    return keyboard

def send_cv_btn(link):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='לחץ כאן למעבר למשרה ולשליחת קוח', callback_data='press', url=link)],
    ])
    return keyboard

def send_new_jobs_and_add_mail_btn():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='לחץ כאן לצפייה במשרות חדשות', callback_data='get_new_jobs')],
        [InlineKeyboardButton(text='לחץ כאן להוספת מייל', callback_data='before_add_email_msg')],
    ])
    return keyboard

def delete_mail_from_db_btn():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='מחק מייל ממאגר הנתונים', callback_data='delete_mail')],
    ])
    return keyboard
