import requests



def get_heritage_object(
        heritage_object_id: str | int,
        url: str = "https://inventaris.onroerenderfgoed.be/erfgoedobjecten/{}",
) -> requests.Response:
    return requests.get(url.format(heritage_object_id), headers={"Accept": "application/json"})


def get_maintenance_plan(maintenance_uri):
    headers = {'Accept': 'application/json'}
    r = requests.get(url= maintenance_uri, header=headers)
    return r



if __name__ == "__main__":
    import pprint
    o = get_heritage_object(14167)
    pprint.pprint(o.json(), indent=2)