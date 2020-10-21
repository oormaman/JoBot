import os
from re import search
import requests

from server import jobsDBLogic
from server.jobsDBLogic import get_all_job_links_in_db, delete_job_from_db

jobWebFileNameList=["jobWeb/orgadi.py","jobWeb/one1.py","jobWeb/nisha.py","jobWeb/drushim.py","jobWeb/intel.py"]

def run_web_scraping():
    for fileName in jobWebFileNameList:
        cmd = "python " + fileName
        os.system(cmd)

def check_if_its_student_job(new_job):
    expression = ["student" , "סטודנט","טנדוטס" ,"Student" , "sudent"]
    for item in expression:
        if search(item, new_job.job_name):
            return True
        if search(item, new_job.description):
            return True
    return False

def insert_new_job(new_job):
    keyword_dict = {}
    keyword_dict['software_student'] = ['C++', 'תוכנה', 'מדעי המחשב','Computer Science','Computer Science','R&D','אלגוריתמיקה','בדיקות']
    keyword_dict['electrical_student'] = ['חשמל','electronic','Electrical','חומרה','אלקטרוניקה']
    keyword_dict['mechanical_student'] = ['אנליזות','מכונות']
    keyword_dict['industrial_and_management'] = ['תעשייה וניהול','תעשיה וניהול','תפ"י']
    keyword_dict['business_and_economics'] = ['מנהל עסקים','כלכלן']
    for item in keyword_dict:
        if check_professional_affiliation_classification(new_job, keyword_dict[item]) is True:
            if new_job.affiliation1 == "NULL":
                new_job.set_affiliation1(item)
            elif new_job.affiliation2 == "NULL":
                new_job.set_affiliation2(item)
    jobsDBLogic.insert_job(new_job)


def check_professional_affiliation_classification(new_job,expression):
    for item in expression:
        if item in new_job.job_name:
            return True
        if item in new_job.description:
            return True
    return False

def check_if_jobs_still_relevant():
        all_jobs_links_in_db = get_all_job_links_in_db()
        for item in all_jobs_links_in_db:
            if requests.get(convert_tuple_to_str(item)).ok is False:
                print("isnt response:"+convert_tuple_to_str(item))
                delete_job_from_db(convert_tuple_to_str(item))

def convert_tuple_to_str(tup):
    str = ''.join(tup)
    return str

def main():
    run_web_scraping()


if __name__=="__main__":
    main()


