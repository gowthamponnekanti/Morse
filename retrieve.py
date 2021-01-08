import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/home/pi/Downloads/oops-49b91-firebase-adminsdk-hwhh0-9db96f5a05.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oops-49b91.firebaseio.com/'
})
ref = db.reference('oops')
print(ref.get())
d = dict(ref.get())
text = next(iter(d))
print(d[text]['studentName'])

ref.delete()
