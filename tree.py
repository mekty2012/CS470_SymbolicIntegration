import sympy
import symbolic
import re

int_set = {"-5", "-4", "-3", "-2", "-1", "0", "1", "2", "3", "4", "5"}
int_regex = re.compile("^[-+]?[0-9]+$")

type_str_dict = {
  sympy.core.add.Add : "+", 
  sympy.core.mul.Mul : "*",
  sympy.core.power.Pow : "**",
  sympy.exp : "exp", 
  sympy.log : "log", 
  sympy.core.power.Pow : "**",
  sympy.sin : "sin", 
  sympy.cos : "cos", 
  sympy.tan : "tan", 
  sympy.sinh : "sinh", 
  sympy.cosh : "cosh", 
  sympy.tanh : "tanh", 
  sympy.asin : "asin", 
  sympy.acos : "acos", 
  sympy.atan : "atan", 
  sympy.asinh : "asinh", 
  sympy.acosh : "acosh", 
  sympy.atanh : "atanh"
}

def tree_to_list(formula):
  if isinstance(formula, sympy.core.numbers.Integer):
    return [str(formula)]
  elif isinstance(formula, sympy.core.numbers.Rational):
    return ["/", str(formula.p), str(formula.q)]
  elif isinstance(formula, sympy.core.numbers.Pi):
    return ["acos", "-1"]
  elif isinstance(formula, sympy.core.numbers.Exp1):
    return ["exp", "1"]
  elif isinstance(formula, sympy.core.numbers.ImaginaryUnit):
    return ["sqrt", "-1"]
  elif isinstance(formula, sympy.core.symbol.Symbol):
    return [str(formula)]
  elif isinstance(formula, symbolic.op_mult_types):
    res = []
    for i in range(len(formula.args)):
      res.append(type_str_dict[type(formula)])
      res = res + tree_to_list(formula.args[i])
    res = res + tree_to_list(formula.args[-1])
    return res
  elif isinstance(formula, symbolic.op_types):
    curr = [type_str_dict[type(formula)]]
    for arg in formula.args:
      curr = curr + tree_to_list(arg)
    return curr
  else:
    raise ValueError("This function expects valid formula but is type {}".format(type(formula)))

def list_to_tree(words):
  first = words[0]
  if first == "x":
    return symbolic.x, words[1:]
  #elif first in int_set:
  elif int_regex.match(first):
    return int(first), words[1:]
  elif first in symbolic.unary_ops:
    child, rest = list_to_tree(words[1:])
    return symbolic.generate_unary_tree(first, child), rest
  elif first in symbolic.binary_ops or first == "**":
    child1, rest1 = list_to_tree(words[1:])
    child2, rest2 = list_to_tree(rest1)
    return symbolic.generate_binary_tree(first, child1, child2), rest2
  else:
    raise ValueError("This function expects valid formula but first is {}".format(first))