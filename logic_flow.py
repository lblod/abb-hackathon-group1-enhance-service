import requests
from datetime import datetime
import pdfplumber
from io import BytesIO

def get_heritage_object(heritage_object_id):
    headers = {'Accept': 'application/json'}
    r = requests.get(url='https://inventaris.onroerenderfgoed.be/erfgoedobjecten/' + str(heritage_object_id), headers=headers)
    return r

def check_maintenance_plan(heritage_object_id):
    headers = {'Accept': 'application/json'}
    r = requests.get(url='https://plannen.onroerenderfgoed.be/plannen?aanduidingsobject=https://id.erfgoed.net/aanduidingsobjecten/' + str(heritage_object_id),
                     headers=headers)
    return r

def get_maintenance_plan(maintenance_uri):
    headers = {'Accept': 'application/json'}
    r = requests.get(url= maintenance_uri, header=headers)
    return r

#Right now the decision is made that if there are multiple designation objects found, we simply take the first one
def get_do_from_response(json):
    for i in json['relaties']:
        if 'bescherming' in i:
            return i['self']

def get_designation_object(designation_object):
    headers = {'Accept': 'application/json'}
    r = requests.get(url=designation_object, headers=headers)
    return r

def get_decision(decision_uri):
    headers = {'Accept': 'application/json'}
    r = requests.get(url=decision_uri, headers=headers)
    return r
    
def get_list_of_attachments(decision_id):
    headers={'Accept': 'application/json'}
    r = requests.get(url='https://besluiten.onroerenderfgoed.be/besluiten/' + str(decision_id) + '/bestanden', headers=headers)
    return r

def download_file(decision_id, file_id):
    url = 'https://besluiten.onroerenderfgoed.be/besluiten/'+ str(decision_id) + '/bestanden/' + str(file_id)
    r = requests.get(url)
    # Assuming `pdf_bytes` contains the PDF file as bytes
    pdf_bytes = r.content  # your byte data

    # Create a BytesIO object from the byte data
    pdf_stream = BytesIO(pdf_bytes)
    with pdfplumber.open(pdf_stream) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text()

        print(all_text)
    
def get_list_of_actions(decision):
    decision = decision.json()
    # We start from the assumption that the decission referred is a valid one. We will not implement to check wether it is expired or not
    if datetime.strptime(decision['datum_ondertekening'], '%Y-%m-%d') > datetime.strptime('2015-1-1', '%Y-%m-%d'):
        print('Get the PDF and look at Art. 5: ')
        decision_id = decision['id']
        return get_list_of_attachments(decision_id)
    else:
        print('Get the law text from the Codex and get a list of actions from it.')

def get_actions_for_heritage_object(object):
    response = ''
    #Retrieve heritage object
    ho = get_heritage_object(object)
    #Only continue if heritage object exists
    if ho:
        response = ho.json()
    else:
        return 'Geen object gevonden'

    #Check if a maintenance plan is found for the object
    plan = check_maintenance_plan(object)
    if len(plan.json()) != 0:
        #If a plan is found, return it, and check if the user is satisfied
        print(get_maintenance_plan(plan.json[0]['uri']))
        return 'Plan gevonden'
    else:
        #If no plan is found, retrieve the relevant designation objects.
        do = get_do_from_response(response)
        r = get_designation_object(do)
        #Get the latest decision refering to the designation object
        #And check the date to be later than 2015-01-01
        #We opted to only check the first reference
        decision = get_decision(r.json()['besluiten'][0]['uri'])
        decision_id = decision.json()['id']
        #If the date is > 1-1-2015, download the 'besluit' pdf for reference of actions
        if datetime.strptime(decision.json()['datum_ondertekening'], '%Y-%m-%d') > datetime.strptime('2015-1-1', '%Y-%m-%d'):
            print('Get the PDF and look at Art. 5: ')
            attachments = get_list_of_attachments(decision_id)
            for i in attachments.json():
                if i['bestandssoort']['soort'] == 'Besluit':
                    print(download_file(decision_id, i['id']))
        else:
            print('Get the law text from the Codex and get a list of actions from it.')


# Example with a plan: get_actions_for_heritage_object(14167)
# Example after 2015: get_actions_for_heritage_object(31061)
# Example before 2015: get_actions_for_heritage_object(135025)