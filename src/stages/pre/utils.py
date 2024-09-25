import requests
from datetime import datetime
from io import BytesIO
import dataclasses


def get_heritage_object(heritage_object_id):
    headers = {'Accept': 'application/json'}
    r = requests.get(url='https://inventaris.onroerenderfgoed.be/erfgoedobjecten/' + str(heritage_object_id),
                     headers=headers)
    return r


def check_maintenance_plan(heritage_object_id):
    headers = {'Accept': 'application/json'}
    r = requests.get(
        url='https://plannen.onroerenderfgoed.be/plannen?aanduidingsobject=https://id.erfgoed.net/aanduidingsobjecten/' + str(
            heritage_object_id),
        headers=headers)
    return r


def get_maintenance_plan(maintenance_uri):
    headers = {'Accept': 'application/json'}
    r = requests.get(url=maintenance_uri, header=headers)
    return r


@dataclasses.dataclass
class Relation:
    naam: str
    relation_type: str
    object_type: str
    uri: str

def extract_active_relation(heritage_json: dict[str, str]) -> list[Relation]:
    """ Function that extracts relevant relations (api apperantly does not always response with correct relations shown
    in interface?) -> see notebook for example of this """
    relevant_relations = []
    for relation in heritage_json.get("relaties", []):
        if relation.get("verwant_status", {}).get("naam", None) != "Actief":
            continue

        if relation.get("aanduidingsobjecttype", None) is None:
            continue

        relevant_relations.append(
            Relation(
                naam=relation.get("verwant", {}).get("naam"),
                relation_type=relation.get("relatietype", {}).get("naam"),
                object_type=relation.get("aanduidingsobjecttype"),
                uri=relation.get("uri")
            )
        )

        return relevant_relations

# Right now the decision is made that if there are multiple designation objects found, we simply take the first one
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
    headers = {'Accept': 'application/json'}
    r = requests.get(url='https://besluiten.onroerenderfgoed.be/besluiten/' + str(decision_id) + '/bestanden',
                     headers=headers)
    return r


def download_file(decision_id, file_id):
    url = 'https://besluiten.onroerenderfgoed.be/besluiten/' + str(decision_id) + '/bestanden/' + str(file_id)
    r = requests.get(url)
    # Assuming `pdf_bytes` contains the PDF file as bytes
    pdf_bytes = r.content  # your byte data

    # Create a BytesIO object from the byte data
    return BytesIO(pdf_bytes)

def download_plan_file(plan_id, file_id):
    url = 'https://plannen.onroerenderfgoed.be/plannen/' + str(plan_id) + '/bestanden/' +  str(file_id)
    r = requests.get(url)
     # Assuming `pdf_bytes` contains the PDF file as bytes
    pdf_bytes = r.content  # your byte data

    # Create a BytesIO object from the byte data
    return BytesIO(pdf_bytes)



def get_list_of_actions(decision):
    decision = decision.json()
    # We start from the assumption that the decission referred is a valid one. We will not implement to check wether it is expired or not
    if datetime.strptime(decision['datum_ondertekening'], '%Y-%m-%d') > datetime.strptime('2015-1-1', '%Y-%m-%d'):
        print('Get the PDF and look at Art. 5: ')
        decision_id = decision['id']
        return get_list_of_attachments(decision_id)
    else:
        print('Get the law text from the Codex and get a list of actions from it.')






# Example with a plan: get_actions_for_heritage_object(14167)
# Example after 2015: get_actions_for_heritage_object(31061)
# Example with actions in decision: get_actions_for_heritage_object(34145)
# Example before 2015: get_actions_for_heritage_object(135025)
