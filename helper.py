from flask import Flask, request, session, render_template, redirect, flash
import requests

CURR_USER_KEY = "current_user"
IS_TEACHER = "is_teacher"

def get_state_codes():
    states = requests.get('http://commonstandardsproject.com/api/v1/jurisdictions/').json()['data']
    data = [standards for standards in states if standards["type"] == "state"]
    return data

def get_standards_list(state_code):
    standards = requests.get(f'http://commonstandardsproject.com/api/v1/jurisdictions/{state_code}').json()['data']['standardSets']
    return standards

def get_subject_list(standards):
    subject_list = [standard_subject["subject"] for standard_subject in standards]
    return subject_list

def get_grade_level_standard_sets(grade, standards):
    """Returns all State Grade Level Standard Sets per grade in arguemnt
    Organized by subject."""

    grade_level_standards = [standard for standard in standards if grade in standard['educationLevels']]

    return grade_level_standards

def sort_sets_by_subject(subject_list, standard_set_list):
    standard_sets_by_subject = {}

    for subject in subject_list:
        sub_list = []
        for obj in standard_set_list:
            if subject == obj["subject"]:
                sub_list.append({'title': obj["document"]["title"],
                    'id': obj["id"]})

            standard_sets_by_subject[subject] = sub_list

    return standard_sets_by_subject

def get_standards(standard_set_code):
    standards = requests.get(f'http://commonstandardsproject.com/api/v1/standard_sets/{standard_set_code}').json()['data']['standards']

    standard_id_list = standards.keys()

    des = []
    for id in standard_id_list:
        des.append(standards[id]['description'])

    standards_dict = dict(zip(des, standard_id_list))

    return standards_dict

def extract_username_from_selectfield(string):
    string = string.split()
    username = string[-1]
    return sub(r'[\(\)]', '', username)

def append_zero_convert_to_string(int):
    """The API formats single digit grades as strings with appended 0's (ex. 02, 07, 08)"""
    if int <= 9:
        return ('0' + str(int))
    else:
        return str(int)

def remove_punc_characters(list):
    strings_sanz_punc = [string.replace('\'', '') for string in list]
    return strings_sanz_punc

def login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id
    session[IS_TEACHER] = user.is_teacher

def logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    if IS_TEACHER in session:
        del session[IS_TEACHER]