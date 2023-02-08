from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher

class JSON_RPC_Server:
    """ JSON RPC Server to expose canvas server methods.

    """

    def __init__(self,projection_server, hostname:str,
                port):
        
        # Projection Server
        self.projection_server = projection_server

        # WSGI Server Hostname
        self.hostname   = "localhost" if hostname is None else hostname

        # WSGI Server Port
        self.port       = 4000 if port is None else port


    
    @Request.application
    def application(self,request):

        response = JSONRPCResponseManager.handle(
            request.data, dispatcher)

        dispatcher.add_method(self.projection_server.test_connection)
        dispatcher.add_method(self.projection_server.remove_item)
        dispatcher.add_method(self.projection_server.hide_item)
        dispatcher.add_method(self.projection_server.get_all_plot_items)
        

        return Response(response.json, mimetype='application/json')
    
    # To start RPC Server
    def run(self):
        run_simple(hostname = self.hostname, 
                port = self.port, 
                application = self.application,
                threaded=True)

