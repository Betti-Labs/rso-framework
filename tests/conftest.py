"""
Pytest configuration for RSO framework tests.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Ensure all imports work
try:
    from xi import XiOscillator, XiSymbolic, xi_operator
    print("✓ RSO modules imported successfully in conftest.py")
except ImportError as e:
    print(f"✗ Import error in conftest.py: {e}")
    raise