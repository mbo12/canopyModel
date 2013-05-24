import bottle
import Model
import gevent
import gevent.pywsgi
import geventwebsocket
import json
import time
treeapp = bottle.Bottle()

@treeapp.route('/')
def index():

  return open('model.html','rU')

@treeapp.route('/displayModel.js')
def staticfile():
  return bottle.static_file('displaymodel.js',root='')

@treeapp.route('/model')
def canvasmodel():
  ws = bottle.request.environ.get('wsgi.websocket')
  tree = Model.Model()
  gevent.sleep(0.5)
  changes ={}
  changes['established']=tree.established
  changes['dead'] = tree.dead
  ws.send(json.dumps(changes))
  tree.transition()
  while 1:
    if (ws.receive()):
      gevent.sleep(0.5)
      changes ={}
      changes['established']=(tree.established)
      changes['dead'] = (tree.dead)
      ws.send(json.dumps(changes))
      tree.transition()
      
  
 
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketHandler, WebSocketError
server = WSGIServer(("0.0.0.0", 8000), treeapp,
                    handler_class=WebSocketHandler)
server.serve_forever()