from mlpy.ml.grammar.parser import MLParser

code = "add = fn(x) => x + 1;"

parser = MLParser()
tree = parser.parse(code, "test.ml")
print("Parsed tree type:", type(tree))
print("Tree items:", len(tree.items))
if tree.items:
    stmt = tree.items[0]
    print("First statement type:", type(stmt))
    if hasattr(stmt, 'value'):
        print("Value type:", type(stmt.value))
        if hasattr(stmt.value, 'parameters'):
            print("Parameters:", stmt.value.parameters)
            for p in stmt.value.parameters:
                print("  Param:", p, "type:", type(p))
                if hasattr(p, 'name'):
                    print("    name attr:", p.name)
                print("    str:", str(p))
