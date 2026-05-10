import ast

class DeadCodeDetector(ast.NodeVisitor):
    def __init__(self):
        self.functions = set()
        self.calls = set()

    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        self.generic_visit(node)

    def visit_If(self, node):
        # détecter if False
        if isinstance(node.test, ast.Constant) and node.test.value == False:
            print(" Condition toujours fausse détectée (code inutile)")
        self.generic_visit(node)


def detect_dead_code(filename):
    print("\n==============================")
    print(f"Analyse du fichier : {filename}")
    print("==============================")

    with open(filename, "r") as f:
        tree = ast.parse(f.read())

    detector = DeadCodeDetector()
    detector.visit(tree)

    unused_functions = detector.functions - detector.calls

    if unused_functions:
        print(" Fonctions inutilisées détectées :", unused_functions)
        print("Nombre de fonctions inutilisées :", len(unused_functions))
    else:
        print(" Aucune fonction inutile détectée")


detect_dead_code("test1.py")
detect_dead_code("test2.py")
detect_dead_code("test3.py")

