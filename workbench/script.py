"""Small Clausewitz-script reader: preserves duplicate keys and bare lists."""
import re

def parse(text):
    tokens=re.findall(r'"(?:[^"\\]|\\.)*"|#[^\n]*|[{}=]|[^\s{}=#]+',text)
    tokens=[t for t in tokens if not t.startswith('#')]; index=0
    def block(nested=False):
        nonlocal index
        result=[]
        while index<len(tokens):
            key=tokens[index];index+=1
            if key=='}':
                if not nested:raise ValueError('Unexpected closing brace')
                return result
            if key in ['{','=']:raise ValueError('Unexpected token '+key)
            value=None
            if index<len(tokens) and tokens[index]=='=':
                index+=1
                if index==len(tokens):raise ValueError('Missing value for '+key)
                value=tokens[index];index+=1
                if value=='{':value=block(True)
                elif value in ['}','=']:raise ValueError('Missing value for '+key)
            result.append((key,value))
        if nested:raise ValueError('Unclosed block')
        return result
    return block()

def first(ast,key,default=None):return next((v for k,v in ast if k==key),default)
def descend(ast):
    for k,v in ast:
        yield k,v
        if isinstance(v,list):yield from descend(v)
def dump(ast,level=0):
    return '\n'.join('\t'*level+k+(' = {\n'+dump(v,level+1)+'\n'+'\t'*level+'}' if isinstance(v,list) else ' = '+v if v is not None else '') for k,v in ast)
def replace(ast,key,value):
    for i,(k,v) in enumerate(ast):
        if k==key:ast[i]=(key,value);return
    ast.append((key,value))
