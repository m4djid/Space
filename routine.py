from db import Handler
from fsscanner import fsscanner
import os

# Compare the file system to the database and add missing files to the database
def fsdbcomparator():
    print("Comparision started")
    database = []
    FS = []
    cursor = Handler().connexion().find({'node': {'$exists': True}}, {'node': 1, 'path': 1, '_id': 0})
    for items in cursor:
        database.append(items)

    for dir, subdirs, files in os.walk("./nodes"):
        for x in subdirs:
            FS.append(fsscanner(os.path.join(dir, x)))
        for y in files:
            FS.append(fsscanner(os.path.join(dir, y)))

    r = [x for x in database + FS if x not in database or x not in FS]
    if len(r) > 0:
        for items in r:
            Handler().insertDB(fsscanner(items['path'], details=1))
        print("Database Updated : %s node(s)" % len(r))
    else:
        print("Database up to date")

