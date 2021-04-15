import streamlit as st
import gspread
import pandas as pd
from fuzzywuzzy import process
from datetime import date
from oauth2client.service_account import ServiceAccountCredentials

PAGE_CONFIG = {'page_title': 'IPL Simulation', 'page_icon': '📓', 'layout': 'centered'}
st.set_page_config(**PAGE_CONFIG)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('iplsimulation.json', scope)
client = gspread.authorize(creds)
sheet = client.open('IPL Simulation')
date_subject = {'20/04/2021': 'Big Data', '22/04/2021': 'Deep Learning', '24/04/2021': 'Marketing Management',
               '26/04/2021': 'Computer Vision', '28/04/2021': 'Financial Institutions & Markets', '30/04/2021': 'Natural Language Processing',
               '14/04/2021': 'Test', '15/04/2021': 'Test', '16/04/2021': 'Test', '17/04/2021': 'Test', '18/04/2021': 'Test', '19/04/2021': 'Test'}
subject_id = {'Test': 0, 'Big Data': 1, 'Deep Learning': 2, 'Marketing Management': 3, 'Computer Vision': 4, 'Financial Institutions & Markets': 5, 'Natural Language Processing': 6}
today = date.today().strftime('%d/%m/%Y')

def insertQA(subj, q, a):
    records = sheet.get_worksheet(subject_id[subj])
    data = records.get_all_records()
    present = 0
    for dt in data:
        if dt['Question'] == q:
            present += 1
            st.subheader(f'Question: {q}')
            st.subheader(f'Answer: {dt["Answer"]}')
            st.subheader('Present!')
    
    if present == 0:
        records.append_row([q, a])
        st.subheader(f'Question: {q}')
        st.subheader(f'Answer: {a}')
        st.subheader('Added!')

def findQA(subj, q):
    records = sheet.get_worksheet(subject_id[subj])
    data = records.get_all_records()
    questions = pd.DataFrame.from_dict(data)['Question'].tolist()
    present = 0
    for dt in data:
        if dt['Question'] == q:
            present += 1
            st.subheader(f'Question: {q}')
            st.subheader(f'Answer: {dt["Answer"]}')
    
    if present == 0:
        st.subheader('Not found, most similar question is:')
        qs = process.extract(q, questions)
        q1, q2 = qs[0][0], qs[1][0]
        for dt in data:
            if dt['Question'] == q1:
                st.subheader(f'Question: {q1}')
                st.subheader(f'Answer: {dt["Answer"]}')
            if dt['Question'] == q2:
                st.subheader(f'Question: {q1}')
                st.subheader(f'Answer: {dt["Answer"]}')
        

def main():
    st.header('IPL Simulation')
    subj = date_subject[today]
    question = st.text_input('Enter question:').strip().lower()
    answer = st.text_input('Enter answer:').strip().lower()

    if st.button('Submit'):
        if answer == '' or answer == None:
            findQA(subj, question)
        else:
            insertQA(subj, question, answer)
        
if __name__ == '__main__':
    main()
