"""
Symbolic and numeric utilities for exploring the Recursive Superpositional
Ontology (RSO) framework.  This module defines classes and functions to
construct Xi attractors, iterate them as discrete oscillators, and
generate symbolic structures using SymPy.  The goal of this code is not
to perform any kind of numerical integration, but rather to provide
minimal models that illustrate the behaviour of the ⊕ operator and the
resulting contradiction fields.

Classes
-------
XiOscillator
    A discrete oscillator that toggles between a predicate and its negation.
XiSymbolic
    A symbolic representation of a predicate and its negation using SymPy.

Functions
---------
xi_operator(x, depth=2)
    Construct a finite approximation to a Xi attractor by recursively
    applying the ⊕ operator to a predicate and its negation.

Exceptions
----------
RSORuntimeError
    Base exception for RSO framework runtime errors.
InvalidPredicateError
    Raised when predicate names are invalid.
DepthLimitError
    Raised when recursion depth exceeds safe limits.

These tools are used in the accompanying notebook and can be extended
further for experimentation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Iterable, Optional

from sympy import symbols, Not, And, Or, simplify
from sympy.core.symbol import Symbol


class RSORuntimeError(Exception):
    """Base exception for RSO framework runtime errors."""
    pass


class InvalidPredicateError(RSORuntimeError):
    """Raised when predicate names are invalid."""
    pass


class DepthLimitError(RSORuntimeError):
    """Raised when recursion depth exceeds safe limits."""
    pass


@dataclass
class XiOscillator:
    """A simple discrete oscillator representing Ξ(x).

    The oscillator alternates deterministically between a predicate being
    "active" (True) and its negation (False).  This captures the core
    intuition behind the RSO: a property never stabilises at a single
    truth value but recursively flips back and forth.

    Parameters
    ----------
    initial : bool
        The starting boolean state of the predicate (True for x, False for ¬x).
    
    Raises
    ------
    TypeError
        If initial is not a boolean value.
    """

    initial: bool

    def __post_init__(self):
        """Validate initialization parameters."""
        if not isinstance(self.initial, bool):
            raise TypeError(f"initial must be bool, got {type(self.initial).__name__}")

    def iterate(self, steps: int) -> List[bool]:
        """Generate a sequence of boolean states for a given number of steps.

        Parameters
        ----------
        steps : int
            Number of iterations to perform. Must be non-negative.

        Returns
        -------
        List[bool]
            A list containing the state at each iteration.  ``True``
            corresponds to the predicate x being active; ``False``
            corresponds to ¬x.
        
        Raises
        ------
        ValueError
            If steps is negative.
        TypeError
            If steps is not an integer.
        """
        if not isinstance(steps, int):
            raise TypeError(f"steps must be int, got {type(steps).__name__}")
        if steps < 0:
            raise ValueError(f"steps must be non-negative, got {steps}")
        
        history: List[bool] = []
        current = self.initial
        for _ in range(steps):
            history.append(current)
            current = not current  # flip state
        return history
    
    def get_period(self) -> int:
        """Get the period of the oscillation.
        
        Returns
        -------
        int
            The period of oscillation (always 2 for basic oscillator).
        """
        return 2
    
    def is_stable(self, steps: int = 10) -> bool:
        """Check if the oscillation is stable over given steps.
        
        Parameters
        ----------
        steps : int, optional
            Number of steps to check for stability.
            
        Returns
        -------
        bool
            True if oscillation maintains expected period.
        """
        if steps < 4:
            steps = 4  # Need at least 2 full periods
            
        sequence = self.iterate(steps)
        period = self.get_period()
        
        # Check if sequence repeats with expected period
        for i in range(period, len(sequence)):
            if sequence[i] != sequence[i - period]:
                return False
        return True


@dataclass
class XiSymbolic:
    """A symbolic representation of a predicate and its negation.

    This class utilises SymPy to construct formulae involving a
    predicate ``x`` and its negation ``¬x``.  The ``xi_operator``
    function uses these objects to build finite approximations to the
    contradiction field Ξ(x).

    Parameters
    ----------
    name : str
        Name of the predicate symbol.  Must be a valid Python identifier.
    
    Raises
    ------
    InvalidPredicateError
        If name is not a valid identifier or is reserved.
    TypeError
        If name is not a string.
    """

    name: str

    def __post_init__(self) -> None:
        """Validate and initialize the symbolic predicate."""
        if not isinstance(self.name, str):
            raise TypeError(f"name must be str, got {type(self.name).__name__}")
        
        if not self.name:
            raise InvalidPredicateError("Predicate name cannot be empty")
        
        if not self._is_valid_identifier(self.name):
            raise InvalidPredicateError(f"'{self.name}' is not a valid Python identifier")
        
        if self._is_reserved_name(self.name):
            raise InvalidPredicateError(f"'{self.name}' is a reserved name")
        
        try:
            self.symbol = symbols(self.name)
            self.negation = Not(self.symbol)
        except Exception as e:
            raise InvalidPredicateError(f"Failed to create symbol '{self.name}': {e}")

    def _is_valid_identifier(self, name: str) -> bool:
        """Check if name is a valid Python identifier."""
        return name.isidentifier()
    
    def _is_reserved_name(self, name: str) -> bool:
        """Check if name is a reserved keyword or common symbol."""
        reserved = {
            'True', 'False', 'None', 'and', 'or', 'not', 'if', 'else', 'elif',
            'for', 'while', 'def', 'class', 'return', 'yield', 'import', 'from',
            'as', 'try', 'except', 'finally', 'with', 'lambda', 'global', 'nonlocal'
        }
        return name in reserved

    def base_set(self) -> List[Symbol]:
        """Return the basic set {x, ¬x}.
        
        Returns
        -------
        List[Symbol]
            List containing the symbol and its negation.
        """
        return [self.symbol, self.negation]
    
    def get_contradiction(self) -> And:
        """Get the contradiction x ∧ ¬x.
        
        Returns
        -------
        And
            The contradiction formula.
        """
        return And(self.symbol, self.negation)
    
    def get_tautology(self) -> Or:
        """Get the tautology x ∨ ¬x.
        
        Returns
        -------
        Or
            The tautology formula.
        """
        return Or(self.symbol, self.negation)


def xi_operator(predicate: XiSymbolic, depth: int = 2, max_depth: int = 10) -> List:
    """Construct a finite approximation to Ξ(x).

    The ⊕ operator conceptually produces an infinite recursion of
    contradictions between a predicate and its negation.  This
    function constructs a finite set of symbolic expressions up to a
    given recursion depth by repeatedly combining the predicate,
    its negation, and prior results using logical conjunction and
    disjunction.

    Parameters
    ----------
    predicate : XiSymbolic
        The symbolic predicate whose contradiction field is built.
    depth : int, optional
        The recursion depth.  A value of 0 yields just {x, ¬x};
        larger values produce combinations.
    max_depth : int, optional
        Maximum allowed depth to prevent excessive computation.

    Returns
    -------
    List
        A list of SymPy logical expressions approximating Ξ(x).
    
    Raises
    ------
    TypeError
        If predicate is not XiSymbolic or depth is not int.
    ValueError
        If depth is negative.
    DepthLimitError
        If depth exceeds max_depth.
    """
    if not isinstance(predicate, XiSymbolic):
        raise TypeError(f"predicate must be XiSymbolic, got {type(predicate).__name__}")
    
    if not isinstance(depth, int):
        raise TypeError(f"depth must be int, got {type(depth).__name__}")
    
    if depth < 0:
        raise ValueError(f"depth must be non-negative, got {depth}")
    
    if depth > max_depth:
        raise DepthLimitError(f"depth {depth} exceeds maximum allowed depth {max_depth}")
    
    base = predicate.base_set()
    results: List = list(base)
    
    if depth == 0:
        return results
    
    previous_level = list(base)
    
    for level in range(depth):
        new_level: List = []
        
        # Combine each pair of expressions with conjunction and disjunction
        for a in previous_level:
            for b in base:
                try:
                    and_expr = And(a, b)
                    or_expr = Or(a, b)
                    
                    # Simplify expressions to avoid redundancy
                    and_simplified = simplify(and_expr)
                    or_simplified = simplify(or_expr)
                    
                    new_level.extend([and_simplified, or_simplified])
                    
                except Exception as e:
                    # Log warning but continue processing
                    print(f"Warning: Failed to process expressions at level {level}: {e}")
                    continue
        
        # Add only unique expressions (by string representation)
        existing_strs = {str(simplify(expr)) for expr in results}
        for expr in new_level:
            expr_str = str(simplify(expr))
            if expr_str not in existing_strs:
                results.append(expr)
                existing_strs.add(expr_str)
        
        previous_level = new_level
        
        # Safety check: if no new expressions generated, break early
        if not new_level:
            break
    
    return results


def validate_xi_attractor(attractor: List, predicate: XiSymbolic) -> dict:
    """Validate properties of a Ξ attractor.
    
    Parameters
    ----------
    attractor : List
        The attractor to validate.
    predicate : XiSymbolic
        The original predicate.
        
    Returns
    -------
    dict
        Validation results including checks for contradiction preservation,
        tautology presence, and structural properties.
    """
    if not isinstance(attractor, list):
        raise TypeError("attractor must be a list")
    
    if not isinstance(predicate, XiSymbolic):
        raise TypeError("predicate must be XiSymbolic")
    
    results = {
        'total_expressions': len(attractor),
        'contains_contradiction': False,
        'contains_tautology': False,
        'contains_base_predicate': False,
        'contains_base_negation': False,
        'unique_simplified': 0,
        'validation_passed': False
    }
    
    try:
        # Check for base elements
        base_set = predicate.base_set()
        contradiction = predicate.get_contradiction()
        tautology = predicate.get_tautology()
        
        simplified_attractor = [str(simplify(expr)) for expr in attractor]
        results['unique_simplified'] = len(set(simplified_attractor))
        
        # Check presence of key elements
        for expr in attractor:
            simplified = simplify(expr)
            if simplified == base_set[0]:  # predicate
                results['contains_base_predicate'] = True
            elif simplified == base_set[1]:  # negation
                results['contains_base_negation'] = True
            elif str(simplified) == str(simplify(contradiction)):
                results['contains_contradiction'] = True
            elif str(simplified) == str(simplify(tautology)):
                results['contains_tautology'] = True
        
        # Overall validation
        results['validation_passed'] = (
            results['contains_base_predicate'] and
            results['contains_base_negation'] and
            results['total_expressions'] > 0
        )
        
    except Exception as e:
        results['error'] = str(e)
        results['validation_passed'] = False
    
    return results


__all__ = [
    "XiOscillator", 
    "XiSymbolic", 
    "xi_operator", 
    "validate_xi_attractor",
    "RSORuntimeError",
    "InvalidPredicateError", 
    "DepthLimitError"
]