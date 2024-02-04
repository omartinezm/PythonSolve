class Equal:
    def __init__(self, sideLeft,sideRight) -> None:
        self.args = [sideLeft,sideRight]
        self.name='Equality'
        self.sideLeft=sideLeft
        self.sideRight=sideRight

    def __str__(self) -> str:
        return str(self.args[0])+'='+str(self.args[1])

class Add:
    def __init__(self, term1,term2) -> None:
        self.args = [term1,term2]
        self.name='Sum'
        self.term1=term1
        self.term2=term2

    def __str__(self) -> str:
        return str(self.term1)+'+'+str(self.term2)

class Difference:
    def __init__(self, term1,term2) -> None:
        self.args = [term1,term2]
        self.name='Difference'
        self.term1=term1
        self.term2=term2

    def __str__(self) -> str:
        return str(self.term1)+'-'+str(self.term2)

class Product:
    def __init__(self, factor1,factor2) -> None:
        self.args = [factor1,factor2]
        self.name='Product'
        self.factor1=factor1
        self.factor2=factor2

    def __str__(self) -> str:
        return str(self.factor1)+'*'+str(self.factor2)

class Quotient:
    def __init__(self, numerator,denominator) -> None:
        self.args = [numerator,denominator]
        self.name='Quotient'
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self) -> str:
        return str(self.numerator)+'/'+str(self.denominator)
    
class Number:
    def __init__(self,value) -> None:
        self.args = [value]
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
class Variable:
    def __init__(self,name) -> None:
        self.args = [name]
        self.name=name

    def __str__(self) -> str:
        return str(self.name)
