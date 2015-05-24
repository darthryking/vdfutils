import sys
import os

from vdfutils import parse_vdf, format_vdf, VDFConsistencyFailure

PARSE_VDF_DIR = 'parse_vdf'
PARSE_VDF_TEST_CASES = (
    (
        'test1.vdf',
        True,
        {
            'key1'  :   'value1',
            'key2'  :   'value2',
            'key3'  :   'value3',
            'key4'  :   'value4',
            'key5'  :   'value5',
        },
    ),
    (
        'test2.vdf',
        True,
        {
            'key1'  :   'value1',
            'key2'  :   'value2',
            'key3'  :   'value3',
            'key4'  :   'value4',
            'key5'  :   'value5',
        },
    ),
    (
        'test3.vdf',
        True,
        {
            'key1'  :   'value1',
            'key2'  :   'value2',
            'key3'  :   'value3',
            'key4'  :   'value4',
            'key5'  :   'value5',
        },
    ),
    (
        'test4.vdf',
        True,
        {
            'body'  :   {
                'head'  :   'skull',
                'torso' :   {
                    'upper' :   {
                        'arm1'  :   'left',
                        'arm2'  :   'right',
                    },
                    'lower' :   {
                        'leg1'  :   'left',
                        'leg2'  :   'right',
                    },
                },
            },
        },
    ),
    (
        'test5.vdf',
        True,
        VDFConsistencyFailure("Brackets without heading!"),
    ),
    (
        'test6.vdf',
        True,
        VDFConsistencyFailure("Brackets without heading!"),
    ),
    (
        'test7.vdf',
        True,
        VDFConsistencyFailure("Mismatched brackets!"),
    ),
    (
        'test8.vdf',
        True,
        {
            'This'  :   'is',
            'some'  :   'perfectly',
            'valid' :   'data.',
        },
    ),
    (
        'test9.vdf',
        True,
        VDFConsistencyFailure("Key without value!"),
    ),
    (
        'test10.vdf',
        True,
        {
            'foo'   :   'repeat',
        },
    ),
    (
        'test11.vdf',
        True,
        {},
    ),
    (
        'test12.vdf',
        True,
        {
            'visible'   :   'value',
            'can'       :   {
                'see'   :   'everything',
                'in'    :   'here',
            },
        },
    ),
    (
        'test13.vdf',
        True,
        {
            'this'  :   {
                'is'    :   {
                    'a' :   {
                        'set'   :   {
                            'of'    :   {
                                'ultra' :   {
                                    'nested'    :   {
                                        'brackets'  :   {}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
    ),
    (
        'test14.vdf',
        True,
        VDFConsistencyFailure('Mismatched brackets!'),
    ),
    (
        'test15.vdf',
        True,
        VDFConsistencyFailure('Mismatched brackets!'),
    ),
    (
        'test16.vdf',
        True,
        {
            'escaped'   :   {
                'tab'           :   '\t',
                'newline'       :   '\n',
                'quote'         :   '\"',
                'backslash'     :   '\\',
                'everything'    :   '\t\n\"\\\\\"\n\t',
            }
        },
    ),
    (
        'test16.vdf',
        False,
        VDFConsistencyFailure('Mismatched quotes!'),
    ),
    (
        'test17.vdf',
        False,
        {
            'unescaped'   :   {
                'tab'           :   '\\t',
                'newline'       :   '\\n',
                'backslash'     :   '\\\\',
                'everything'    :   '\\t\\n\\',
                '\\\\\\\\\\'    :   '\\n\\t',
            }
        },
    ),
)


def test_parse_vdf():
    for file, escape, expected in PARSE_VDF_TEST_CASES:
        with open(os.path.join(PARSE_VDF_DIR, file), 'r') as f:
            data = f.read()
            
        print "Testing {}...".format(file)
        print "Expected:\n", expected
        
        if (type(expected) is not dict and
                issubclass(expected.__class__, Exception)):
                
            result = None
            try:
                result = parse_vdf(data, escape=escape)
                
            except expected.__class__ as e:
                print "Result:\n", e
                
                assert str(e) == str(expected)
                
                print "Passed!\n"
                continue
                
            print "Result:\n", result
            assert result is None
            
        else:
            result = parse_vdf(data, escape=escape)
            
            print "Result:\n", result
            
            assert result == expected
            
            print "Passed!\n"
        
    print "All parse_vdf() tests passed!"
    return 0
    
    
if __name__ == '__main__':
    assert test_parse_vdf() == 0
    print "All tests passed!"
    
    