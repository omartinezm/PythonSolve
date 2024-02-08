class Equal:
    def __init__(self, sideLeft,sideRight) -> None:
        self.args = [sideLeft,sideRight]
        self.name='Equality'

    def __str__(self) -> str:
        return str(self.args[0])+'='+str(self.args[1])
    
    def __name__(self) -> str:
        return 'equal'

class Add:
    def __init__(self, *kwargs) -> None:
        self.args = [*kwargs]
        self.name='Sum'

    def __str__(self) -> str:
        return "+".join([str(k) for k in self.args])
    
    def __name__(self) -> str:
        return 'add'

class Negative:
    def __init__(self,value) -> None:
        self.args = [value]
    
    def __str__(self) -> str:
        return '-('+str(self.args[0])+')'
    
    def __name__(self) -> str:
        return 'negative'

class Difference:
    def __init__(self, term1,term2) -> None:
        self.args = [term1,Negative(term2)]
        self.name='Difference'

    def __str__(self) -> str:
        return str(self.args[0])+'-'+str(self.args[1])
    
    def __name__(self) -> str:
        return 'difference'

class Product:
    def __init__(self, factor1,factor2) -> None:
        self.args = [factor1,factor2]
        self.name='Product'

    def __str__(self) -> str:
        return str(self.args[0])+'*'+str(self.args[1])
    
    def __name__(self) -> str:
        return 'product'

class Quotient:
    def __init__(self, numerator,denominator) -> None:
        self.args = [numerator,denominator]
        self.name='Quotient'

    def __str__(self) -> str:
        return str(self.args[0])+'/'+str(self.args[1])
    
    def __name__(self) -> str:
        return 'quotient'
    
class Number:
    def __init__(self,value) -> None:
        self.args = [value]
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
    def __name__(self) -> str:
        return 'number'
    
class Variable:
    def __init__(self,name) -> None:
        self.args = [name]
        self.name=name

    def __str__(self) -> str:
        return str(self.name)
    
    def __name__(self) -> str:
        return 'variable'