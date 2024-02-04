from structures import *
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, NAME, ENCODING, ENDMARKER, NEWLINE
from io import BytesIO

def parse(str):
    left, right= str.split('=')
    tokensL = tokenize(BytesIO(left.encode('utf-8')).readline)
    tokensR = tokenize(BytesIO(right.encode('utf-8')).readline)
    result = [constructTokens(tokensL),constructTokens(tokensR)]
    res = Equal(eval(untokenize(result[0])),eval(untokenize(result[1])))
    return res

def constructTokens(tokens):
    result = []
    n_parenthesis = 0
    for toknum, tokval, _, _, _ in tokens:
        if toknum == NUMBER:
            result.extend([(NAME,'Number'),(OP,'('),(NUMBER,tokval),(OP,')')])
            if n_parenthesis>0:
                result.extend([(OP,')')]*n_parenthesis)
                n_parenthesis=0
        elif toknum == NAME:
            if len(result)>0:
                (_,ptokval)=result[-1]
                if ptokval!=',':
                    index = -1
                    while ptokval!='(':
                        index-=1
                        (_,ptokval)=result[index]
                    result[len(result)+index-1:len(result)+index-1] = [(NAME,'Product'),(OP,'(')]
                    result[len(result)+index+3:len(result)+index+3] = [(OP,','),(NAME,'Variable'),(OP,'('),(NAME,repr(str(tokval))),(OP,')'),(OP,')')]
                else:
                    result.extend([(NAME,'Variable'),(OP,'('),(NAME,repr(str(tokval))),(OP,')')])
            else:
                result.extend([(NAME,'Variable'),(OP,'('),(NAME,repr(str(tokval))),(OP,')')])
            if n_parenthesis>0:
                result.extend([(OP,')')]*n_parenthesis)
                n_parenthesis=0
        elif toknum == OP:
            if tokval == '+':
                result.insert(0,(OP,'('))
                result.insert(0,(NAME,'Add'))
                result.extend([(OP,',')])
            elif tokval == '-':
                result.insert(0,(OP,'('))
                result.insert(0,(NAME,'Add'))
                result.extend([(OP,','),(NAME,'Negative'),(OP,'(')])
                n_parenthesis+=1
            n_parenthesis+=1
        elif toknum in [ENCODING, NEWLINE, ENDMARKER]:
            continue
        else:
            result.extend((toknum,tokval))
    # r = [t[1] for t in result]
    # print("".join(r))
    return result

print(parse("3+2-1=x"))