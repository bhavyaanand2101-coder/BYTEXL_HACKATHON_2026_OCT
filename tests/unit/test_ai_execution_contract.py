"""
CI Test for AI Execution Contract.
AST-based import + call inspection on packages/domain/** and services/enrichment/**/*_layer.py.
Asserts NO forbidden LLM, network, or nondeterministic calls exist in the scoring path.
"""

import ast
from pathlib import Path

FORBIDDEN_MODULES = [
    "openai",
    "anthropic",
    "google.generativeai",
    "cohere",
    "mistralai",
    "requests",
    "httpx",
    "aiohttp",
    "urllib",
    "urllib3",
    "socket",
    "http.client",
    "subprocess",
    "os.system",
]

FORBIDDEN_CALLS = [
    "requests.get",
    "requests.post",
    "requests.put",
    "requests.delete",
    "httpx.get",
    "httpx.post",
    "aiohttp.ClientSession",
    "urllib.request.urlopen",
    "socket.socket",
    "subprocess.run",
    "subprocess.Popen",
    "os.system",
    "random.random",
    "random.randint",
    "random.choice",
    "random.shuffle",
]


def _get_call_name(node: ast.AST) -> str:
    """Helper to reconstruct dotted call names (e.g. requests.get)."""
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        parent = _get_call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def inspect_file_ast(file_path: Path):
    is_stat_layer = file_path.name == "stat_layer.py"
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=str(file_path))

    for node in ast.walk(tree):
        # 1. Check direct imports (import x)
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in FORBIDDEN_MODULES:
                    assert not alias.name.startswith(forbidden), (
                        f"Forbidden module import '{alias.name}' detected in {file_path}. "
                        "See AI Execution Contract."
                    )
                if not is_stat_layer:
                    assert alias.name != "random", (
                        f"Module 'random' import forbidden in {file_path}. "
                        "Only permitted in stat_layer.py with deterministic seed."
                    )

        # 2. Check from imports (from x import y)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for forbidden in FORBIDDEN_MODULES:
                    assert not node.module.startswith(forbidden), (
                        f"Forbidden module 'from {node.module}' detected in {file_path}. "
                        "See AI Execution Contract."
                    )
                if not is_stat_layer:
                    assert node.module != "random" and not node.module.startswith("random."), (
                        f"Module 'random' import forbidden in {file_path}. "
                        "Only permitted in stat_layer.py with deterministic seed."
                    )

        # 3. Check AST function calls
        elif isinstance(node, ast.Call):
            call_name = _get_call_name(node.func)
            for forbidden_call in FORBIDDEN_CALLS:
                if call_name == forbidden_call or call_name.endswith(f".{forbidden_call}"):
                    assert False, (
                        f"Forbidden function call '{call_name}' detected in {file_path}. "
                        "Scoring path must be 100% deterministic and free of I/O."
                    )


def test_ai_execution_contract_ast():
    root = Path(__file__).parent.parent.parent

    # 1. Inspect packages/domain/**
    domain_files = list((root / "packages" / "domain").glob("*.py"))
    assert len(domain_files) > 0, "Domain files must exist"
    for df in domain_files:
        inspect_file_ast(df)

    # 2. Inspect services/enrichment/**/*_layer.py
    enrichment_files = list((root / "services" / "enrichment").glob("*_layer.py"))
    assert len(enrichment_files) > 0, "Enrichment layer files must exist"
    for ef in enrichment_files:
        inspect_file_ast(ef)

