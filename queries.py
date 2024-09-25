from datetime import datetime
from helpers import update, generate_uuid
from escape_helpers import sparql_escape_string, sparql_escape_int, sparql_escape_uri, sparql_escape_datetime

def insert_heritage_objects(heritage_objects):
    """
    Takes in a list of heritage objects and inserts each object's rules as annotations and validations into the triplestore.

    heritage_objects: list[dict[int, list[dict]]]
      int -> heritage object id
      dict -> keys ('rule', 'source', 'source_type')
    """
    
    for heritage_object in heritage_objects:
        for heritage_object_id, rules in heritage_object.items():
            # Loop through the inner dictionary to get rule, source, and source_type
            for rule_entry in rules:
                rule = sparql_escape_string(rule_entry['rule'])
                source = sparql_escape_int(rule_entry['source'])
                source_uri = f"<https://id.erfgoed.net/besluiten/{source}>" # hard-coded besluit for now --> should be different based on source_type
                
                # Generate UUIDs for the annotation and validation
                annotation_uuid = generate_uuid()
                validation_uuid = generate_uuid()
                
                # Current datetime for the validation
                current_datetime = sparql_escape_datetime(datetime.now())
                
                # Build SPARQL query for the annotation and validation
                the_query = f"""
                PREFIX prov: <http://www.w3.org/ns/prov#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX vair: <https://w3id.org/vair#>
                PREFIX oa: <http://www.w3.org/ns/oa#>
                PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
                PREFIX dct: <http://purl.org/dc/terms/>
                PREFIX mu: <http://mu.semte.ch/vocabularies/core/>

                INSERT DATA {{
                  GRAPH <http://mu.semte.ch/application> {{
                    <http://data.lblod.info/annotations/{annotation_uuid}> a oa:Annotation ;
                      mu:uuid "{annotation_uuid}" ;
                      oa:hasBody {rule} ;
                      oa:hasTarget {source_uri} ;
                      ext:hasValidation <http://data.lblod.info/validations/{validation_uuid}> .
                    <http://data.lblod.info/validations/{validation_uuid}> a vair:Validation ;
                      mu:uuid "{validation_uuid}" ;
                      dct:creator <http://data.lblod.info/id/personen/67a8c359-437e-4375-b247-bcde9098ca8b> ;
                      dct:created {current_datetime} .
                  }}
                }}
                """
                
                # Execute the query for each rule entry
                update(the_query)
