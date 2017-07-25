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
        # else:
        #     self.prop_ = {
        #         'node': nodeCible,
        #         'path': targetPath,
        #         'parent': os.path.basename(os.path.split(targetPath)[0]),
        #         'ancestor': [],
        #         'accepts': [],
        #         'provides': [],
        #         'properties': {},
        #     }
        #     self.prop_['properties'] = self.getPropertiesDict()
        #     self.prop_['properties']['mtime'] = {
        #             "mtime": "Modified "+datetime.fromtimestamp(os.path.getmtime(targetPath)).strftime(
        #                 "%Y-%m-%d %H:%M:%S"), "readOnly": "True"}
        #     self.prop_['properties']['ctime'] = {
        #             "ctime": "MetaData modified "+datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "readOnly": "True"}
        #     self.prop_['properties']['btime'] = {
        #             "btime": "Creation date "+datetime.fromtimestamp(os.path.getctime(targetPath)).strftime(
        #                 "%Y-%m-%d %H:%M:%S"), "readOnly": "True"}
        #     self.prop_['properties'][cle] = donnee[cle]
        #     self.insertDB(self.prop_)

    def setViews(self, cible, accepts, provides):
        coll = self.connexion()
        # nodeCible = os.path.basename(cible)
        if self.getNode(cible):
            coll.update({'path': cible}, {"$set": {'accepts': accepts, 'provides': provides}})


# a = Handler()
# # a.updateMeta("BBBBB","myresult1",[],"description",["test de création", "True"])
#
# print(a.getNode("tatatata","myresult1",[]))

# a.getChildrenNode("VospaceUws")
# pprint(a.getMeta("./VOTest/VOSpace/nodes/myresult1"))
# print(a.nodeExistsChecker('myresult1.txt'))
# print(a.fsToDict('/home/bouchair/PycharmProjects/VOSpace-Py/VOTest/VOSpace/nodes/myresult1/Capability'))
# print(a.getVOSpaceSettings('voviews'))
# print(a.getMeta("./VOTest/VOSpace/nodes/myresult1"))
# a.insertionMongo(a.metaDB("./VOTest/VOSpace/nodes/myresult1"), 'NodeMeta')
# a.insertionMongo(a.metaDB("./VOTest/VOSpace/nodes/myresult2"), 'NodeMeta')
# a.insertionMongo(a.metaDB("./VOTest/VOSpace/nodes/myresult3"), 'NodeMeta')
# meta = a.metaDB("./VOTest/VOSpace/nodes/myresult1")
# if a.modifMeta("myresult3", meta):
#       print("Updated")
# a.insertionMongo(a.fsToDict("./VOTest/VOSpace/nodes/myresult1"), 'VOSpaceFiles')
# a.insertionMongo(a.fsToDict("./VOTest/VOSpace/nodes/myresult2"), 'VOSpaceFiles')
# a.insertionMongo(a.fsToDict("./VOTest/VOSpace/nodes/myresult3"), 'VOSpaceFiles')
