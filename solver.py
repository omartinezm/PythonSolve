from parseEQ import parse
from structures import *
import copy

def reduceAdd(expr):
    left = expr.args[0]
    right = expr.args[1]
    if isinstance(left,Add):
        term1=left.term1
        term2=left.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                left = Product(num,term1.factor2)
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            left = Number(num)
    elif isinstance(right,Add):
        term1=right.term1
        term2=right.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                right = Product(num,term1.factor2)
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            right = Number(num)
    n_expr = expr.__copy__()
    n_expr.args=[left,right]
    return n_expr

def reduceDiff(expr):
    n_expr = copy.copy(expr)
    return Equal(*[reduceDiffArg(arg) for arg in n_expr.args])
    n_expr.args([reduceDiffArg(arg) for arg in n_expr.args])
    return n_expr

def reduceDiffArg(expr):
    print(expr)
    if isinstance(expr,Difference):
        term1=expr.term1
        term2=expr.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value-num2.value
                return Product(num,term1.factor2)
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value-term2.value
            return Number(num)
    if isinstance(expr,Add):
        term1=expr.term1
        term2=expr.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                return Product(num,term1.factor2)
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            return Number(num)
    if len(expr.args)>1:
        for arg in expr.args:
            n_expr = copy.copy(arg)
            return reduceDiff(n_expr)
    return expr
   
    
def leftToRight(arg):
    left= arg.sideLeft
    right= arg.sideRight
    if isinstance(left,Add):
        return Equal(left.term1,Difference(right,left.term2))
    elif isinstance(left,Difference):
        return Equal(left.term1,Add(right,left.term2))
    return arg
    
def rightToLeft(arg):
    left= arg.sideLeft
    right= arg.sideRight
    if isinstance(right,Add):
        return Equal(Difference(left,right.term2),right.term2)
    elif isinstance(left,Difference):
        return Equal(Add(left,right.term2),right.term2)
    return arg

def productToQuotient(arg):
    left= arg.sideLeft
    right= arg.sideRight
    if isinstance(left,Product) and isinstance(left.factor1,Number):
        return Equal(left.factor2,Quotient(right,left.factor1))
    elif isinstance(right,Product) and isinstance(right.factor1,Number):
        return Equal(Quotient(left,right.factor1),right.factor2)
    else:
        return arg
    
def reduceQuotient(arg):
    left= arg.sideLeft
    right= arg.sideRight
    resL = dummyReduction(left)
    resR = dummyReduction(right)
    if resL[1]:
        return Equal(resL[0],right)
    elif resR[1]:
        return Equal(left,resR[0])
    return arg

def dummyReduction(expr):
    if isinstance(expr,Quotient):
        if isinstance(expr.args[0],Product) and isinstance(expr.args[0].factor1,Number):
            return [Product(Number(expr.args[0].factor1.value/expr.args[1].value),expr.args[0].factor2),True]
        elif isinstance(expr.args[0],Number):
            return [Number(expr.args[0].value/expr.args[1].value),True]
    else:
        return [expr,False]

def measure(graph):
    depthL = measureDepth(graph.args[0],0)
    depthR = measureDepth(graph.args[1],0)
    res = (depthL+depthR)**2*depthL
    return res

def measureDepth(node,result):
    if len(node.args)==1:
        return result
    else:
        res = [measureDepth(n,result+1) for n in node.args]
        return max(res)


oper = [reduceAdd,reduceDiff,leftToRight,rightToLeft,productToQuotient,reduceQuotient]

input = parse('x+2=2+3')
def solve(input):
    curr = input
    path = [str(input)]
    max_iter =40
    curr_measure = measure(input)
    while curr_measure>0 and max_iter>0:
        for operation in oper:
            new = operation(curr)
            print(new)
            n_measure = measure(new)
            if n_measure<curr_measure:
                # print(operation)
                curr=new
                curr_measure=n_measure
                path.append(str(curr))
        max_iter-=1
    return list(set(path))

# input=productToQuotient(input)
# input=reduceQuotient(input)

# print(measure(input))
input = parse('x=2-3+3')
print(reduceDiff(input))
# print(solve(input))