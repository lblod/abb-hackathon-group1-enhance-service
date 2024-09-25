from ..base import Stage
from .utils import *
from ...components.data.datasource import DataSource
from ...components.data import codex
from datetime import datetime


class PreProcessingStage(Stage):
    pass

    def __init__(self):
        super().__init__()

    def get_actions_for_heritage_object(self, object_id):
        # Retrieve heritage object
        ho = get_heritage_object(object_id)

        if not ho.ok:
            return 'Geen object gevonden'

        heritage_json = ho.json()

        # Check if a maintenance plan is found for the object
        plan = check_maintenance_plan(object_id)
        if len(plan.json()) != 0:
            # If a plan is found, return it, and check if the user is satisfied
            print(get_maintenance_plan(plan.json[0]['uri']))
            return 'Plan gevonden'
        else:
            # If no plan is found, retrieve the relevant designation objects.
            do = extract_active_relation(heritage_json)
            r = get_designation_object(do[0].uri)  # only using first for now
            # Get the latest decision refering to the designation object
            # And check the date to be later than 2015-01-01
            # We opted to only check the first reference
            decision = get_decision(r.json()['besluiten'][0]['uri'])
            decision_id = decision.json()['id']
            # If the date is > 1-1-2015, download the 'besluit' pdf for reference of actions
            if datetime.strptime(decision.json()['datum_ondertekening'], '%Y-%m-%d') > datetime.strptime('2015-1-1',
                                                                                                         '%Y-%m-%d'):
                print('Get the PDF and look at Art. 5: ')
                attachments = get_list_of_attachments(decision_id)
                for i in attachments.json():
                    if i['bestandssoort']['soort'] == 'Besluit':
                        dsource = DataSource(
                            filetype="byte_pdf",
                            file=download_file(decision_id, i['id'])
                        )
                        yield dsource

            else:
                yield codex


    def run(self, *args, **kwargs) -> list[dict[int, list[DataSource]]]:
        """
        1. Gather data (if needs be a preselection list of ids we randomly selected)
        2. For each element in the data, gather:
            => APPLY RULES
            => all files that are required to scrape for relevant rules
            => furture attributes that are used in processing
            ...

            Keep in mind that we just need to gather all things that are relevant to pass to the AI service.
            We could easily extend this later on.
        3.  For each data source, create a dictionary where key -> item id, and value is a list of instances of the "DataSource" class.
            This datasource class can easily be red in the upcomming step
        """

        heritage_ids = kwargs.get("heritage_objects", [])
        heritage_files = []

        for heritage_id in heritage_ids:
            heritage_files.append(
                {heritage_id:list(self.get_actions_for_heritage_object(heritage_id))}
            )

        return heritage_files



if __name__ == "__main__":
    PreProcessingStage().run()
    print(codex.content)

