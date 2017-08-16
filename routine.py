from db import Handler
from fsscanner import fsscanner as fs
import os

class routine(object):

# Compare the file system to the database and add missing files to the database
    def fsdbcomparator(self):
        print("Comparision started")
        database = []
        FS = []
        cursor = Handler().connexion().find({'node': {'$exists': True}}, {'node': 1, 'path': 1, '_id': 0})
        for items in cursor:
            database.append(items)

        for dir, subdirs, files in os.walk("./storage"):
            for x in subdirs:
                FS.append(fs().scanner(os.path.join(dir, x)))
            for y in files:
                FS.append(fs().scanner(os.path.join(dir, y)))

        r = [x for x in database + FS if x not in database or x not in FS]
        if len(r) > 0:
            for _ in r:
                try:
                    Handler().insertDB(fs().scanner("./storage/"+_['path'], details=1))
                except Exception as e:
                    Handler().connexion().delete_one({'path':_['path']})
                    print(e)
            print("Database Updated : %s node(s)" % len(r))
        else:
            print("Database up to date")

