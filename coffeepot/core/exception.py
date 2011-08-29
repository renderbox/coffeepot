class JSLibraryError(Exception):
    
    def __init__(self, message):
        super(Exception, self).__init__(message)
        

class NoSuchVisualEffectError(Exception):
    '''
    Raise and error if a visual effect is missing 
    '''
    def __init__(self, message):
        super(Exception, self).__init__(message)
