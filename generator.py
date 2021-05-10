import symbolic
import sympy

def generate_forward():
  formula = symbolic.fixed_init(15)
  integrated = sympy.integrate(formula, symbolic.x, meijerg=False)
  if symbolic.is_integral_valid(integrated):
    return (formula, integrated)
  else:
    return None

def generate_backward():
  formula = symbolic.fixed_init(15)
  differentiated = formula.diff(symbolic.x)
  return (differentiated, formula)

def generate_part(dataset):
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