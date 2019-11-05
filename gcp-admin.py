from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def gcp_grp_admin_client():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
    """

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']

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

    service = build('admin', 'directory_v1', credentials=creds)
    return service


def create_group(group_email_id):

    client = gcp_grp_admin_client()

    # list all current groups
    try:
        curr_grp_list = client.groups().list(domain=your-domain-name).execute()
    except Exception as e:
        print(f'Erorr getting list of current existing groups\n{e}')
        return

    if group_email_id in curr_grp_list:
        return f'Group by id {group_email_id} is already created'

    else:
        try:
            client.groups().insert(email=group_email_id,
                                   description=f'{group_email_id} Team',
                                   name=group_email_id.split('@')[0]).execute()
            print(f'Group created with email_id:- {group_email_id}')
        except Exception as e:
            print(f'Error creating group {group_email_id}\n{e}')

def delete_group(group_email_id):
    
    client = gcp_grp_admin_client()

    # list all current groups
    try:
        curr_grp_list = client.groups().list(domain=your-domain-name).execute()
    except Exception as e:
        print(f'Erorr getting list of current existing groups\n{e}')
        return

    if group_email_id in curr_grp_list:
        return f'Group by id {group_email_id} is already created'

    else:
        try:
            client.groups().delete(email=group_email_id).execute()
            print(f'Group created with email_id:- {group_email_id}')
        except Exception as e:
            print(f'Error creating group {group_email_id}\n{e}')    

def add_members(group_email_id, member_list):

    client = gcp_grp_admin_client()

    # list all the members in group
    try:
        existing_members_list = client.members().list(groupkey=group_email_id)..execute()
    except Exception as e:
        print(f'Error getting existing list of members for group {group_email_id}\n{e}')
        return

    for member_email_id in members_list:
        if member_email_id in existing_members_list:
            return

        else:
            try:
                client.members().insert(groupkey=group_email_id,
                                        email=member_email_id,
                                        role='MEMBER').execute()
                print(f'Member {member_email_id} added to group {group_email_id}')
            except Exception as e:
                print(f'Error adding Member {member_email_id} to group {group_email_id}\n{e}')


def remove_member(group_email_id, member_list):

    client = gcp_grp_admin_client()

    # list all the members in group
    try:
        existing_members_list = client.members().list(groupkey=group_email_id).execute()
    except Exception as e:
        print(f'Error getting existing list of members for group {group_email_id}\n{e}')
        return

    for member_email_id in members_list:
        if member_email_id in existing_members_list:
            return

        else:
            try:
                client.members().insert(groupkey=group_email_id,
                                        email=member_email_id).execute()
                print(f'Member {member_email_id} removed to group {group_email_id}')

            except Exception as e:
                print(f'Error removing user {member_email_id} from group {group_email_id}\n{e}')
