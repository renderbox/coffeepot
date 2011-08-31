"""
from pyjax.core.exception import JSLibraryError
from pyjax.core.node import CoreNode, ScriptNode, AlertNode, FunctionNode, Generator

try:
    from pyjax.core.node import TemplateNode
except ImportError:
    pass

class JQueryNode( CoreNode ):
    '''Generates Javascript'''

    def add_node(self, node):
        self.cache.append( node )

    def function(self, name=None, indent=None):
        result = FunctionNode(name, indent)
        self.add_node(result)
        return result


def make_method(m):
    def temp(self, *args, **kwargs):
        self.addMethod(m, args, kwargs)
        return self
    return temp

methodList = ['click', 'show', 'hide', 'append', 'before', 'after', 'prepend', 'insertBefore', 'insertAfter', 'replaceWith', 'html']

for m in methodList:
    setattr( JQueryNode, m, make_method(m) )
"""