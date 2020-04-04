from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly',
          'https://www.googleapis.com/auth/classroom.guardianlinks.students.readonly',
          'https://www.googleapis.com/auth/classroom.rosters.readonly'
          ]

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    global ludzie
    ludzie = {}
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    #Def dictionary check - Perf
    def checkKey(dict, key):

        if key in dict.keys(): #if there is key in memory
            dane = dict[key]
            return dane
        else:                   #update dictionary
            results = service.userProfiles().get(userId=udi)
            userinfo = results.execute()
            dane = userinfo['name']
            ludzie[key] = dane
            return dane



    service = build('classroom', 'v1', credentials=creds)

    # Call the Classroom API

    results = service.courses().list(pageSize=50).execute()
    courses = results.get('courses', [])
    dane = []
    if not courses:
        print('Brak widocznych zajęć')
    else:
        print('Zajęcia:')
        for course in courses:
            udi = course['ownerId']
            n = checkKey(ludzie, udi)
            linijka = course['ownerId']+" | "+n['fullName']+" | "+course["enrollmentCode"]+" | "+course['name']+" | "+course['descriptionHeading']
            print(linijka)


if __name__ == '__main__':
    main()