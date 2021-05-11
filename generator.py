import symbolic
import sympy

def generate_forward():
  """
  Generate dataset with forward method

  It tries to integrate random function.
  The integral may not be symbolically possible, or may contains invalid operators.
  In those cases, it returns None.
  """
  formula = symbolic.fixed_init(15)
  integrated = sympy.integrate(formula, symbolic.x, meijerg=False)
  if symbolic.is_integral_valid(integrated):
    return (formula, integrated)
  else:
    return None

def generate_backward():
  """
  Generate dataset with backward method

  It differentiate random function.
  """
  formula = symbolic.fixed_init(15)
  differentiated = formula.diff(symbolic.x)
  return (differentiated, formula)

def generate_part(dataset):
  """
  Use integration by parts formula

  Given F, G, and their derivative f, g, we have
  \int fG = FG - \int Fg
  So if we knows \int fG or \int Fg, we have the other one.
  """
  first = symbolic.fixed_init(15)
  second = symbolic.fixed_init(15)
  first_d = first.diff(symbolic.x)
  second_d = second.diff(symbolic.x)

  FG = first * second
  fG = first_d * second
  Fg = first * second_d
  if fG in dataset:
    return (Fg, FG - dataset[fG])
  elif Fg in dataset:
    return (fG, FG - dataset[Fg])
  else:
    return None