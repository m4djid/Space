import pymongo as mongo
import os
from datetime import datetime
from pymongo.errors import ConnectionFailure, CursorNotFound, OperationFailure


class Handler(object):

    @staticmethod
    def connexion():
        try:
            c = mongo.MongoClient('localhost', 27017)
            db = c['vospace']
            coll = db['VOSpaceFiles']
            return coll
        except ConnectionFailure as e:
            raise e

    # Insert into mongoDB
    def insertDB(self, data):
        try:
            coll = self.connexion()
            coll.insert_one(data)
        except OperationFailure as e:
            return e

    # Get the metadata representation from mongoDB
    def getNode(self, target, parent, ancestor):
        coll = self.connexion()
        curseur = coll.find({
            'node': target,
            'parent': parent,
            'ancestor' : ancestor
        }, {"_id": 0})
        temp = {}
        for document in curseur:
            for keys, values in document.items():
                temp[keys] = values
        return temp


    # Get a node's children's representation
    def getChildrenNode(self, node, ancestor):
        return self.connexion().find({"parent":node, "ancestor":ancestor}, {"path": 1, "busy": 1, "properties": 1, "_id": 0})

    # Get Property empty dictionary from DB
    def getPropertiesDict(self):
        retour = {}
        coll = self.connexion()
        curseur = coll.find({'name': 'propertiesdict'}, {"metadata": 1, "_id": 0})
        for documents in curseur:
            for keys, values in documents.items():
                    for k, v in values.items():
                        retour[k] = v
        return retour

    # Update node metadata
    def updateMeta(self, node, parent, ancestor, key, data):
        coll = self.connexion()
        try:
            if data[0] != '':
                coll.update({'node': node, 'parent':parent, 'ancestor':ancestor},
                            {"$set": {'properties.'+key+'.'+key: data[0], 'properties.'+key+'.readonly': data[1],
                                      'properties.ctime.ctime' : "MetaData modified " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
            elif data[0] != '' and data[1] == '':
                coll.update({'node': node, 'parent': parent, 'ancestor': ancestor},
                            {"$set": {'properties.' + key + '.' + key: data[0], 'properties.' + key + '.readonly': 'False',
                                'properties.ctime.ctime': "MetaData modified " + datetime.now().strftime(
                                '%Y-%m-%d %H:%M:%S')}})
            else:
                coll.update({'node': node, 'parent':parent, 'ancestor':ancestor}, {"set": {'properties.'+key+'.'+key: '',
                    'properties.ctime.ctime': "MetaData modified " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')}})
        except CursorNotFound as e:
            return "Error %s" % e


    def setViews(self, cible, parent, ancestor, accepts, provides):
        coll = self.connexion()
        if self.getNode(cible, parent, ancestor):
            coll.update({'node': cible, 'parent': parent, 'ancestor': ancestor}, {"$set": {'accepts': accepts, 'provides': provides}})

