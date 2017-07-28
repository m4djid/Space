# VOSpace settings class
# This class checks the state of the service at start up
# Scan the file system to create a dictionary
# Set the service settings

import os
import time
from copy import deepcopy
from datetime import datetime
from db import Handler


RACINE = "./nodes"
PROTOCOL = {
        'get': 'ivo://ivoa.net/vospace/core#httpget',
        'post': 'ivo://ivoa.net/vospace/core#httppost',
        'put': 'ivo://ivoa.net/vospace/core#httpput',
        'delete': 'ivo://ivoa.net/vospace/core#httpdelete'
    }
PROPERTIES = {
        'title': '',
        'creator': '',
        'subject': '',
        'description': '',
        'publisher': '',
        'contributor': '',
        'date': '',
        'type': '',
        'format': '',
        'identifier': '',
        'source': '',
        'language': '',
        'relation': '',
        'coverage': '',
        'rights': '',
        'availableSpace': '',
        'groupread': '',
        'groupwrite': '',
        'publicread': '',
        'quota': '',
        'length': '',
        'mtime': '',
        'ctime': '',
        'btime': '',
    }
VIEWS = {
        'default': 'ivo://ivoa.net/vospace/core#defaultview',
        'anyview': 'ivo://ivoa.net/vospace/core#anyview',
        'fits': 'ivo://ivoa.net/vospace/core#fits',
        'votable': 'ivo://ivoa.net/vospace/core#votable',
        'zip': 'ivo://ivoa.net/vospace/core#zip',
        'tar.gz': 'ivo://ivoa.net/vospace/core#targz'
    }
PropertiesDict = {
    'title': {"title": '', "readonly": "False"},
    'creator': {"creator": '', "readonly": "False"},
    'subject': {"subject": '', "readonly": "False"},
    'description': {"description": '', "readonly": "False"},
    'publisher': {"publisher": '', "readonly": "False"},
    'contributor': {"contributor": '', "readonly": "False"},
    'date': {"date": '', "readonly": "False"},
    'type': {"type": '', "readonly": "True"},
    'format': {"format": '', "readonly": "False"},
    'identifier': {"identifier": '', "readonly": "False"},
    'source': {"source": '', "readonly": "False"},
    'language': {"language": '', "readonly": "False"},
    'relation': {"relation": '', "readonly": "False"},
    'coverage': {"coverage": '', "readonly": "False"},
    'rights': {"rights": '', "readonly": "False"},
    'availableSpace': {"availableSpace": '', "readonly": "False"},
    'groupread': {"groupread": '', "readonly": "False"},
    'groupwrite': {"groupwrite": '', "readonly": "False"},
    'publicread': {"publicread": '', "readonly": "False"},
    'quota': {"quota": '', "readonly": "False"},
    'length': {"length": '', "readonly": "False"},
    'mtime': {"mtime": '', "readonly": "True"},
    'ctime': {"ctime": '', "readonly": "True"},
    'btime': {"btime": '', "readonly": "True"},
}

def octet(entier):
    taille_ = entier
    retour = ''
    if taille_ >= 1000 and taille_ < 1000000:
        retour = str(round(taille_ / 100, 2)) + 'ko'
    elif taille_ >= 1000000:
        retour = str(round(taille_ / 1000000, 2)) + 'Mo'
    elif taille_ < 1000:
        retour = str(taille_) + 'o'
    return retour


