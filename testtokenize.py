from vdfutils import *
from vdfutils import _tokenize_vdf

# General
assert list(_tokenize_vdf('')) == []
assert list(_tokenize_vdf('   ')) == []
assert list(_tokenize_vdf('abc')) == [Field('abc')]
assert list(_tokenize_vdf('abc def')) == [Field('abc'), Field('def')]
assert list(_tokenize_vdf('abc def     ghi')) == [
    Field('abc'), Field('def'), Field('ghi')
]
assert list(_tokenize_vdf('abc def  {}   ghi')) == [
    Field('abc'), Field('def'), OpenBrace(), CloseBrace(), Field('ghi')
]
assert list(_tokenize_vdf('abc def  {}   {ghi}')) == [
    Field('abc'), Field('def'), OpenBrace(), CloseBrace(), OpenBrace(),
    Field('ghi'), CloseBrace()
]
assert list(_tokenize_vdf('abc def  {}   {"ghi"}')) == [
    Field('abc'), Field('def'), OpenBrace(), CloseBrace(), OpenBrace(),
    Field('ghi'), CloseBrace()
]
assert list(_tokenize_vdf('"abc def  {}   {ghi}"')) == [
    Field('abc def  {}   {ghi}')
]
assert list(_tokenize_vdf('"abc def  {}   ""{ghi}"')) == [
    Field('abc def  {}   '), Field('{ghi}')
]
assert list(_tokenize_vdf('"abc"def  {}   ""{ghi}')) == [
    Field('abc'), Field('def'), OpenBrace(), CloseBrace(), Field(''),
    OpenBrace(), Field('ghi'), CloseBrace()
]
assert list(_tokenize_vdf('"abc"def"ghi"jkl"mno"')) == [
    Field('abc'), Field('def'), Field('ghi'), Field('jkl'), Field('mno')
]
assert list(_tokenize_vdf('"\\abc\\""def"ghi"jkl"m\\no"')) == [
    Field('\\abc"'), Field('def'), Field('ghi'), Field('jkl'), Field('m\no')
]
assert list(_tokenize_vdf('""""""')) == [
    Field(''), Field(''), Field('')
]

# Escape chars
assert list(_tokenize_vdf('\\')) == [Field('\\')]
assert list(_tokenize_vdf('\\n')) == [Field('\n')]
assert list(_tokenize_vdf('\\t')) == [Field('\t')]
assert list(_tokenize_vdf('\\"')) == [Field('"')]
assert list(_tokenize_vdf('\\\\"')) == [Field('\\"')]
assert list(_tokenize_vdf('\\\\')) == [Field('\\')]
assert list(_tokenize_vdf('\\\\\\')) == [Field('\\\\')]
assert list(_tokenize_vdf('\\\\\\\\')) == [Field('\\\\')]
assert list(_tokenize_vdf('\\\\\\\\t')) == [Field('\\\\t')]
assert list(_tokenize_vdf('\\\\\\\\\\t')) == [Field('\\\\\t')]

# Bad VDF

try:
    list(_tokenize_vdf('"'))
    assert False
except VDFConsistencyFailure as e:
    assert e.message == 'Mismatched quotes!'
    
try:
    list(_tokenize_vdf('"abc def  {}   ""{ghi}""'))
    assert False
except VDFConsistencyFailure as e:
    assert e.message == 'Mismatched quotes!'
    
try:
    list(_tokenize_vdf('"""""'))
    assert False
except VDFConsistencyFailure as e:
    assert e.message == 'Mismatched quotes!'
    
# Comments
assert list(_tokenize_vdf('//')) == []
assert list(_tokenize_vdf('// abc')) == []
assert list(_tokenize_vdf('// abc def')) == []
assert list(_tokenize_vdf('// abc def\nghi')) == [Field('ghi')]
assert list(_tokenize_vdf('/ abc def\nghi')) == [Field('ghi')]
assert list(_tokenize_vdf('"/"')) == [Field('/')]
assert list(_tokenize_vdf('/"')) == []

print "All tests passed!"

