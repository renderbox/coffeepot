from pyjax.core.exception import JSLibraryError
from pyjax.core.node import CoreNode, ScriptNode, AlertNode, FunctionNode, Generator

try:
    from pyjax.core.node import TemplateNode
except ImportError:
    pass


"""
class InsertNode(CoreNode):
    '''Generates code to insert text into a div using Javascript'''
    
    WHERE = ["before", "after", "html", "append", "prepend"]
    
    def __init__(self, idtag, location, text, parent=None ):
        
        super(InsertNode, self).__init__(parent)

        self.idtag = idtag
        self.location = location
        self.text = text

    def render(self):
        if self.location == "before":
            return "$('%s').insertBefore('%s')" % (self.text, self.idtag)
        elif self.location == "after":
            return "$('%s').insertAfter('%s')" % (self.text, self.idtag)
        elif self.location == "append":
            return "$('%s').append('%s')" % (self.idtag, self.text)
        elif self.location == "prepend":
            return "$('%s').prepend('%s')" % (self.idtag, self.text)
            
        return "$('%s').html('%s')" % (self.idtag, self.text)
"""        

class JQueryNode(CoreNode):
    '''Generates visual effect code in Javascript'''

    def function(self, name=None, indent=None):
        result = FunctionNode(name, indent)
        self.add_node(result)
        return result

'''
class Bob(object):
    def addMethod(self, m, args, kwargs):
        print m
'''

def make_method(m):
    def temp(self, *args, **kwargs):
        self.addMethod(m, args, kwargs)
        return self
    return temp

methodList = ['click', 'show', 'hide', 'append', 'before', 'after', 'prepend', 'insertBefore', 'insertAfter', 'replaceWith', 'html']

for m in methodList:
    setattr( JQueryNode, m, make_method(m) )
