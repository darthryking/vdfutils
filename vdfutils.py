"""

vdfutils.py
By DKY

Version 2.2.0

Utilities for processing Valve KeyValue data formats.

"""

__version__ = '2.2.0'

from collections import OrderedDict

__all__ = (
    'parse_vdf',
    'format_vdf',
    'NEWLINE',
    'TAB',
    'QUOTE',
    'OPEN_BRACE',
    'CLOSE_BRACE',
    'SLASH',
    'BACKSLASH',
    'ESC_BACKSLASH',
    'ESC_NEWLINE',
    'ESC_TAB',
    'ESC_QUOTE',
    'SPACE',
    'WHITESPACE',
)

NEWLINE = '\n'
TAB = '\t'

QUOTE = '"'

OPEN_BRACE = '{'
CLOSE_BRACE = '}'

SLASH = '/'

BACKSLASH = '\\'
ESC_BACKSLASH = BACKSLASH * 2
ESC_NEWLINE = BACKSLASH + 'n'
ESC_TAB = BACKSLASH + 't'
ESC_QUOTE = BACKSLASH + QUOTE

SPACE = ' '
WHITESPACE = ''.join((SPACE, NEWLINE, TAB))


class VDFConsistencyFailure(Exception):
    """ You have a bad VDF file. :( """
    
    BAD_VDF_MSG = "You have a bad VDF file. :("
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return "{}\nError is: {}".format(self.BAD_VDF_MSG, self.message)
        
        
class _Token(object):
    """ An abstract base class for VDF tokens. """
    pass
    
    
class _Field(_Token):
    """ A Token that represents a data field (either a key or a value). """
    
    def __init__(self, data):
        self.data = data
        
    def __repr__(self):
        return "_Field('{}')".format(self.data)
        
    def __eq__(self, other):
        return self.data == other.data
        
        
class _Brace(_Token):
    """ A Token that represents an open or close curly brace. """
    
    def __init__(self, open):
        self.isOpen = open
        
    def __repr__(self):
        return "_Brace({})".format(self.isOpen)
        
    def __eq__(self, other):
        return self.isOpen == other.isOpen
        
        
class _OpenBrace(_Brace):
    """ A Token that represents an open curly brace. """
    
    def __init__(self):
        super(_OpenBrace, self).__init__(True)
        
    def __repr__(self):
        return "_OpenBrace()"
        
        
class _CloseBrace(_Brace):
    """ A Token that represents a close curly brace. """
    
    def __init__(self):
        super(_CloseBrace, self).__init__(False)
        
    def __repr__(self):
        return "_CloseBrace()"
        
        
def _tokenize_vdf(inData, escape=True):
    """ Returns a generator that yields tokens representing the given VDF 
    data. If the generator encounters data that cannot be tokenized, raises
    VDFConsistencyFailure.
    
    """
    
    shouldEscape = escape
    
    def escape(s):
        ''' Replaces a string's escape sequences with their corresponding 
        characters, if shouldEscape is True. If shouldEscape is False, returns 
        the string unchanged.
        
        '''
        
        if not shouldEscape:
            return s
            
        escapeDict = {
            ESC_BACKSLASH   :   BACKSLASH,
            ESC_NEWLINE     :   NEWLINE,
            ESC_TAB         :   TAB,
            ESC_QUOTE       :   QUOTE,
        }
        
        sLen = len(s)
        
        result = []
        
        i = 0
        while i < sLen:
            for seq, char in escapeDict.iteritems():
                seqLen = len(seq)
                if s[i:i + seqLen] == seq:
                    result.append(char)
                    i += seqLen
                    break
            else:
                result.append(s[i])
                i += 1
                
        return ''.join(result)
        
    inData += SPACE     # Forces the last character to be dealt with properly.
    
    dataLen = len(inData)
    
    quoteStart = -1
    fieldStart = -1
    
    shouldEscapeQuote = False
    
    commented = False
    
    i = 0
    while i < dataLen:
        c = inData[i]
        
        if not commented:
            # VDF KeyValues comments are marked by a single forward slash.
            if c == SLASH:
                if quoteStart == -1:
                    commented = True
                    
            elif c == QUOTE:
                if not shouldEscapeQuote:
                    if quoteStart == -1:
                        if fieldStart != -1:
                            data = escape(inData[fieldStart:i])
                            yield _Field(data)
                            
                            fieldStart = -1
                            
                        quoteStart = i
                        
                    else:
                        data = escape(inData[quoteStart + 1:i])
                        yield _Field(data)
                        
                        quoteStart = -1
                        
            elif c in WHITESPACE:
                if fieldStart != -1:
                    data = escape(inData[fieldStart:i])
                    yield _Field(data)
                    
                    fieldStart = -1
                    
            elif c == OPEN_BRACE:
                if quoteStart == -1:
                    if fieldStart != -1:
                        data = escape(inData[fieldStart:i])
                        yield _Field(data)
                        
                        fieldStart = -1
                        
                    yield _OpenBrace()
                    
            elif c == CLOSE_BRACE:
                if quoteStart == -1:
                    if fieldStart != -1:
                        data = escape(inData[fieldStart:i])
                        yield _Field(data)
                        
                        fieldStart = -1
                        
                    yield _CloseBrace()
                    
            else:
                if quoteStart == -1 and fieldStart == -1:
                    fieldStart = i
                    
            # Special case for dealing with escaped quotes.
            if shouldEscape:
                if c == BACKSLASH:
                    shouldEscapeQuote = not shouldEscapeQuote
                else:
                    shouldEscapeQuote = False
                    
        else:   # Commented
            if c == NEWLINE:
                commented = False
                
        lastChar = c
        
        i += 1
        
    if quoteStart != -1:
        raise VDFConsistencyFailure("Mismatched quotes!")
        
        
