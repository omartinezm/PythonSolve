from parse import parse, standarize
from structures import *
import copy

def reduceSum(expr):
    """ This function reduces one posible operation of sum each side of the equality
    """
    left = reduceTerm(expr.args[0])
    right = reduceTerm(expr.args[1])
    if left[1] or right[1]:
        return ([Equal(left[0],right[0])],True)
    return ([expr], False)

def reduceTerm(expr):
    """ Utility to redice two terms
    """
    var_coef = 0
    con_coef = 0
    for n1,arg1 in enumerate(expr.args):
        for n2,arg2 in enumerate(expr.args[n1+1:]):
            if isinstance(arg1,Number) and isinstance(arg2,Number):
                con_coef = arg1.args[0]+arg2.args[0]
                n_args=expr.args
                n_args.pop(n2)
                n_args.pop(n1)
                if con_coef != 0 or len(n_args)==0:
                    n_args.append(Number(con_coef))
                return (Add(*n_args),True)
            if isinstance(arg1,Variable) and isinstance(arg2,Variable):
                con_coef = 2
                n_args=expr.args
                n_args.pop(n2)
                n_args.pop(n1)
                n_args.append(Product(con_coef,arg1.args[0]))
                return (Add(*n_args),True)
            elif isinstance(arg1,Product) and isinstance(arg2,Variable):
                added = False
                if isinstance(arg1.args[0],Number) and isinstance(arg1.args[1],Variable):
                    added = True
                    var_coef += arg1.args[0].args[0]+1
                elif isinstance(arg1.args[1],Number) and isinstance(arg1.args[1],Variable):
                    added = True
                    var_coef += arg1.args[1].args[0]+1
                if added:
                    n_args=expr.args
                    n_args.pop(n2)
                    n_args.pop(n1)
                    if var_coef==0:
                        n_args.append(Number(0))
                    elif var_coef==0:
                        n_args.append(arg2.args[0])
                    else:
                        n_args.append(Product(Number(var_coef),arg2.args[0]))
                    if len(n_args)==1:
                        return (n_args[0],True)
                    else:
                        return (Add(*n_args),True)
            elif isinstance(arg1,Variable) and isinstance(arg2,Product):
                added = False
                if isinstance(arg2.args[0],Number) and isinstance(arg2.args[1],Variable):
                    added = True
                    var_coef += arg2.args[0].args[0]+1
                elif isinstance(arg2.args[1],Number) and isinstance(arg2.args[1],Variable):
                    added = True
                    var_coef += arg2.args[1].args[0]+1
                if added:
                    n_args=expr.args
                    n_args.pop(n2)
                    n_args.pop(n1)
                    if var_coef==0:
                        n_args.append(Number(0))
                    elif var_coef ==1:
                        n_args.append(arg1.args[0])
                    else:
                        n_args.append(Product(Number(var_coef),arg1.args[0]))
                    if len(n_args)==1:
                        return (n_args[0],True)
                    else:
                        return (Add(*n_args),True)
            elif isinstance(arg1,Product) and isinstance(arg2,Product):
                added = False
                if isinstance(arg1.args[0],Number) and isinstance(arg1.args[1],Variable) and isinstance(arg2.args[0],Number) and isinstance(arg2.args[1],Variable):
                    added = True
                    var_coef += arg1.args[0].args[0]+arg2.args[0].args[0]
                if added:
                    n_args=expr.args
                    n_args.pop(n2)
                    n_args.pop(n1)
                    if var_coef==0:
                        n_args.append(Number(0))
                    elif var_coef == 1:
                        n_args.append(arg1.args[1])
                    else:
                        n_args.append(Product(Number(var_coef),arg1.args[1]))
                    if len(n_args)==1:
                        return (n_args[0],True)
                    else:
                        return (Add(*n_args),True)
            elif isinstance(arg1,Negative) or isinstance(arg2,Negative):
                res = None
                if isinstance(arg1,Negative) and not isinstance(arg2,Negative):
                    dummy_expr = Add(Product(Number(-1),arg1.args[0]),arg2)
                elif not isinstance(arg1,Negative) and isinstance(arg2,Negative):
                    dummy_expr = Add(arg1,Product(Number(-1),arg2.args[0]))
                else:# isinstance(arg1,Negative) and isinstance(arg2,Negative):
                    dummy_expr = Add(Product(Number(-1),arg1.args[0]),Product(Number(-1),arg2))
                res = reduceTerm(dummy_expr)
                if res[1]:
                    n_args=expr.args
                    n_args.pop(n2)
                    n_args.pop(n1)
                    n_args.append(res[0])
                    if len(n_args) == 0:
                        return (n_args[0],True)
                    else:
                        return (Add(*n_args),True)
    return (expr,False)
    
