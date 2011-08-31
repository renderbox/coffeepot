.. Coffee Pot documentation master file, created by
   sphinx-quickstart on Mon Aug 29 14:04:07 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Coffee Pot's documentation!
======================================

Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

The base module to use is the JavaScript (JS) language you choose.  For example, if I want to use JQuery, I should look to import from coffeepot.jquery.  If you do it this way you will pick-up all the proper inheritance and module level configuring for free.

You can start with this (jquery)::

	from coffeepot.jquery.generator import Generator
	g = Generator()
	
A Generator is the basic tool in Coffee Pot.  It, well, generates JavaScript.  This Class is a Giant Factory with convenience methods for your JS library calls.  As you call each method, they are added to a todo queue.  

Generate the JavaScript::
	
	g.render()

When you call the render() method all the JS will be generated.  If you are using DJango, there is also a convience method that uses