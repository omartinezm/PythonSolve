from structures import *
from tokenize import tokenize, untokenize, NUMBER, NAME, OP, NAME, ENCODING, ENDMARKER, NEWLINE
from io import BytesIO
import copy

def parse(str):
    """ This function parse the string into something readable for the machine
    
        This parser works only on expressions of first degree. Can be extended to any other
        kind of mathematical expressions.
    """
    if str.find('=') == -1:
        tokens = tokenize(BytesIO(str.encode('utf-8')).readline)
        result = constructTokens(tokens)
        res = eval(untokenize(result))
        return collapser(res)
    else:
        left, right= str.split('=')
        tokensL = tokenize(BytesIO(left.encode('utf-8')).readline)
        tokensR = tokenize(BytesIO(right.encode('utf-8')).readline)
        result = [constructTokens(tokensL),constructTokens(tokensR)]
        res = Equal(eval(untokenize(result[0])),eval(untokenize(result[1])))
        return standarize(res)

def standarize(expr):
    n_expr = collapser(expr)
    n_expr = negNumber(n_expr)
    return n_expr

def collapser(expr):
    """ This function transforms expressions to a better expression
        
        >   Add(Add(1,2),3) into Add(1,2,3)
        >   Product(Negative(TERM1),TERM2) into Negative(Product(TERM1,TERM2))
    """
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

def negNumber(expr):
    # This function transform "Negative(Number(x))"" into "Number(-x)"
    if isinstance(expr,Negative):
        if isinstance(expr.args[0],Number):
            return Number(-expr.args[0].args[0])
    else:
        if len(expr.args)>1:
            n_expr = copy.copy(expr)
            n_args = []
            for arg in n_expr.args:
                n_args.append(negNumber(arg))
            n_expr.args = n_args
            return n_expr
    return expr


def constructTokens(tokens):
    """ Heart of the parser: transform the tokens into readable object.

        Returns a list of new tokens.
    """
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
    return result
