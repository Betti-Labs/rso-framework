#!/usr/bin/env python3
"""
Basic test script to verify RSO framework functionality.
This can be run independently to check if everything works.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all core modules can be imported."""
    print("Testing imports...")
    
    try:
        from xi import XiOscillator, XiSymbolic, xi_operator
        print("+ Core imports successful")
        return True
    except Exception as e:
        print(f"- Import failed: {e}")
        return False

def test_oscillator():
    """Test basic oscillator functionality."""
    print("Testing oscillator...")
    
    try:
        from xi import XiOscillator
        
        osc = XiOscillator(True)
        result = osc.iterate(4)
        expected = [True, False, True, False]
        
        if result == expected:
            print(f"+ Oscillator works: {result}")
            return True
        else:
            print(f"- Oscillator failed: got {result}, expected {expected}")
            return False
    except Exception as e:
        print(f"- Oscillator test failed: {e}")
        return False

def test_symbolic():
    """Test symbolic functionality."""
    print("Testing symbolic operations...")
    
    try:
        from xi import XiSymbolic, xi_operator
        
        pred = XiSymbolic('Test')
        result = xi_operator(pred, 1)
        
        if len(result) >= 2:  # Should have at least base set
            print(f"+ Symbolic operations work: generated {len(result)} expressions")
            return True
        else:
            print(f"- Symbolic test failed: only {len(result)} expressions generated")
            return False
    except Exception as e:
        print(f"- Symbolic test failed: {e}")
        return False

def test_formal_proofs():
    """Test formal verification."""
    print("Testing formal verification...")
    
    try:
        from formal_proofs import run_formal_verification
        
        results = run_formal_verification()
        
        if isinstance(results, dict) and len(results) > 0:
            print("+ Formal verification works")
            return True
        else:
            print("- Formal verification failed")
            return False
    except Exception as e:
        print(f"- Formal verification test failed: {e}")
        return False

def main():
    """Run all basic tests."""
    print("RSO Framework Basic Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_oscillator,
        test_symbolic,
        test_formal_proofs,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"- Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! RSO framework is working correctly.")
        return 0
    else:
        print("WARNING: Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())