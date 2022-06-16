# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://mail.google.com/']

# Variable creds will store the user access token.
    # If no valid token found, we will create one.
creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
if os.path.exists('token.pickle'):

        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
service = build('gmail', 'v1', credentials=creds) 


def getEmails():
       

    # request a list of all the messages
    result = service.users().messages().list(userId='me',q="label:sent").execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    emails = []


    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    for msg in messages:
        # Get the message from its id
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        # Use try-except to avoid any Errors
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'To':
                    receiver = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data , "lxml")
            body = soup.body()

            # Printing the subject, sender's email and message
            str_body = str(body).replace("\r\n&gt", '')
            emails.append([msg['id'],msg['threadId'],subject,receiver,sender,str_body])
            
        except:
            pass

    return emails


mes = getEmails()


value = input("Welcome! Please introduce the substring you would like to search:\n")
print(f'You have searched for the substring {value}')

def search_sub(word,mail):
    found = []
    for x in mail:
        if word.lower() in x[2] + x[3] + x[4]:
            found.append(mail[mail.index(x)])
    return found

found_emails = search_sub(value,mes)

def create_message(thread,sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  print(message)
  raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
  return {
    'raw': raw_message.decode("utf-8"),
    'threadId': thread
  }

def send_message(message):
  try:
    message = (service.users().messages().send(userId= 'me', body=message).execute())
    print('Message Id: %s' % message['id'])
    return message
  except Exception as e:
    print('An error occurred: %s' % e)
    return None


def no_reply(mail):
    value = input('Please write the message you would to send\n Message: ')
    for thread in mail:
        compare = service.users().threads().get(userId = 'me', id=thread[1]).execute()
        if len(compare['messages']) <= 1:
           details =  create_message(thread[1],thread[4], thread[3], thread[2], value)
           send_message(details)
            
            
    return 

no_reply(mes)








    




