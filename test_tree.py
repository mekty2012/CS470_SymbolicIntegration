import symbolic
import generator
import tree
import sympy
import pytest

def test_code():
  for i in range(10):
    orig = symbolic.fixed_init(15)
    encoded = tree.tree_to_list(orig)
    decoded, rest = tree.list_to_tree(encoded)
    print(orig)
    print(sympy.srepr(orig))
    print(encoded)
    print(decoded)
    assert len(rest) == 0
    assert sympy.simplify(orig - decoded, rational=True) == sympy.simplify(0)
