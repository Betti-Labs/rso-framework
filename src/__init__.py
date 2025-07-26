"""
RSO Framework - Recursive Superpositional Ontology

A computational framework for contradiction-preserving logic and reality modeling.
"""

__version__ = "1.0.1"
__author__ = "Gregory Betti"
# __email__ = "[email will be added when available]"

try:
    from .xi import XiOscillator, XiSymbolic, xi_operator, validate_xi_attractor
    from .xi import RSORuntimeError, InvalidPredicateError, DepthLimitError
    
    __all__ = [
        "XiOscillator",
        "XiSymbolic", 
        "xi_operator",
        "validate_xi_attractor",
        "RSORuntimeError",
        "InvalidPredicateError",
        "DepthLimitError"
    ]
except ImportError as e:
    # Graceful fallback if imports fail
    print(f"Warning: Could not import RSO components: {e}")
    __all__ = []