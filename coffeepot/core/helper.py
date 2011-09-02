def arg_string_for_js(*args, **kwargs):
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
    #kwArgList = []
    sep = ", "
    kwsep = sep
    result = ""

    if 'indent' in kwargs:
        sep = ",\n%s" % (kwargs['indent'] * " ")
        kwsep = sep + "  "
        del( kwargs['indent'] )
            
    if args:
        result = sep.join([ convertValue(x) for x in args ])
    
    if kwargs:
        if args:
            result += sep
        result += "{ %s }" % kwsep.join([ '%s:%s' % ( k, convertValue(v) ) for k, v in kwargs.items() ])
    
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
