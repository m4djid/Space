import os
from datetime import datetime
from copy import deepcopy
from db import Handler


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
def fsscanner(path, properties=None, details=None):
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