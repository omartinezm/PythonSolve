from parseEQ import parse
from structures import *

def reduceAdd(arg):
    left = arg.sideLeft
    right = arg.sideRight
    change = False
    if isinstance(left,Add):
        term1=left.term1
        term2=left.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                left = Product(num,term1.factor2)
                change = True
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            left = Number(num)
            change = True
    elif isinstance(right,Add):
        term1=right.term1
        term2=right.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value+num2.value
                right = Product(num,term1.factor2)
                change = True
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value+term2.value
            right = Number(num)
            change = True
    return Equal(left,right)

def reduceDiff(arg):
    left = arg.sideLeft
    right = arg.sideRight
    if isinstance(left,Difference):
        term1=left.term1
        term2=left.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value-num2.value
                left = Product(num,term1.factor2)
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value-term2.value
            left = Number(num)
    elif isinstance(right,Difference):
        term1=right.term1
        term2=right.term2
        if isinstance(term1,Product) and isinstance(term2,Product):
            num1=term1.factor1
            num2=term2.factor1
            if isinstance(num1,Number) and isinstance(num2,Number):
                num = num1.value-num2.value
                right = Product(num,term1.factor2)
        elif isinstance(term1,Number) and isinstance(term2,Number):
            num = term1.value-term2.value
            right = Number(num)
    return Equal(left,right)
    
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


input = parse('x+1=0')
def solve(input):
    end=False
    output=input
    path = [input]
    max_iter =20
    while not end and max_iter>0:
        if isinstance(output.sideLeft,Variable) and isinstance(output.sideRight,Number):
            print("END")
            end = True
        else:
            output=reduceAdd(output)
            output=reduceDiff(output)
            output=leftToRight(output)
            output=rightToLeft(output)
            max_iter-=1
    return output

print(solve(input))