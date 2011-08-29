from coffeepot.core.node import 

class CoreGenerator(object):
    def __init__(self):
        #super(object, self).__init__()
        self.reset_cache()

    def add_node(self, node):
        self.cache.append( node )
        return node

    def reset_cache(self):
        self.cache = []

    def function(self, name=None, indent=None):
        return self.add_node( FunctionNode(name, indent) )

    def render(self):
        if not self.cache:
            return ""
        
        return ";\n".join( [x.render() for x in self.cache] ) + ";"



try:
    from coffeepot.core.node import TemplateNode
    from django.http import HttpResponse

    class DjangoGenerator( CoreGenerator ):
        def render_to_response(self, content_type="text/javascript"):
            return HttpResponse(self.render(), content_type=content_type)

        def template_node(self, template, context={}):
            return self.add_node( TemplateNode( template, context ) )

    Generator = DjangoGenerator
        
except ImportError:     #If it does not exist we are OK not adding the method
    Generator = GeneratorNode
        