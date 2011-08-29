def arg_string_for_js(args, kwargs, indent=None):
    '''
    Formats a dictionary into a string for JavaScript functions to work with.
    It's different from the JSON Parser in that the key values are not put
    in quotes.
    
    EXAMPLE:
    
    INPUT ARGS
    ['one', 2]

    INPUT DICTIONARY
    {'bool': True, 'color': 'green', 'number': 1, 'url': '/path/tostuff.html'}
    
    OUTPUT (normal)
    'one', 2, {url:"/path/tostuff.html", color:"green", bool:true, number:1}
    
    OUTPUT (indented 4 spaces)
    'one', 2,
    {url:"/path/tostuff.html",
        color:"green",
        bool:true,
        number:1}
    '''
    argList = []
    kwArgList = []
    sep = ", "
    result = ""

    if indent:
        sep = ",\n%s" % (indent * " ")
    
    for entry in args:
        argList.append( convertValue(entry) )
    
    if kwargs:
        for k, v in jsOpts.items():
            kwArgList.append( '%s:%s' % ( k, convertValue(v) ) )
            
    if argList:
        result = sep.join(argList)
    
    if kwArgList:
        if argList:
            result += sep
        result += "{ %s }" % sep.join(kwArgList)
    
    return result


def convertValue(value):
    if isinstance( value, bool ):                           # Convert Boolean capitalization
        return str(value).lower()
    elif isinstance( value, int ):                          # Values that should not be in quotes
        return value
    elif isinstance( value, dict ):                         # Values that should not be in quotes
        return arg_string_for_js( [], value )
    elif isinstance( value, list ) or isinstance( value, tuple ):              # Values that should not be in quotes
        return '[%s]' % arg_string_for_js( value, {} )
    else:                                                   # Everything else
        return '"%s"' % value
