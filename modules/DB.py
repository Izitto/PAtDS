from tinydb import TinyDB, Query
'''
DB tables to add:
overlay manager:
    olm_overlays
    olm_sources

VTS manager:
    vtsm_models
    vtsm_expressions
    vtsm_modelPositions

    patds_config

'''

db = TinyDB('db.json')
olm_overlays = db.table('om_overlays')
olm_sources = db.table('om_sources')

search = Query()



def insert_overlay(overlay):
    olm_overlays.insert(overlay)

def get_overlay(overlay_uuid):
    return olm_overlays.search(search.uuid.matches == overlay_uuid)

def get_overlays():
    return olm_overlays.all()

def insert_source(source):
    olm_sources.insert(source)

# get source, search by uuid array
def get_source(source_uuid):
    return olm_sources.search(search.uuid.matches == source_uuid)

def get_sources():
    return olm_sources.all()


def dump_db():
    return db.all()