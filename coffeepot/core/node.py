from coffeepot.core.exception import JSLibraryError
from coffeepot.core.helper import arg_string_for_js

class _Node(object):
    '''
    Foundation Class for all nodes.  All should inherit from this.
    '''

    def __init__(self, name)
        self.name = name
        self.reset_cache()

    def add_node(self, node):
        self.cache.append( node )
        
    def reset_cache(self):
        self.cache = []
        
    def render(self):
        if not self.cache:
            return ""


class _MethodNode(object):
    '''
    This is a representation of a method in JavaScript.  This are rendered
    building blocks for properly formatting python args into JS args. 
    
    These are created by other nodes and should not be instanced directly.
    '''
    def __init__(self, name, args=[], kwargs={} )
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def render(self):
        return '%s(%s)' % (self.name, arg_string_for_js(self.args, self.kwargs) )


class CompoundNode(_Node):
    '''
    A Compound node is the equivalent of one line of JavaScript.  You can
    chain method calls with this type of node and as a result, the JavaScript
    generated will have chained methods.
    '''

    def add_node(self, node):
        raise NotImplementedError("function add_node not implemented")
    
    def add_method(self, name, args=[], kwargs={}):
        self.cache.append( _MethodNode(name, args, kwargs) )

    def render(self):
        if not self.cache:
            return ""
        
        return '$("%s").%s' % (self.name, '.'.join([x.render() for x in self.cache]) )


class ScriptNode(object):
    '''
    A Script node is one that assumes you are giving it proper raw JavaScript.
    It does not try to generate JavaScript of it's own but instead provide a 
    place to add whatever you want.  This was created so it can be inserted
    into a Generator chain like other nodes.
    '''
    def __init__(self, text):
        self.text = text

    def render(self):
        return self.text


class AlertNode(object):
    '''
    Creates a standard JavaScript alert dialogue
    '''
    def __init__(self, alert):
        self.alert = alert

    def render(self):
        return 'alert("%s")' % self.alert


class FunctionNode(_Node):
    '''
    This is a special kind of Node that takes a list of Nodes that allows you
    to encapsulate several lines of code into a single function.
    If you don't pass a name in, the function will be anonymous.  If you don't
    pass in an indent value, the returned string will be in one line with ';' 
    separating commands.
    '''

    def __init__(self, name=None, indent=None):
        super(FunctionNode, self).__init__(name)
        self.indent = indent

    def render(self):
        result = ""
        sep = "; "

        if self.indent:
            sep = ";\n%s" % (self.indent * " ")

        if self.name:
            result += "%s: function() { " % self.name
        else:
            result += "function() { "

        result += sep.join([x.render() for x in self.cache])
        result +=  "; }"
        return result
        

#
#   'Django patch' the classes if the django libraries are installed
#

try:
    from django.template.loader import get_template

    class TemplateNode( _Node ):
        '''
        A Script node is one that assumes you are giving it the proper JavaScript.
        It does not try to generate JavaScript of it's own but instead provide a 
        place to add whatever you want.  This was created so it can be inserted
        into a Generator chain like other nodes.
        '''
        def __init__(self, template, context={} ):
            super(TemplateNode, self).__init__(None)
            self.context = context
            self.add_template( template, self.context )

        def add_node(self, node):
            raise NotImplementedError("function add_node not implemented")

        def add_template(self, template, context={} ):
            if template.__class__.__name__ in ['str']:
                self.cache.append( Template( template ) )
            else:
                self.cache.append( get_template( template ) )

        def render(self):
            if not self.cache:
                return ""
                
            return '\n'.join( [t.render( self.context ) for t in self.cache] )

except ImportError:     #If it does not exist we are OK not adding the method
    pass
