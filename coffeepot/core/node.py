import coffeepot
from coffeepot.core.exception import JSLibraryError
from coffeepot.core.helper import arg_string_for_js

class _Node(object):
    '''
    Foundation Class for all nodes.  All should inherit from this.
    '''

    def __init__(self, name=None, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.reset_queue()
        
    def __str__(self):
        '''
        Added this built-in so the code can be rendered when called by a
        formatted string.
        '''
        return self.render()
        
    def reset_queue(self):
        '''
        Set the queue back to nothing.
        '''
        self.queue = []

    def add_to_queue(self, node):
        '''
        Anything can be added to the render queue as long as it has a 'render()' 
        method and it returns a string.
        '''
        self.queue.append( node )
        return node
        
    def render(self):
        '''
        Render method generates the JavaScript code for the node.
        '''
        if not self.queue:
            return ""


class _MethodNode(_Node):
    '''
    This is a representation of a method in JavaScript.  These are rendered
    building blocks for properly formatting python args into JS args. 
    
    These are created by other nodes and should not be instanced directly.
    '''

    def render(self):
        return '%s(%s)' % (self.name, arg_string_for_js(self.args, self.kwargs) )


class _GeneratorNode(_Node):
    '''
    Generator Node is what the user will used to generate the JavaScript.
    This (or one of it's derivatives) should be used to create everything 
    else from.
    '''

    def render(self):
        if not self.queue:
            return ""

        return ";\n".join( [x.render() for x in self.queue] ) + ";"

    # CONVIENENCE FUNCTIONS
    def function(self, name=None, indent=None):
        '''
        Returns a Function Node Object and returns it.
        '''
        return FunctionNode(name, indent)

    def add_function(self, name=None, indent=None):
        '''
        Creates a Function Node object and Adds it to the Queue.
        '''
        return self.add_to_queue( self.function(name, indent) )

    def script(self, text):
        '''
        Creates a Script Node Object and returns it.
        '''
        return ScriptNode(text)

    def add_script(self, text):
        return self.add_to_queue( self.script(text) )

    def add_element(self, name, *args, **kwargs):
        return self.add_to_queue( ElementNode(name, *args, **kwargs) )


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


class FunctionNode( _GeneratorNode ):
    '''
    This is a special kind of Node that takes a list of Nodes that allows you
    to encapsulate several lines of code into a single function.
    If you don't pass a name in, the function will be anonymous.  If you don't
    pass in an indent value, the returned string will be in one line with ';' 
    separating commands.
    '''

    def __init__(self, name=None, indent=None, *args, **kwargs):
        super(FunctionNode, self).__init__(name, *args, **kwargs)
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

        result += sep.join([x.render() for x in self.queue])
        
        if self.queue:
            result +=  "; }"
        else:
            result +=  "}"
            
        return result
        

class ElementNode( _Node ):
    '''
    A Element Node can operate on an HTML element with JavaScript.  You can
    chain method calls with this type of node and as a result, the JavaScript
    generated will have chained methods.
    
    The following example is using '#foo' as the element.

    JQuery Example:
        $('#foo').hide().fadeIn().fadeOut()
    '''

    def add_method(self, name, args=[], kwargs={}):
        self.queue.append( _MethodNode(name, args, kwargs) )

    def render(self):
        if not self.queue:
            return ""

        return '$("%s").%s' % (self.name, '.'.join([x.render() for x in self.queue]) )


# Add JQuery Functions to the Element Node
if coffeepot.JSLIB in ['jquery']:
    def make_method(m):
        def temp(self, *args, **kwargs):
            self.add_method(m, args, kwargs)
            return self
        return temp
    
    # This list should probably be automaticly generated.
    methodList = ['click', 'show', 'hide', 'append', 'before', 'after', 'prepend', 'insertBefore', 'insertAfter', 'replaceWith', 'html']

    for m in methodList:
        # NEED TO ADD CHECK TO MAKE SURE IT'S NOT ALREADY THERE
        setattr( ElementNode, m, make_method(m) )


#-------------------------------------------------------------------
#   DJANGO PATCHING
#
#   'Django patch' the classes if the django libraries are installed
#

if coffeepot.FRAMEWORK in ['django']:
    from django.template.loader import get_template
    from django.template import Context, Template
    from django.http import HttpResponse

    class TemplateNode( _Node ):
        '''
        A TemplateNode node uses the Django template system to generate the code.
        It assumes that whatever you are handing it, you know what you are doing.
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
            add_template_path adds a Template Object to the render queue of the TemplateNode.
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
            This will be added to queue and rendered with the Node's context
            '''
            self.queue.append( templateObject )

        def render(self, context={}):
            if not self.queue:
                return ""
            
            if not self.context:
                self.context = context
                
            return '\n'.join( [t.render( self.context ) for t in self.queue] )


    class _DjangoGeneratorNode( _GeneratorNode ):
        def render_to_response(self, content_type="text/javascript"):
            return HttpResponse(self.render(), content_type=content_type)

        def template_node(self, template, context={}):
            return self.add_to_queue( TemplateNode( template, context ) )

    Generator = _DjangoGeneratorNode

else:     #If it does not exist we are OK not adding the method
    Generator = _GeneratorNode
