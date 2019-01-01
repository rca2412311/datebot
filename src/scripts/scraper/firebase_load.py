import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./data/careerwise_firebase_cred.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Save data
with open('./data/new-york-city.json') as file:
    salaries = json.load(file)
    for salary in salaries:
        if 'intern' not in salary['jobTitle'].lower():
            try:
                doc_ref = db.collection(u'salary').document(u'{}'.format(salary['company']))
                doc_ref.set({
                    u'company': u'{}'.format(salary['company']).replace('/', ' '),
                    u'jobtitle': u'{}'.format(salary['jobTitle']),
                    u'pay': u'{}'.format(salary['meanPay'])
                })
            except Exception as e:
                print(e)

# Get data
# ref = db.collection(u'salary').where(u'company', u'==', u'Google').get()
# for refs in ref:
#     print(refs.to_dict())

