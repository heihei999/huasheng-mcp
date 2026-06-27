"""Smoke test core for xingce-solver MCP server."""
import sys
import os

def test_import():
    """Test that the main module can be imported."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from xingce_solver.mcp_server import create_server
    print("OK: MCP server module imported successfully")

def test_scaffold():
    """Test that graphic reasoning scaffold loads."""
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from xingce_solver.scaffolds.graphic_reasoning_scaffold import build_graphic_reasoning_scaffold
    s = build_graphic_reasoning_scaffold()
    assert s['module'] == 'graphic_reasoning'
    assert s['version'] == 'v0.2.2'
    print(f"OK: graphic_reasoning_scaffold {s['version']} loaded")

if __name__ == '__main__':
    test_import()
    test_scaffold()
    print("All smoke tests passed")