def leftToRight(expr):
    """ Moves a term from the left to right of que equation
    """
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
            res.append(standarize(Equal(temp,Add(right,Negative(term))) if not isinstance(term,Negative) else Equal(temp,Add(right,term.args[0]))))
            print('---->',res[-1])
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
            res.append(standarize(Equal(temp,Add(right,term))))
    elif isinstance(left,Variable) or isinstance(left,Number) or isinstance(left,Negative):
        res.append(standarize(Equal(Number(0),Add(right,Negative(left))) if not isinstance(left,Negative) else Equal(Number(0),Add(right,left.args[0]))))
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
            res.append(standarize(Equal(Add(left,Negative(term)),temp) if not isinstance(term,Negative) else Equal(Add(left,term.args[0]),temp)))
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
            res.append(standarize(Equal(Add(left,term),temp)))
    elif isinstance(right,Variable) or isinstance(right,Number) or isinstance(right,Negative):
        res.append(standarize(Equal(Add(left,Negative(right)),Number(0)) if not isinstance(right,Negative) else Equal(Add(left,right.args[0]),Number(0))))
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
    return standarize(Equal(left,right))

# def reduceSign(expr):
#     left = negProduct(expr.args[0])
#     right = negProduct(expr.args[1])
#     return [standarize(Equal(left,right))]

def measure(graph):
    left = graph.args[0]
    right = graph.args[1]
    depthL = depth(left,[1,0])
    depthR = depth(right,[1,0])
    res = (depthL[1]-1)**2+(1-depthL[1])**2+(1-depthR[0])**2+(1-depthL[0])**2
    return res

def depth(node,p_res):
    # This function find the depth of the graph. Return a list [depth,leaves].
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


oper = [reduceSum,multiplyByMinus,leftToRight,rightToLeft,productToQuotient,reduceQuotient]

input=parse('x+2=1')


path = []

def solve(input,path,solved=False):
    """
        This function search the path from the equation graph to a graph in the form
            Variable('x')=Number(a)
    """
    max_iter = 3
    curr = input
    curr_measure = measure(input)
    print(curr,"->",curr_measure," (start)")
    while (not solved and max_iter>0):
        for operation in oper:
            new = operation(curr)
            for n in new:
                n_measure = measure(n)
                path.append(n)
                if n_measure == 0:
                    solved = True
                    print(path)
                    break
                else:
                    solve(n,path,solved)
        max_iter-=1
    return path

# inputs = ['x=-1','-x=1','2x=1','-2x=-1','-2x+1=1','-2x+1=-1','x=1']
inputs = ['x+x=1','-x+x=1','2x-x=1','-2x+x=-1','-2x-x=1','-2x+1=-1','x=1','x+x+1+1=0','x+x+1+1=1+1+2x+2x','x-x+1-1=1']
# inputs = ['-2*=1','-x+x=1','2x-x=1','-2x+x=-1','-2x-x=1','-2x+1=-1','x=1','x+x+1+1=0','x+x+1+1=1+1+2x+2x','x-x+1-1=1']
# inputs = ['-2x-x=1']
for i in inputs:
    r = parse(i)
    s = reduceSum(reduceSum(parse(i))[0])
    print(r,'->',s[0])


# for t in leftToRight(input):
#     print(t)
# print(solve(input,[]))