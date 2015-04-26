import sys
import os

from vdfutils import parse_vdf, format_vdf, VDFConsistencyFailure, UNIQUEIFIER

PARSE_VDF_DIR = 'parse_vdf'
PARSE_VDF_TEST_CASES = (
    (
        'test1.vdf',
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
        VDFConsistencyFailure("Brackets have no heading!"),
    ),
    (
        'test6.vdf',
        VDFConsistencyFailure("Mismatched brackets!"),
    ),
    (
        'test7.vdf',
        VDFConsistencyFailure("Mismatched brackets!"),
    ),
    (
        'test8.vdf',
        {
            'This'  :   'is',
            'some'  :   'perfectly',
            'valid' :   'data.',
        },
    ),
    (
        'test9.vdf',
        VDFConsistencyFailure("Key without value!"),
    ),
    (
        'test10.vdf',
        {
            'foo'   :   'repeat',
        },
    ),
    (
        'test11.vdf',
        {},
    ),
    (
        'test12.vdf',
        {
            'visible'   :   'value',
            'can'       :   {
                'see'   :   'everything',
                'in'    :   'here',
            },
        },
    ),
)


def test_parse_vdf():
    for file, expected in PARSE_VDF_TEST_CASES:
        with open(os.path.join(PARSE_VDF_DIR, file), 'r') as f:
            data = f.read()
            
        print "Testing {}...".format(file)
        print "Expected:\n", expected
        
        if (type(expected) is not dict and
                issubclass(expected.__class__, Exception)):
            
            result = None
            try:
                result = parse_vdf(data, ordered=False)
                
            except expected.__class__ as e:
                print "Result:\n", e
                
                assert str(e) == str(expected)
                
                print "Passed!\n"
                continue
                
            print "Result:\n", result
            assert result is None
            
        else:
            result = parse_vdf(data, ordered=False)
            
            print "Result:\n", result
            
            assert parse_vdf(data) == expected
            
            print "Passed!\n"
        
    print "All parse_vdf() tests passed!"
    return 0
    
    
if __name__ == '__main__':
    assert test_parse_vdf() == 0
    
    print "All tests passed!"
    
    