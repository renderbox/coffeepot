import unittest
from coffeepot.jquery.lib import Generator


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.g = Generator()
        self.functionName = 'steve'
        self.elementName = '#bob'
        
    # FUNCTION NODE TESTS
    def test_unnamed_function(self):
        self.g.reset_queue()
        f = self.g.add_function()
        self.assertEqual(f.render(), 'function() { }')

    def test_named_function(self):
        self.g.reset_queue()
        f = self.g.add_function(self.functionName)
        self.assertEqual(f.render(), '%s: function() { }' % (self.functionName) )

    # ELEMENT NODE TESTS
    def test_element_args(self):
        self.g.reset_queue()
        f = self.g.add_function(self.functionName)
        self.assertRaises(TypeError, f.add_element )

    def test_element_render(self):
        self.g.reset_queue()
        f = self.g.add_function(self.functionName)
        e = f.add_element(self.elementName).hide(3, t=2)
        self.assertEqual(self.g.render(), '%s: function() { $("%s").hide(3, { t:2 }); };' % (self.functionName, self.elementName) )


'''
from coffeepot.jquery.lib import Generator
g = Generator()
f = g.add_function('steve')
e = f.add_element('#bob').hide(3, t=2)
g.render()
'''