import coffeepot
from coffeepot.core.exception import JSLibraryError
from coffeepot.core.helper import arg_string_for_js

class CoreNode(object):
    '''
    Foundation Class for all nodes.  All should inherit from this.
    '''

    def __init__(self, name):
        self.name = name
        self.reset_cache()
        
    def __str__(self):
        '''
        Added this built-in so the code can be generated when called by a
        formatted string.
        '''
        return self.render()
        
    def reset_cache(self):
        self.cache = []
        
    def render(self):
        '''
        Render method generates the JavaScript code for the node.
        '''
        if not self.cache:
            return ""


class _MethodNode(object):
    '''
    This is a representation of a method in JavaScript.  These are rendered
    building blocks for properly formatting python args into JS args. 
    
    These are created by other nodes and should not be instanced directly.
    '''
    def __init__(self, name, args=[], kwargs={} ):
        self.name = name
        self.args = args
        self.kwargs = kwargs

    def render(self):
        return '%s(%s)' % (self.name, arg_string_for_js(self.args, self.kwargs) )


class CompoundNode( CoreNode ):
    '''
    A Compound node is the equivalent of one line of JavaScript.  You can
    chain method calls with this type of node and as a result, the JavaScript
    generated will have chained methods.
    
    JQuery Example:
        $('foo').hide().fadeIn().fadeOut()
    '''

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


class FunctionNode( CoreNode ):
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

if coffeepot.FRAMEWORK in ['django']:
    from django.template.loader import get_template
    from django.template import Context, Template

    class TemplateNode( CoreNode ):
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

        @property
        def context(self):
            return self._context
            
        @context.setter
        def context(self, value):
            if isinstance(value, Context):
                self._context = value
            else:
                self._context = Context( value )

        @context.deleter
        def context(self, value):
            del self._context

        def add_template_path(self, template):
            '''
            add_template_path adds a Template Object to the render cache of the TemplateNode.
            It's a convenience method that will take a path to a template and use the
            appropriate template.
            '''
            self.add_template_object( get_template( template ) )

        def add_template_string(self, templateString):
            '''
            Similar to add_template except the input is a string.  This string will be 
            converted into a Django template and rendered with the Node's context
            '''
            self.add_template_object( Template( templateString ) )

        def add_template_object(self, templateObject):
            '''
            Similar to add_template except the input is a Django Template Object.  
            This will be added to cache and rendered with the Node's context
            '''
            self.cache.append( templateObject )

        def render(self, context={}):
            if not self.cache:
                return ""
            
            if not self.context:
                self.context = context
                
            return '\n'.join( [t.render( self.context ) for t in self.cache] )
