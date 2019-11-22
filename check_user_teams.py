import csv
import requests
import json
import pandas as pd
import sys

api_key = '<your api key here>'
user_data_csv = './user-list.csv' 
list_users_url = "https://api.opsgenie.com/v2/users/"
api_headers = {'Content-Type': 'application/json','Authorization':'GenieKey ' + api_key}
get_teams_url = "https://api.opsgenie.com/v2/users/"
get_schedules_url = "https://api.opsgenie.com/v2/users/"
not_assigned = {'team': [], 'schedule': []}


def build_user_list(api_key, url, api_headers):
    user_list_request = requests.get(url = list_users_url, headers = api_headers)
    user_json = json.loads(user_list_request.text) 
    users = []
    
    for user in user_json['data']:
        if user['role']['name'] != "Stakeholder":
            users.append(user['username'])

    while 'next' in user_json['paging']:
        next_url = str(user_json['paging']['next'])
        user_list_request = requests.get(url = next_url, headers = api_headers)
        user_json = json.loads(user_list_request.text)    
        for user in users_json['data']:
            if user['role']['name'] != "Stakeholder":
                users.append(user['username'])
    return users

def call_user_checks(users):
    for user in users:
        check_if_team_member(user)
        check_if_scheduled(user)

def check_if_team_member(user):
    user_teams_request = requests.get(url = get_teams_url + user + "/teams", headers = api_headers)
    user_teams_json = json.loads(user_teams_request.text)
    if len(user_teams_json['data']) == 0 :
        not_assigned['team'].append(user)

def check_if_scheduled(user):
    user_schedules_request = requests.get(url = get_schedules_url + user + "/schedules" , headers = api_headers)
    user_schedules_json = json.loads(user_schedules_request.text)
    if len(user_schedules_json['data']) == 0:
        not_assigned['schedule'].append(user)

def generate_csv(not_assigned):
    df_team = pd.DataFrame(not_assigned['team'])
    df_schedule = pd.DataFrame(not_assigned['schedule'])
    df = pd.concat([df_team, df_schedule], axis=1)
    df.columns = ['Not assigned to a team', 'Not assigned to a schedule']
    df.to_csv(user_data_csv, sep='\t', encoding='utf-8')

users = build_user_list(api_key, list_users_url, api_headers)
call_user_checks(users)
generate_csv(not_assigned)





