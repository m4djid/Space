# from VoPackage import settings as start
from functools import wraps
import os
from vospace import Vospace
from flask import Flask, request, Response, render_template, make_response
from flask_restplus import Api, Resource
from parser import Parser
import werkzeug.utils as w
from fsscanner import fsscanner as fs
from db import Handler as db

UPLOAD_FOLDER = './storage'

app = Flask(__name__)



api = Api(app, version='1.0', title='CDS VOSpace',
    description='Prototype de VOSpace')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'jar','vot','xml', 'java', 'tar.gz', 'zip']
app.config.SWAGGER_UI_LANGUAGES = ['en', 'fr']
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('templates/errors.html', maxBytes=1024 * 1024 * 100, backupCount=200)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("<br><br><table><tr><td><font color=\"red\"> %(asctime)s- %(name)s - %(levelname)s - %(message)s</font><tr></table>")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# def check_auth(username, password):
#     # Test account
#     user = ['iyapici' , 'm']
#     mdp = ['cds', 'b']
#     if username in user and password in mdp:
#         return username and password
#     # return username == 'iyapici' and password == 'cds'
#
# def authenticate():
#     # 401 return for identification
#     return Response(
#     'Could not verify your access level for that URL.\n'
#     'You have to login with proper credentials', 401,
#     {'WWW-Authenticate': 'Basic realm="Login Required"'})
#
# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         auth = request.authorization
#         if not auth or not check_auth(auth.username, auth.password):
#             return authenticate()
#         return f(*args, **kwargs)
#     return decorated



# @app.route('/', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
# def api_root():
#     if request.method == 'GET':
#         return "VOSpace"
#
#
# @app.route("/nodes", strict_slashes=False)
# def api_landing():
#     return make_response(render_template('nodes.html'), 200)


@api.route('/nodes/<path:path>',  strict_slashes=False)
class MyResource(Resource):
    @api.response(200, "Représentation de la node")
    @api.response(404, "Node non trouvée")
    def get(self,path):
        _path, target = os.path.split(path)
        _, parent = os.path.split(_path)
        if _:
            ancestor = _.split(os.sep)
        else:
            ancestor = []
        node = Vospace().getNode(target, parent, ancestor)
        if node == False:
            return make_response(render_template("404.html"), 404)
        else:
            return Response(node, mimetype='text/xml')

    @api.response(200, "Node modifiée")
    @api.response(404, "Node non trouvée")
    def post(self, path):
        xmltodict = Parser().xml_parser(request.data.decode("utf-8"))
        Vospace().setNode(xmltodict['cible'], xmltodict['parent'], xmltodict['ancestor'], xmltodict['properties'])
        node = Vospace().getNode(xmltodict['cible'], xmltodict['parent'], xmltodict['ancestor'])
        return Response(node, status=200, mimetype='text/xml')

    @api.response(201, "Représentation de la node créée")
    @api.response(500, "Erreur interne")
    def put(self, path):
        xmltodict = Parser().xml_parser(request.data.decode("utf-8"))
        Vospace().createNode(xmltodict)
        node = Vospace().getNode(xmltodict['cible'], xmltodict['parent'], xmltodict['ancestor'])
        return Response(node, status=201, mimetype='text/xml')

    @api.response(204, "Node deleted \n")
    def delete(self, path):
        return Response(Vospace().deleteNode(path), status=204, mimetype='text/xml')

@api.route('/upload/<path:path>',  strict_slashes=False)
class MyUpload(Resource):
    def put(self,path):
            print("PUT")
            file = request.files['files']
            print("FILE : ")
            print(request.files)
            if file and allowed_file(file.filename):
                filename = w.secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER']+"/"+path, filename))
                print("SAVE " + os.path.join(app.config['UPLOAD_FOLDER']+"/"+path, filename))
                db().insertDB(fs().scanner(os.path.join(app.config['UPLOAD_FOLDER']+"/"+path, filename), details=1))
            return path

@api.route("/protocols")
class Protocol(Resource):
    def get(self):
        body = Vospace().getVOSpaceSettings("protocols")
        if body:
            return Response(body, status='200', content_type='text/xml')
        else:
            make_response(render_template("404.html"), 404)


@api.route("/views")
class _View(Resource):
    def get(self):
        body = Vospace().getVOSpaceSettings("views")
        if body:
            return Response(body, status='200', content_type='text/xml')
        else:
            make_response(render_template("404.html"), 404)


@api.route("/properties")
class Properties(Resource):
    def get(self):
        body = Vospace().getVOSpaceSettings("properties")
        if body:
            return Response(body, status='200', content_type='text/xml')
        else:
            make_response(render_template("404.html"), 404)

@app.route("/errors")
def api_error():
    return make_response(render_template("errors.html"))


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)