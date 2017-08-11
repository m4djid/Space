# Classe traduisant les instructions en actions
import os
import shutil
import time
from copy import deepcopy

from fsscanner import fsscanner as fs
from db import Handler as mydb
from genericbackend import Backend
from parser import Parser as xml


class Vospace(Backend):


    # Get the service's protocols/views/properties list
    def getVOSpaceSettings(self, meta):
        retour = {}
        coll = mydb().connexion()
        curseur = coll.find({'name': 'vo'+meta})
        if curseur:
            for documents in curseur:
                for keys, values in documents.items():
                    if keys == "metadata":
                        for k, v in values.items():
                            retour[k] = v
        return xml().xml_generator(meta, retour)

    # Get the node data
    def getNode(self, target, parent, ancestor):
        # Return the node's representation
        node = {
            'children': [],
            'properties': {},
            'accepts': {},
            'provides': {},
            'busy': '',
        }
        try:
                meta = mydb().getNode(target, parent, ancestor)
                if meta == {}:
                    return False
                else:
                    node['busy'] = meta['busy']
                    node['path'] = deepcopy(meta['path'])
                    node['properties'] = deepcopy(meta['properties'])
                    node['accepts'] = deepcopy(meta['accepts'])
                    node['provides'] = deepcopy(meta['provides'])
                    # If the parent is not empty, it is added to
                    # the ancestor list to find the subnodes
                    if parent != '':
                        ancestor.append(parent)
                    cursor = mydb().getChildrenNode(target, ancestor)
                    for items in cursor:
                        node['children'].append(items)
                    return xml().xml_generator("get",node)
        except Exception as e:
            return e


    def createNode(self, dictionary):
        if dictionary['ancestor'] == ['']:
            # MongoDB ancestor field will not work if
            # ancestor = ['']
            ancestor = []
        else:
            ancestor = dictionary['ancestor']
        representation = mydb().getNode(dictionary['cible'], dictionary['parent'], ancestor)
        if not representation:
            try:
                os.makedirs(dictionary['path'])
            except OSError as e:
                return 'Directory creation failed. Error %s' % e
            if os.path.exists(dictionary['path']):
                mydb().insertDB(fs().scanner(dictionary['path'], details=1))
                self.setNode(dictionary['cible'], dictionary['parent'], ancestor, dictionary['properties'])
        else:
            return "FileExistsError"

    def setNode(self, target, parent, ancestor, properties):
        if ancestor == ['']:
            # MongoDB ancestor field will not work if
            # ancestor = ['']
            ancestor = []
        readOnly = mydb().getNode(target, parent, ancestor)
        if readOnly:
            # if readOnly['busy'] == "False":
            validator = {}
            for keys, values in readOnly['properties'].items():
                for k, v in values.items():
                    validator[k] = v
            propDict = mydb().getPropertiesDict()
            for key in set(properties).intersection(set(validator)):
                propDict[key] = deepcopy(properties[key])
                if readOnly['properties'][key]['readonly'] not in ["true", "True"]:
                    mydb().updateMeta(target, parent, ancestor, key, propDict[key])
            else:
                return "Node busy"


    def copyNode(self, targetPath, locationPath):
        pass

    def moveNode(self, targetPath, locationPath):
        pass

    def deleteNode(self, targetPath):
        # Delete the node and the subnodes
        path, target = os.path.split(targetPath)
        _, parent = os.path.split(path)
        if not _:
            # MongoDB ancestor field will not work if
            # ancestor = ['']
            ancestor = []
        else:
            ancestor = _.split(os.sep)
        if "storage" in ancestor:
            ancestor.remove("storage")
        if os.path.exists(targetPath):
            # isbusy = mydb().getNode(target, parent, ancestor)
            # if isbusy:
            #     if isbusy['busy'] == "False":
            if mydb().connexion().delete_one({'node': target, 'parent': parent, 'ancestor': ancestor}):
                if parent:
                    ancestor.append(parent)
                if mydb().connexion().delete_many({'parent': target, 'ancestor': ancestor}):
                    if os.path.isdir(targetPath):
                        shutil.rmtree(targetPath)
                    elif os.path.isfile(targetPath):
                        os.remove(targetPath)
        else:
            return "FileNotFound"

    def pushToVoSpace(self, targetPath, **kwargs):
        # Execute a push to VOSpace
        pass

    def pushFromVoSpace(self, targetPath, **kwargs):
        # Execute a push from VOSpace
        pass

    def pullFromVoSpace(self, targetPath, **kwargs):
        # Execute a pull from VOSpace
        pass

    def pullToVoSpace(self, targetPath, endpointUri):
        # Execute a pull to VOSpace
        pass
