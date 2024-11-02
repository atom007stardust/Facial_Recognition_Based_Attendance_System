import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"Enter your firebase database URL here"
})
#create the reference to the database    #within the database create a reference called Students,
# within students there'll be std ids, within each id there will be additional information of the students
ref = db.reference('Students')
#We can create an interface to add the data to the database, if an admin is using this when a new student registers, we can use pygame or Tkinter
#JSON format
#wihtin JSON we will have another JSON that will have the information
data  = {
    "123456":
        {
            "name" : "Tom Cruise",
            "major" : "Acting",
            "starting_year": 2021,
            "total_attendance":6,
            "standing":"G", #G means good
            "year":4,
            "last_attendance_time":"2024-03-12 00:23:45"


        },
    "555444":
        {
            "name" : "Jack Black",
            "major" : "Medicine",
            "starting_year": 2021,
            "total_attendance":8,
            "standing":"G", #G means good
            "year":4,
            "last_attendance_time":"2024-05-09 00:20:45"
        },
    "654321":
    {
            "name" : "Rebecca Ferugson",
            "major" : "Acting",
            "starting_year": 2022,
            "total_attendance":3,
            "standing":"B", #B means bad
            "year":3,
            "last_attendance_time":"2024-02-12 00:15:34"
    },
    "888888":
        {
            "name" : "Sarah Omar",
            "major" : "Software Engineering",
            "starting_year": 2021,
            "total_attendance":8,
            "standing":"G", #G means good
            "year":4,
            "last_attendance_time":"2024-05-23 00:10:10"
        },
    "454545":
        {
            "name" : "Emma Watson",
            "major" : "Journalism",
            "starting_year": 2018,
            "total_attendance":4,
            "standing":"G", #G means good
            "year":1,
            "last_attendance_time":"2024-05-23 00:10:10"
        },
    "778899":
        {
            "name" : "Abdullah Majid",
            "major" : "Accounting",
            "starting_year": 2024,
            "total_attendance":4,
            "standing":"G", #G means good
            "year":1,
            "last_attendance_time":"2024-05-23 00:10:10"
        }
}

#send the data to the database
for key,value in data.items():
    ref.child(key).set(value) #to send the data to a specific directory, use ,child
