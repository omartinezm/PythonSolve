from parse import parse, collapser
from structures import *
import copy

def reduceDiff(expr):
    # Reduce all possible sum and differences operations at time
    n_expr = copy.copy(expr)
    return [Equal(*[reduceDiffArg(arg) for arg in n_expr.args])]

def reduceDiffArg(expr):
    # Collects term by term in a sum
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
            temp = None
            if var_coef ==1:
                temp = var_liter
            elif var_coef == -1:
                temp = Negative(var_liter)
            else:
                temp = Product(Number(var_coef),var_liter)
            if res:
                res = Add(temp,res)
            else:
                res = temp
        else:
            res = Number(0)
        return res
    if len(expr.args)>1:
        n_expr = copy.copy(expr)
        n_expr.args = [reduceDiffArg(arg) for arg in n_expr.args]
        return n_expr

    return expr
   
def addTerm(var_coef,var_liter,expr,positive=True):
    # Add a term to previous computation
    var_liter = var_liter
    if isinstance(expr,Variable):
        var_coef +=1 if positive else -1
        var_liter = expr
    elif isinstance(expr,Product):
        if isinstance(expr.args[0],Number) and isinstance(expr.args[1],Variable):
            var_coef += expr.args[0].value if positive else -expr.args[0].value
            var_liter = expr.args[1]
        elif isinstance(expr.args[1],Number) and isinstance(expr.args[0],Variable):
            var_coef += expr.args[1].value if positive else -expr.args[1].value
            var_liter = expr.args[0]
        elif isinstance(expr.args[0],Negative) and isinstance(expr.args[1],Variable):
            var_coef += expr.args[0].args[0].value if positive else -expr.args[0].args[0].value
            var_liter = expr.args[1]
        elif isinstance(expr.args[1],Negative) and isinstance(expr.args[0],Variable):
            var_coef += expr.args[1].args[0].value if positive else -expr.args[0].args[0].value
            var_liter = expr.args[0]
    return (var_coef,var_liter)
    
def leftToRight(expr):
    left = expr.args[0]
    right = expr.args[1]
    res = [expr]
    if isinstance(left,Add):
        for n, arg in enumerate(left.args):
            term = arg
            n_args = left.args.copy()
            n_args.pop(n)
            temp = None
            if len(n_args)==1:
                temp = n_args[0]
            else:
                temp = Add(*n_args)
            res.append(collapser(Equal(temp,Add(right,Negative(term))) if not isinstance(term,Negative) else Equal(temp,Add(right,term.args[0]))))
    elif isinstance(left,Difference):
        for n, arg in enumerate(left.args):
            term = arg
            n_args = left.args.copy()
            n_args.pop(n)
            temp = None
            if len(n_args)==1:
                temp = n_args[0]
            else:
                temp = Add(*n_args)
            res.append(collapser(Equal(temp,Add(right,term))))
    elif isinstance(left,Variable) or isinstance(left,Number) or isinstance(left,Negative):
        res.append(collapser(Equal(Number(0),Add(right,Negative(left))) if not isinstance(left,Negative) else Equal(Number(0),Add(right,left.args[0]))))
    return res
    
def rightToLeft(expr):
    left = expr.args[0]
    right = expr.args[1]
    res = [expr]
    if isinstance(right,Add):
        for n, arg in enumerate(right.args):
            term = arg
            n_args = right.args.copy()
            n_args.pop(n)
            temp = None
            if len(n_args)==1:
                temp = n_args[0]
            else:
                temp = Add(*n_args)
            res.append(collapser(Equal(Add(left,Negative(term)),temp) if not isinstance(term,Negative) else Equal(Add(left,term.args[0]),temp)))
    elif isinstance(right,Difference):
        for n, arg in enumerate(right.args):
            term = arg
            n_args = right.args.copy()
            n_args.pop(n)
            temp = None
            if len(n_args)==1:
                temp = n_args[0]
            else:
                temp = Add(*n_args)
            res.append(collapser(Equal(Add(left,term),temp)))
    elif isinstance(right,Variable) or isinstance(right,Number) or isinstance(right,Negative):
        res.append(collapser(Equal(Add(left,Negative(right)),Number(0)) if not isinstance(right,Negative) else Equal(Add(left,right.args[0]),Number(0))))
    return res

def productToQuotient(expr):
    left= expr.args[0]
    right= expr.args[1]
    if isinstance(left,Product) and isinstance(left.args[0],Number) and isinstance(right,Number):
        return [Equal(left.args[1],Quotient(right,left.args[0]))]
    elif isinstance(right,Product) and isinstance(right.args[0],Number) and isinstance(left,Number):
        return [Equal(Quotient(left,right.args[0]),right.args[1])]
    else:
        return [expr]

