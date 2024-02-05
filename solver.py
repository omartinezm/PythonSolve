from parseEQ import parse
from structures import *
import copy

strut = ['equal','add','negative','difference','product','quotient','number','variable']

def collapser(expr):
    if isinstance(expr,Add) and isinstance(expr.args[0],Add):
        return Add(expr.args[0],expr.args[0].args[0])
    else:
        n_expr = copy.copy(expr)
        if len(n_expr.args)>1:
            n_expr.args=[collapser(arg) for arg in n_expr.args]
        return n_expr

def reduceAdd(expr):
    left = expr.args[0]
    right = expr.args[1]
    if isinstance(left,Add):
        term1=left.args[0]
        term2=left.args[1]
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.args[0]
            num2=term2.args[0]
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                left = Product(num,term1.args[1])
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            left = Number(num)
    elif isinstance(right,Add):
        term1=right.args[0]
        term2=right.args[1]
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.args[0]
            num2=term2.args[0]
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                right = Product(num,term1.args[1])
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            right = Number(num)
    n_expr = expr.__copy__()
    n_expr.args=[left,right]
    return n_expr

def reduceDiff(expr):
    n_expr = copy.copy(expr)
    return Equal(*[reduceDiffArg(arg) for arg in n_expr.args])

def reduceDiffArg(expr):
    if isinstance(expr,Difference):
        term1=expr.args[0]
        term2=expr.args[1]
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.args[0]
            num2=term2.args[0]
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value-num2.value
                return Product(Number(num),term1.args[1])
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value-term2.value
            return Number(num)
    if isinstance(expr,Add):
        term1=expr.args[0]
        term2=expr.args[1]
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.args[0]
            num2=term2.args[0]
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                return Product(Number(num),term1.args[1])
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            return Number(num)
    if len(expr.args)>1:
        n_expr = copy.copy(expr)
        n_expr.args = [reduceDiffArg(arg) for arg in n_expr.args]
        return n_expr

    return expr
   
    
def leftToRight(expr):
    left= expr.args[0]
    right= expr.args[1]
    if isinstance(left,Add):
        return Equal(left.args[0],Difference(right,left.args[1]))
    elif isinstance(left,Difference):
        return Equal(left.args[0],Add(right,left.args[1]))
    return expr
    
def rightToLeft(expr):
    left= expr.args[0]
    right= expr.args[1]
    if isinstance(right,Add):
        return Equal(Difference(left,right.args[1]),right.args[0])
    elif isinstance(right,Difference):
        return Equal(Add(left,right.args[1]),right.args[0])
    return expr

def productToQuotient(expr):
    left= expr.args[0]
    right= expr.args[1]
    if isinstance(left,Product) and isinstance(left.args[0],Number):
        return Equal(left.args[1],Quotient(right,left.args[0]))
    elif isinstance(right,Product) and isinstance(right.args[0],Number):
        return Equal(Quotient(left,right.args[0]),right.args[1])
    else:
        return expr

def flip(expr):
    return Equal(expr.args[1],expr.args[0])

def reduceQuotient(expr):
    left = expr.args[0]
    right = expr.args[1]
    resL = dummyReduction(left)
    resR = dummyReduction(right)
    if resL[1]:
        return Equal(resL[0],right)
    elif resR[1]:
        return Equal(left,resR[0])
    return expr

def dummyReduction(expr):
    if isinstance(expr,Quotient):
        if isinstance(expr.args[0],Product) and isinstance(expr.args[0].args[0],Number):
            return (Product(Number(expr.args[0].args[0].value/expr.args[1].value),expr.args[0].args[1]),True)
        elif isinstance(expr.args[0],Number):
            return (Number(expr.args[0].value/expr.args[1].value),True)
    return (expr,False)

def measure(graph):
    if isinstance(graph.args[0],Variable) and isinstance(graph.args[1],Number):
        return 0
    left = graph.args[0]
    right = graph.args[1]
    depthL = measureDepth(left,1)
    depthR = measureDepth(right,1)
    res = (depthL+depthR)**2
    return res

def measureDepth(node,result):
    if isinstance(node,Variable):
        return result*0.5
    else:
        if len(node.args)>1:
            res = [measureDepth(n,result+1) for n in node.args]
        else:
            res = [result]
        return max(res)


oper = [reduceDiff,leftToRight,rightToLeft,productToQuotient,reduceQuotient,flip]

input = parse('-1=2x')
# input = productToQuotient(input)
def solve(input):
    curr = collapser(input)
    path = [str(input)]
    max_iter =10
    curr_measure = measure(input)
    print(curr,"->",curr_measure," (start)")
    while curr_measure>0 and max_iter>0:
        for operation in oper:
            new = operation(curr)
            n_measure = measure(new)
            new = collapser(new)
            print(curr,'->',new,': ',operation,'->',n_measure)
            if n_measure<curr_measure:
                # print(curr,"->",new,"->",n_measure," ("+str(operation)+")")
                # print(operation)
                curr=copy.copy(new)
                curr_measure=n_measure
                path.append(str(curr))
                break
        max_iter-=1
    return path

# input=productToQuotient(input)
# print(input)
# input=reduceQuotient(input)

# print(measure(input))
# input = parse('2=x+5x')
# print(leftToRight(input))
# input="1+2+3"
print(solve(input))