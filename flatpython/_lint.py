import ast
import logging

logger = logging.getLogger(__name__)


class ComplexPython(RuntimeError):
    def __init__(self, msg: str):
        super().__init__()
        self.msg = msg


def lint(code: str) -> bool:
    tree = ast.parse(code)

    def unsupported(value: ast.AST, message: str) -> None:
        body = ast.get_source_segment(code, value)
        if body is None:
            body = ast.dump(value)
        raise ComplexPython(f"{message}:\n{body}")

    class Linter(ast.NodeVisitor):
        def __init__(self, nested: bool, node: ast.AST):
            self.nested = nested
            self.node = node

        def _nested_ast(self, node: ast.AST):
            if self.nested:
                unsupported(self.node, "program contains nested control flow")
            for child in ast.iter_child_nodes(node):
                Linter(nested=True, node=node).visit(child)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._nested_ast(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._nested_ast(node)

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            for stmt in node.body:
                if isinstance(stmt, ast.FunctionDef) or \
                        isinstance(stmt, ast.AsyncFunctionDef):
                    unsupported(node, "class has methods")

        def visit_For(self, node: ast.For) -> None:
            self._nested_ast(node)

        def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
            self._nested_ast(node)

        def visit_While(self, node: ast.While) -> None:
            self._nested_ast(node)

        def visit_If(self, node: ast.If) -> None:
            self._nested_ast(node)

        def visit_Lambda(self, node: ast.Lambda) -> None:
            self._nested_ast(node)

        def visit_IfExp(self, node: ast.IfExp) -> None:
            self._nested_ast(node)

        def visit_ListComp(self, node: ast.ListComp) -> None:
            self._nested_ast(node)

        def visit_SetComp(self, node: ast.SetComp) -> None:
            self._nested_ast(node)

        def visit_DictComp(self, node: ast.DictComp) -> None:
            self._nested_ast(node)

        def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
            self._nested_ast(node)

    try:
        Linter(nested=False, node=tree).visit(tree)
    except ComplexPython as e:
        logger.info(e.msg)
        return False
    return True
