import ast
import operator as op
from functions import delinquency_count, debt_to_income

operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg, ast.Lt: op.lt, ast.LtE: op.le, ast.Gt: op.gt, ast.GtE: op.ge, ast.Eq: op.eq, ast.NotEq: op.ne}

class Parser:
    def __init__(self):
        self.functions = {"delinquency_count" : delinquency_count,
                          "debt_to_income" : debt_to_income}

    def eval_(self, node, inputs):
        match node:
            case ast.Constant(value):
                return value  # integer
            case ast.Name(id=name):
                if name in inputs:
                    return inputs[name]
                
                if name in self.functions:
                    print(name)
                    value = self.functions[name](inputs)
                    inputs[name] = value
                    return value
                raise ValueError(f"Unknown variable: {name}")
            case ast.BinOp(left, op, right):
                return operators[type(op)](self.eval_(left, inputs), self.eval_(right, inputs))
            case ast.UnaryOp(op, operand):  # e.g., -1
                return operators[type(op)](self.eval_(operand, inputs))
            case ast.BoolOp(op, values):
                if isinstance(op, ast.And):
                    result = True
                    for v in values:
                        result = result and self.eval_(v, inputs)
                        if not result:
                            break
                    return result
                elif isinstance(op, ast.Or):
                    result = False
                    for v in values:
                        result = result or self.eval_(v, inputs)
                        if result:
                            break
                    return result
                else:
                    raise TypeError(op)
                
            case ast.Compare(left, ops, comparators):       ## for 1st case below there will be multiple ops and comparators i.e., right hand values, but for 2nd case although list but contain single op and right hand value.
                left = self.eval_(left, inputs)
                for op, right in zip(ops, comparators):
                    right = self.eval_(right, inputs)
                    if not operators[type(op)](left, right):   ## for cases like 1 < 2 < 3 if left hand conditions fail no need to check further
                        return False                            ## not for cases like 1 < 2 and 3 < 4 because boolean operator will take care
                    left = right
                return True
            
            case _:
                raise TypeError(node)
    
    def eval_exp(self, exp, inputs):
        return self.eval_(ast.parse(exp, mode='eval').body, inputs)