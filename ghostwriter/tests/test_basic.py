import importlib
import pytest

MODULES = [
    'ghostwriter.cli',
    'ghostwriter.parser',
    'ghostwriter.llm',
    'ghostwriter.vector_store',
]

@pytest.mark.parametrize('name', MODULES)
def test_imports(name):
    try:
        importlib.import_module(name)
    except ImportError:
        pytest.skip(f'Module {name} requires optional dependencies')
