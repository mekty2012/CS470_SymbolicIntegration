import symbolic
import generator
import tree
import sympy
import pytest

def test_code():
  orig = symbolic.fixed_init(15)
  encoded = tree.tree_to_list(orig)
  decoded, rest = tree.list_to_tree(encoded)
  print(orig)
  print(sympy.srepr(orig))
  print(encoded)
  print(decoded)
  assert len(rest) == 0
  assert tree.tree_to_list(orig) == tree.tree_to_list(decoded)
