import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://students-attendence-9b56a-default-rtdb.firebaseio.com/"
    
})

ref=db.reference("students")

data={
    "22210797":{
        'name':'pranav hore',
        'major':'it',
        'total_attendence':'6',
        'year':'2',
        'last_attendence_time':'2024-4-4 00:00:00'
    },
     "22210798":{
        'name':'alia bhatt',
        'major':'it',
        'total_attendence':'6',
        'year':'2',
        'last_attendence_time':'2024-4-4 00:00:00'
    },
      "22210799":{
        'name':'kiara adwani',
        'major':'it',
        'total_attendence':'6',
        'year':'2',
        'last_attendence_time':'2024-4-4 00:00:00'
    },
       "22210800":{
        'name':'kumar vishwas',
        'major':'it',
        'total_attendence':'6',
        'year':'2',
        'last_attendence_time':'2024-4-4 00:00:00'
    },
       "22210801":{
        'name':'narendra modi',
        'major':'it',
        'total_attendence':'6',
        'year':'2',
        'last_attendence_time':'2024-4-4 00:00:00'
    },
     
}

for key,value in data.items():
    ref.child(key).set(value)