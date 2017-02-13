import os
import cherrypy
from cherrypy.lib.static import serve_file

class Wiki():

    def __init__(self):
        self.headerbegin = """
        <!DOCTYPE HTML>
        <html>
        <head>"""
        self.headerend = """
        </head>"""
        self.bodybegin = """
        <body>"""
        self.bodyend = """
        </body>
        </html>"""
        self.currdir = "%s/" %(os.path.dirname(os.path.abspath(__file__)))

        # Template for a draggable object. Needs name, number and content
        self.element = """
        <p draggable="true" ondragstart="drag(event)" id="%s%s">%s</p>"""
        # Template for a draggable div. Needs name, number and content
        self.div = """
        <div id="div%s%s" class="div" ondrop="drop(event)" ondragover="allowDrop(event)">
            %s
        </div>"""

    # Creates a html site with links to all .html files
    @cherrypy.expose
    def index(self):
        header = self.createHeader()

        body = self.createBody()

        return header + body

    def createBody(self):
	self.addPelement = """
        <script>
	var para = document.createElement("p");
	var node = document.createTextNode("This is new.");
	para.appendChild(node);

	var element = document.getElementById("div1");
	element.appendChild(para);
	</script>"""
        element1 = self.element %("test", "1", "TEST")
        div1 = self.div %("test", "1", element1)
        div2 = self.div %("test", "2", " ")
        content = div1 + div2
        return self.bodybegin + content + self.bodyend

    def createHeader(self):
        self.jsDnDFunctions = """
        <script>
        function allowDrop(ev){
            ev.preventDefault();
        }

        function drag(ev){
            ev.dataTransfer.setData("text", ev.target.id);
        }

        function drop(ev){
            ev.preventDefault();
            var data = ev.dataTransfer.getData("text");
            ev.target.appendChild(document.getElementById(data));
        }
        </script>
        """

        self.style = """
        <style>
	.div {
	    float: left;
	    width: 100px;
	    height: 35px;
	    margin: 10px;
	    padding: 10px;
	    border: 1px solid black;
	}
	</style>"""

        return self.headerbegin + self.style + self.jsDnDFunctions + self.headerend


if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    config = {'global':
        {
            'server.socket_host': "127.0.0.1",
            'server.socket_port': 18080,
            'server.thread_pool': 10,
        },
        '/static':
        {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': "%s/public" % (os.path.dirname(os.path.abspath(__file__)))
        }

    }
    cherrypy.quickstart(Wiki(), '/', config=config)
