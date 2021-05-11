import sympy
import random

x = sympy.symbols('x')

constants = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
binary_ops = ["+", "-", "*", "/"]
unary_ops = ["exp", "log", "sqrt", "sin", "cos", "tan", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh", "arcsinh", "arccosh", "arctanh"]
op_types = (sympy.core.add.Add, sympy.core.mul.Mul, sympy.exp, sympy.log, sympy.core.power.Pow,
                  sympy.sin, sympy.cos, sympy.tan, sympy.sinh, sympy.cosh, sympy.tanh, sympy.asin, sympy.acos, sympy.atan, 
                  sympy.asinh, sympy.acosh, sympy.atanh)

def generate_terminal():
  """
  Generates terminal node. 
  With 50%, returns x. Otherwise returns constant among -5~5, except 0.
  """
  if random.random() > 0.5:
    return x
  else:
    return sympy.Integer(random.choice(constants))

def generate_unary_tree(op_str, child):
  """
  Given operator string and single child, creates tree. 
  """
  if op_str == "exp":
    return sympy.exp(child)
  elif op_str == "log":
    return sympy.log(child)
  elif op_str == "sqrt":
    return sympy.sqrt(child)
  elif op_str == "sin":
    return sympy.sin(child)
  elif op_str == "cos":
    return sympy.cos(child)
  elif op_str == "tan":
    return sympy.tan(child)
  elif op_str == "arcsin":
    return sympy.asin(child)
  elif op_str == "arccos":
    return sympy.acos(child)
  elif op_str == "arctan":
    return sympy.atan(child)
  elif op_str == "sinh":
    return sympy.sinh(child)
  elif op_str == "cosh":
    return sympy.cosh(child)
  elif op_str == "tanh":
    return sympy.tanh(child)
  elif op_str == "arcsinh":
    return sympy.asinh(child)
  elif op_str == "arccosh":
    return sympy.acosh(child)
  elif op_str == "arctanh":
    return sympy.atanh(child)
  else:
    raise ValueError("Unknown operator {}".format(op_str))

def generate_binary_tree(op_str, first_child, second_child):
  """
  Given operator string and two child, creates tree.
  """
  if op_str == "+":
    return first_child + second_child
  elif op_str == "-":
    return first_child - second_child
  elif op_str == "*":
    return first_child * second_child
  elif op_str == "/":
    return first_child / second_child
  else:
    raise ValueError("Unknown opeartor {}".format(op_str))

def full_init(depth):
  """
  Full initialization.
  Given depth N, returns a tree with every terminal node has given depth. 
  """
  if depth == 1:
    return generate_terminal()
  else:
    if random.random() > 0.5:
      op = random.choice(binary_ops)
      first_tree = full_init(depth - 1)
      second_tree = full_init(depth - 1)
      return generate_binary_tree(op, first_tree, second_tree)
    else:
      op = random.choice(unary_ops)
      child = full_init(depth - 1)
      return generate_unary_tree(op, child)

def grow_init(depth, prob):
  """
  Grow initialization. 
  Given depth and probability, grow the tree.
  At each internal node, with given probability, we instead generate terminal node.
  """
  if depth == 1:
    return generate_terminal()
  else:
    if random.random() < prob:
      return generate_terminal()
    else:
      if random.random() > 0.5:
        op = random.choice(binary_ops)
        first_tree = grow_init(depth - 1, prob)
        second_tree = grow_init(depth - 1, prob)
        return generate_binary_tree(op, first_tree, second_tree)
      else:
        op = random.choice(unary_ops)
        child = grow_init(depth - 1, prob)
        return generate_unary_tree(op, child)

def fixed_init(n):
  """
  Creates tree having internal nodes of given number.

  Internally, it randomly splits remaining number of nodes to half if we have binary operation,
  otherwise subtract one.
  """
  if n == 0:
    return generate_terminal()
  else:
    if random.random() > 0.5:
      op = random.choice(bianry_ops)
      left_n = random.randint(n - 1)
      right_n = n - 1 - left_n
      left_tree = fixed_init(left_n)
      right_tree = fixed_init(right_n)
      return generate_binary_tree(op, left_tree, right_tree)
    else:
      op = random.choice(unary_ops)
      child = fixed_init(n - 1)
      return generate_unary_tree(op, child)

def is_safe_op(formula):
  """
  This is helper function for deciding whether given formulas root has safe operator.
  If it is not valid, it means we can't encode given formula in network.
  """
  return isinstance(formula, op_types)

def is_integral_valid(formula):
  """
  Recursively iterates given formula, and check if it is valid integration formula.
  """
  if isinstance(formula, sympy.integrals.integrals.Integral):
    return False
  else:
    if not is_safe_op(formula):
      return False
    else:
      for arg in formula.args:
        if not is_integral_valid(arg):
          return False
      return True


if __name__ == "__main__":
  for i in range(10):
    form = full_init(7)
    print(form)
    print(form.diff(x))
    integ = sympy.integrate(form, x)
    if is_integral_valid(integ):
      print(integ)
    else:
      print("Not valid integration")