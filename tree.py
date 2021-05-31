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

def formula_to_tree(formula):
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
    op = type_str_dict[type(formula)]
    res = [op, None, None]
    temp = res
    for i in range(len(formula.args)):
      temp[1] = formula_to_tree(formula.arg[i])
      temp[2] = [op, None, None]
    temp[2] = formula_to_tree(formula.args[-1])
    return res
  elif isinstance(formula, symbolic.op_types):
    curr = [type_str_dict[type(formula)]]
    for arg in formula.args:
      curr = curr + formula_to_tree(arg)
    return curr
  else:
    raise ValueError("This function expects valid formula but is type {}".format(type(formula)))

def tree_preorder(tree):
  if len(tree) == 1:
    return [tree[0]]
  elif len(tree) == 2:
    return [tree[0]] + tree_preorder(tree[1])
  elif len(tree) == 3:
    return [tree[0]] + tree_preorder(tree[1]) + tree_preorder(tree[2])
  else:
    raise ValueError("All trees are at most binary, but it has {} childs".format(len(tree) - 1))

def tree_depth(tree):
  if len(tree) == 1:
    return 1
  elif len(tree) == 2:
    return tree_depth(tree[1]) + 1
  elif len(tree) == 3:
    return max(tree_depth(tree[1]), tree_depth(tree[2])) + 1
  else:
    raise ValueError("All trees are at most binary, but it has {} childs".format(len(tree) - 1))

def empty_tree(depth):
  if depth == 1:
    return [None]
  else:
    return [None, empty_tree(depth - 1), empty_tree(depth - 1)]

def tree_full_binary(tree, depth):
  if depth == 1:
    if len(tree) == 1:
      return [tree[0]]
    else:
      raise ValueError("Maximum depth expected, but the tree is deeper.")
  else:
    if len(tree) == 3:
      return [tree[0], tree_full_binary(tree[1], depth - 1), tree_full_binary(tree[2], depth - 1)]
    elif len(tree) == 2:
      return [tree[0], tree_full_binary(tree[1], depth - 1), empty_tree(depth - 1)]
    elif len(tree) == 1:
      return [tree[0], empty_tree(depth - 1), empty_tree(depth - 1)]
    else:
      raise ValueError("All trees are at most binary, but it has {} childs".format(len(tree) - 1))

def tree_postorder(tree):
  if len(tree) == 1:
    return [tree[0]]
  elif len(tree) == 3:
    return tree_postorder(tree[1]) + tree_postorder(tree[2]) + [tree[0]]
  else:
    raise ValueError("All trees are complete binary, but it has {} childs".format(len(tree) - 1))

def symb_to_sparse(t):
  ind = symbolic.ops.index(t)
  return [1 if i == ind else 0 for i in range(len(symbolic.ops))]

def symb_to_sparse_list(l):
  return [symb_to_sparse(t) for t in l]

def batch_postorder(trees):
  max_depth = -1
  for tree in trees:
    depth = tree_depth(tree)
    if depth > max_depth:
      max_depth = depth
  
  filled = [tree_full_binary(tree, max_depth) for tree in trees]
  postordered = [tree_postorder(tree) for tree in filled]
  sparsed = [symb_to_sparse_list(traverse) for traverse in postordered]
  return sparsed

def batch_preorder(trees):
  preordered = [tree_preorder(tree) for tree in trees]
  max_length = max(map(len, preordered))
  for traverse in preordered:
    traverse.extend([None] * (max_length - len(traverse)))
  sparsed = [symb_to_sparse_list(traverse) for traverse in preordered]
  return sparsed