def parse_vdf(inData, allowRepeats=False, escape=True):
    """ Parses a string in VDF format and returns an OrderedDict representing 
    the data.
    
    If this is not possible, raises VDFConsistencyFailure.
    
    """
    
    def parse_tokens(tokens, _depth=0):
        ''' Takes a stream of VDF tokens and uses them to build an ordered 
        dictionary representing the VDF data.
        
        If this is not possible, raises VDFConsistencyFailure.
        
        '''
        
        data = OrderedDict()
        
        key = None
        
        for token in tokens:
            if isinstance(token, _Field):
                if key is not None:
                    if allowRepeats:
                        try:
                            data[key].append(token.data)
                        except KeyError:
                            data[key] = token.data
                        except AttributeError:
                            elem = data[key]
                            data[key] = [elem, token.data]
                    else:
                        data[key] = token.data
                        
                    key = None
                    
                else:
                    key = token.data
                    
            elif isinstance(token, _OpenBrace):
                if key is not None:
                    # Recursion is fun!
                    data[key] = parse_tokens(tokens, _depth=_depth + 1)
                    key = None
                else:
                    raise VDFConsistencyFailure("Brackets without heading!")
                    
            elif isinstance(token, _CloseBrace):
                if _depth > 0:
                    break
                else:
                    raise VDFConsistencyFailure("Mismatched brackets!")
                    
            else:
                assert False
                
        else:   # Did not break from loop
            if _depth > 0:
                raise VDFConsistencyFailure("Mismatched brackets!")
                
        if key is not None:
            raise VDFConsistencyFailure("Key without value!")
            
        return data
        
    tokens = _tokenize_vdf(inData, escape)
    return parse_tokens(tokens)
    
    
def format_vdf(data, escape=True, _depth=0):
    """ Takes dictionary data and returns a string representing that data in 
    VDF format.
    
    """
    
    shouldEscape = escape
    
    def escape(s):
        ''' Takes a string and returns a new string with all escapable 
        characters escaped, if shouldEscape is True. If shouldEscape is False,
        returns the string unchanged.
        
        '''
        
        if shouldEscape:
            return (
                s
                    .replace(BACKSLASH, ESC_BACKSLASH)
                    .replace(NEWLINE, ESC_NEWLINE)
                    .replace(TAB, ESC_TAB)
                    .replace(QUOTE, ESC_QUOTE)
            )
        else:
            return s
            
    SINGLE_INDENT = ' ' * 4
    INDENT = SINGLE_INDENT * _depth
    
    outData = []
    
    for key, item in data.iteritems():
        if isinstance(item, basestring):
            outData += (
                INDENT,
                '"{}"'.format(escape(key)),
                SINGLE_INDENT,
                '"{}"'.format(escape(item)),
                '\n',
            )
            
        else:
            outData += (
                INDENT, '"{}"'.format(key),
                '\n', INDENT, '{\n',
                format_vdf(item, _depth=_depth + 1),    # Recursion is fun!
                '\n', INDENT, '}\n',
            )
            
    return ''.join(outData)
    
    