def flip(expr):
    return [Equal(expr.args[1],expr.args[0])]

def reduceQuotient(expr):
    left = expr.args[0]
    right = expr.args[1]
    resL = dummyReduction(left)
    resR = dummyReduction(right)
    if resL[1]:
        return [Equal(resL[0],right)]
    elif resR[1]:
        return [Equal(left,resR[0])]
    return [expr]

def dummyReduction(expr):
    if isinstance(expr,Quotient):
        if isinstance(expr.args[0],Product) and isinstance(expr.args[0].args[0],Number):
            return (Product(Number(expr.args[0].args[0].value/expr.args[1].value),expr.args[0].args[1]),True)
        elif isinstance(expr.args[0],Number):
            return (Number(expr.args[0].value/expr.args[1].value),True)
    return (expr,False)

def multiplyByMinus(expr):
    left = expr.args[0]
    right = expr.args[1]
    left = left.args[0] if isinstance(left,Negative) else Negative(left)
    right = right.args[0] if isinstance(right,Negative) else Negative(right)
    return reduceSign(Equal(left,right))

def reduceSign(expr):
    left = negProduct(expr.args[0])
    right = negProduct(expr.args[1])
    return [Equal(left,right)]


def negProduct(expr):
    """ This function transforms expressions to a better expression
        
        >   Product(Negative(TERM1),TERM2,...) into Negative(Product(TERM1,TERM2,...))
        >   Product(TERM1,Negative(TERM2),...) into Negative(Product(TERM1,TERM2,...))
    """
    if isinstance(expr,Product):
        n_args = []
        negative = False
        for arg in expr.args:
            if isinstance(arg,Negative):
                n_args.extend(negProduct(arg).args)
                negative = not negative
            elif isinstance(arg,Number) and arg.args[0]<0:
                n_args.append(Number(-arg.args[0]))
                negative = not negative
            else:
                n_args.append(arg)
        return Negative(Product(*n_args)) if negative else Product(*n_args)
    else:
        n_expr = copy.copy(expr)
        if len(n_expr.args)>1:
            n_expr.args=[negProduct(arg) for arg in n_expr.args]
        return n_expr

def measure(graph):
    left = graph.args[0]
    right = graph.args[1]
    depthL = depth(left,[1,0])
    depthR = depth(right,[1,0])
    res = (1-depthL[1])**2+(1-depthL[1])**2+(1-depthR[0])**2+(1-depthL[0])**2
    return res

def depth(node,p_res):
    # This function find the depth and the number of leaves. Return a list [depth,leaves].
    res = p_res
    if isinstance(node,Variable) or isinstance(node,Number):
        res[1] += 1
    elif isinstance(node, Negative):
        if isinstance(node.args[0],Number) or isinstance(node.args[0],Variable):
            res[1] += 1
        else:
            res[0] += 1
            for n in node.args:
                res = depth(n,res)
    else:
        res[0] += 1
        for n in node.args:
            res = depth(n,res)
    return res


oper = [reduceDiff,multiplyByMinus,leftToRight,rightToLeft,productToQuotient,reduceQuotient]

input=parse('x+2=1')
def solve(input):
    path = [str(input)]
    max_iter = 10
    curr = input
    curr_measure = measure(input)
    print(curr,"->",curr_measure," (start)")
    while curr_measure>0 and max_iter>0:
        change = False
        for operation in oper:
            new = operation(curr)
            for n in new:
                n_measure = measure(n)
                print(curr,'->',n,': ',operation.__name__,'->',n_measure)
                if n_measure<curr_measure:
                    curr=copy.copy(n)
                    curr_measure=n_measure
                    change = True
            if change:
                path.append(str(curr))
                break
        max_iter-=1
    return path

# inputs = ['x=-1','-x=1','2x=1','-2x=-1','-2x+1=1','-2x+1=-1','x=1']
# inputs = ['x+x=1','-x+x=1','2x-x=1','-2x+x=-1','-2x-x=1','-2x+1=-1','x=1','x+x+1+1=0','x+x+1+1=1+1+2x+2x','x-x+1-1=1']
# inputs = ['-2*=1','-x+x=1','2x-x=1','-2x+x=-1','-2x-x=1','-2x+1=-1','x=1','x+x+1+1=0','x+x+1+1=1+1+2x+2x','x-x+1-1=1']
# inputs = ['2x=3x+1']
# for i in inputs:
#     r = parse(i)
#     for s in rightToLeft(parse(i)):
#         print(r,'->',s,': ',measure(s))


# for t in leftToRight(input):
#     print(t)
print(solve(input))