def getsizedir(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return octet(total_size)


# Get node representation from the filesystem as dictionary
def fstodictionary(path, properties=None, details=None):
    tempdate = datetime.fromtimestamp(os.path.getmtime(path))
    mdate = tempdate.strftime("%Y-%m-%d %H:%M:%S")
    owner = str(os.stat(path).st_uid)
    filename = os.path.basename(path)
    parent = os.path.basename(os.path.abspath(os.path.join(path, os.pardir)))
    if parent == "nodes":
        parent = ''
    _path = path[path.find('nodes'):]
    if details:
        representation = {
            'node': filename,
            'path': _path,
            'ownerId': owner,
            'busy': "False",
            'parent': parent,
            'ancestor': [],
            'accepts': [],
            'provides': [],
        }
        if properties:
            representation['properties'] = deepcopy(properties)
        else:
            representation['properties'] = deepcopy(Handler().getPropertiesDict())
        representation['properties']['mtime'] = {"mtime": "Modified " + mdate, 'readonly': "True"}
        representation['properties']['ctime'] = {"ctime": "MetaData modified " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                 'readonly': "True"}
        representation['properties']['btime'] = {
            "btime": "Creation date " + datetime.fromtimestamp(os.path.getctime(path)).strftime(
                "%Y-%m-%d %H:%M:%S"), 'readonly': "True"}
        if os.path.isdir(path):
            representation['properties']['type'] = {'type': 'ContainerNode', 'readonly': "True"}
        elif os.path.isfile(path):
            representation['properties']['type'] = {'type': 'DataNode', 'readonly': "True"}
        representation['size'] = octet(os.path.getsize(path))
        mathusalem = path.split(os.sep)
        list = [".", "nodes", representation['parent'], representation['node']]
        for items in mathusalem:
            if items not in list:
                representation['ancestor'].append(items)

        return representation
    if not details:
        minrep = {'node': filename, 'path': _path}
        return minrep


def populatemeta():
    meta = [{'name': 'PROPERTIES', 'metadata': PROPERTIES, 'service': 'vospace'},
            {'name': 'PROTOCOL', 'metadata': PROTOCOL, 'service': 'vospace'},
            {'name': 'propertiesdict', 'metadata': PropertiesDict, 'service': 'vospace'},
            {'name': 'voprotocols', 'metadata': {
                'accepts': {'get': 'ivo://ivoa.net/vospace/core#httpget',
                            'put': 'ivo://ivoa.net/vospace/core#httpput'},
                'provides': {'get': 'ivo://ivoa.net/vospace/core#httpget',
                             'put': 'ivo://ivoa.net/vospace/core#httpput'}}, 'service': 'vospace'},
            {'name': 'voviews', 'metadata': {
                'accepts': {'anyview': 'ivo://ivoa.net/vospace/core#anyview',
                            'fits': 'ivo://ivoa.net/vospace/core#fits',
                            'votable': 'ivo://ivoa.net/vospace/core#votable'},
                'provides': {'default': 'ivo://ivoa.net/vospace/core#defaultview',
                             'fits': 'ivo://ivoa.net/vospace/core#fits',
                             'votable': 'ivo://ivoa.net/vospace/core#votable'}}, 'service': 'vospace'},
            {'name': 'voproperties', 'metadata': {
                'accepts': {},
                'provides': {},
                'contains': {'date': 'ivo://ivoa.net/vospace/core#date'}
            }, 'service': 'vospace'}]
    for items in meta:
        Handler().insertDB(items)
    print("VOSpace property list OK")
    print("VOSpace protocol list OK")
    print("VOSpace view list OK")
    print("Service's metadata ready")


def populatefiles():
    start_time = time.time()
    defaultproperties = Handler().getPropertiesDict()
    i = 0
    j = 0
    for dir, subdirs, files in os.walk(RACINE):
        for x in subdirs:
            i = i + 1
            Handler().insertDB(fstodictionary(os.path.join(dir, x), defaultproperties, 1))
        for y in files:
            j = j + 1
            Handler().insertDB(fstodictionary(os.path.join(dir, y), defaultproperties, 1))
    total = i+j
    print("%s files added in %s seconds" % (str(total), (time.time() - start_time)))


def fsdbcomparator():
    print("Comparision started")
    database = []
    FS = []
    cursor = Handler().connexion().find({'node': {'$exists': True}}, {'node': 1, 'path': 1, '_id': 0})
    for items in cursor:
        database.append(items)

    for dir, subdirs, files in os.walk("./nodes"):
        for x in subdirs:
            FS.append(fstodictionary(os.path.join(dir, x)))
        for y in files:
            FS.append(fstodictionary(os.path.join(dir, y)))

    r = [x for x in database + FS if x not in database or x not in FS]
    if len(r) > 0:
        for items in r:
            Handler().insertDB(fstodictionary(items['path'], details=1))
        print("Database Updated : %s node(s)" % len(r))
    else:
        print("Database up to date")


# Startup check up, if the app crashed and the DB is empty, it update it from FS
def main():
    try:
        if Handler().connexion().find({"service": "vospace"}).count() == 0:
            populatemeta()
        if Handler().connexion().find({"node": {'$exists': True}}).count() == 0:
            print("Scan du file system")
            populatefiles()
            print("Database ready")
        else:
            fsdbcomparator()
            print("Database: OK")
    except ConnectionError as e:
        return e

main()