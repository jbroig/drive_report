from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Drive v3 API
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))