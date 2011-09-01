import coffeepot
from coffeepot.core.node import FunctionNode, ScriptNode

class _CoreGenerator(object):
    def __init__(self):
        #super(object, self).__init__()
        self.reset_queue()

    def add_node(self, node):
        self.queue.append( node )
        return node

    def reset_queue(self):
        self.queue = []
        
    def render(self):
        if not self.queue:
            return ""
        
        return ";\n".join( [x.render() for x in self.queue] ) + ";"

    # CONVIENENCE FUNCTIONS
    def function(self, name=None, indent=None):
        '''
        Returns a Function node object
        '''
        return FunctionNode(name, indent)

    def add_function(self, name=None, indent=None):
        '''
        Creates a Function Node object and Adds it to the Queue.
        '''
        return self.add_node( self.function(name, indent) )

    def add_script(self, text):
        return self.add_node( ScriptNode(text) )


if coffeepot.FRAMEWORK in ['django']:
    from coffeepot.core.node import TemplateNode
    from django.http import HttpResponse

    class _DjangoGenerator( _CoreGenerator ):
        def render_to_response(self, content_type="text/javascript"):
            return HttpResponse(self.render(), content_type=content_type)

        def template_node(self, template, context={}):
            return self.add_node( TemplateNode( template, context ) )

    Generator = _DjangoGenerator
        
else:     #If it does not exist we are OK not adding the method
    Generator = _CoreGenerator
