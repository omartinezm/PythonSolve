from structures import *
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, NAME, ENCODING, ENDMARKER, NEWLINE
from io import BytesIO
import copy

def parse(str):
    left, right= str.split('=')
    tokensL = tokenize(BytesIO(left.encode('utf-8')).readline)
    tokensR = tokenize(BytesIO(right.encode('utf-8')).readline)
    result = [constructTokens(tokensL),constructTokens(tokensR)]
    res = Equal(eval(untokenize(result[0])),eval(untokenize(result[1])))
    return collapser(res)

def collapser(expr):
    if isinstance(expr,Add):
        n_args = [] 
        for arg in expr.args:
            if isinstance(arg,Add):
                n_args.extend(collapser(arg).args)
            else:
                n_args.append(arg)
        return Add(*n_args)
    else:
        n_expr = copy.copy(expr)
        if len(n_expr.args)>1:
            n_expr.args=[collapser(arg) for arg in n_expr.args]
        return n_expr

def constructTokens(tokens):
    result = []
    n_parenthesis = 0
    for toknum, tokval, _, _, _ in tokens:
        if toknum == NUMBER:
            result.extend([(NAME,'Number'),(OP,'('),(NUMBER,tokval),(OP,')')])
            if n_parenthesis>0:
                result.extend([(OP,')')]*n_parenthesis)
                n_parenthesis=0
        elif toknum == OP:
            if tokval == '+':
                result.insert(0,(OP,'('))
                result.insert(0,(NAME,'Add'))
                result.extend([(OP,',')])
            elif tokval == '-':
                if len(result)>0:
                    result.insert(0,(OP,'('))
                    result.insert(0,(NAME,'Add'))
                    result.extend([(OP,',')])
                    n_parenthesis+=1
                result.extend([(NAME,'Negative'),(OP,'(')])
            n_parenthesis+=1
        elif toknum == NAME:
            if len(result)>0:
                if result[-1][1] in [',','(']:
                    result.extend([(NAME,'Variable'),(OP,'('),(NAME,repr(str(tokval))),(OP,')')])
                else:
                    index = -1
                    (ptoknum,ptokval)=result[index]
                    while ptoknum != NAME:
                        index -= 1
                        (ptoknum,ptokval)=result[index]
                    result[len(result)+index:len(result)+index] = [(NAME,'Product'),(OP,'(')]
                    result[len(result)+index+4:len(result)+index+4] = [(OP,','),(NAME,'Variable'),(OP,'('),(NAME,repr(str(tokval))),(OP,')'),(OP,')')]
                result.extend([(OP,')')]*n_parenthesis)
                n_parenthesis=0
            else:
                result.extend([(NAME,'Variable'),(OP,'('),(NAME,repr(str(tokval))),(OP,')')])
        elif toknum in [ENCODING, NEWLINE, ENDMARKER]:
            continue
        else:
            result.extend((toknum,tokval))
    r = [t[1] for t in result]
    print("".join(r))
    return result

parse('1=1-2x')
parse('1=2+2x')
parse('1=1-x')
parse('1=x-x')
parse('1=1-1')
parse('1=1+2')
parse('-1=-1')
parse('1=2x+1+x')
parse('x-x=1')