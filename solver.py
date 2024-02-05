from parseEQ import parse
from structures import *
import copy

strut = ['equal','add','negative','difference','product','quotient','number','variable']

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
        con_coef = 0
        var_coef = 0
        var_liter = None
        for arg in expr.args:
            (var_coef,var_liter) = addTerm(var_coef,var_liter,arg,)
            if isinstance(arg,Number):
                con_coef+=arg.value
            elif isinstance(arg,Negative):
                if isinstance(arg.args[0],Number):
                    con_coef-=arg.args[0].value
                else:
                    (var_coef,var_liter) = addTerm(var_coef,var_liter,arg.args[0],False)
        res = None
        if con_coef:
            res = Number(con_coef)
        if var_coef:
            if res:
                res = Add(Product(Number(var_coef),var_liter),res) if var_liter else Add(var_liter,res)
            else:
                res = Product(Number(var_coef),var_liter) if var_liter else var_liter
        return res
    if len(expr.args)>1:
        n_expr = copy.copy(expr)
        n_expr.args = [reduceDiffArg(arg) for arg in n_expr.args]
        return n_expr

    return expr
   
def addTerm(var_coef,var_liter,expr,positive=True):
    var_liter = var_liter
    if isinstance(expr,Variable):
        var_coef +=1
        var_liter = expr
    elif isinstance(expr,Product):
        if isinstance(expr.args[0],Number) and isinstance(expr.args[1],Variable):
            var_coef += expr.args[0].value if positive else -expr.args[0].value
            var_liter = expr.args[1]
        if isinstance(expr.args[1],Number) and isinstance(expr.args[0],Variable):
            var_coef += expr.args[1].value if positive else -expr.args[0].value
            var_liter = expr.args[0]
        if isinstance(expr.args[0],Negative) and isinstance(expr.args[1],Variable):
            var_coef += expr.args[0].args[0].value if positive else -expr.args[0].args[0].value
            var_liter = expr.args[1]
        if isinstance(expr.args[1],Negative) and isinstance(expr.args[0],Variable):
            var_coef += expr.args[1].args[0].value if positive else -expr.args[0].args[0].value
            var_liter = expr.args[0]
    return (var_coef,var_liter)
    
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
    if isinstance(left,Product) and isinstance(left.args[0],Number) and isinstance(right,Number):
        return Equal(left.args[1],Quotient(right,left.args[0]))
    elif isinstance(right,Product) and isinstance(right.args[0],Number) and isinstance(left,Number):
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

# input = parse('2=x+2x')
input=parse('1=x-2x+3-2')
def solve(input):
    path = [str(input)]
    max_iter = 1
    curr = input
    curr_measure = measure(input)
    print(curr,"->",curr_measure," (start)")
    while curr_measure>0 and max_iter>0:
        for operation in oper:
            new = operation(curr)
            n_measure = measure(new)
            print(curr,'->',new,': ',operation,'->',n_measure)
            if n_measure<curr_measure:
                curr=copy.copy(new)
                curr_measure=n_measure
                path.append(str(curr))
                break
        max_iter-=1
    return path

# print(reduceDiff(input))
print(solve(input))