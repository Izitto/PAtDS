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

db = TinyDB('/home/izitto/Documents/Code/PAtDS/database/db.json')
olm_overlays = db.table('om_overlays')
olm_sources = db.table('om_sources')

search = Query()



def insert_overlay(overlay):
    # check if overlay already exists with same uuid, if it does, update it
    if olm_overlays.search(search.uuid == overlay['uuid']):
        olm_overlays.update(overlay, search.uuid == overlay['uuid'])
    else:
        olm_overlays.insert(overlay)

def get_overlay(overlay_uuid):
    return olm_overlays.search(search.uuid == overlay_uuid)

# delete overlay, search by uuid
def delete_overlay(overlay_uuid):
    olm_overlays.remove(search.uuid == overlay_uuid)

def get_overlays():
    return olm_overlays.all()

def insert_source(source):
    olm_sources.insert(source)

# get source, search by uuid array
def get_source(source_uuid):
    return olm_sources.search(search.uuid == source_uuid)

def get_sources():
    return olm_sources.all()



def dump_db():
    return db.all()[0]

def drop_all():
    db.drop_tables()


# get list of all overlays names and their uuids
def get_overlay_list():
    overlays = olm_overlays.all()
    overlay_list = []
    for overlay in overlays:
        overlay_list.append({'name': overlay['name'], 'uuid': overlay['uuid']})
    return overlay_list