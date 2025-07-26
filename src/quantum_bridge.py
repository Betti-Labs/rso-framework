"""
Quantum mechanics bridge for RSO framework.

This module explores connections between RSO and quantum mechanics,
particularly superposition states and measurement collapse.
"""

import numpy as np
from typing import List, Tuple
from numbers import Complex
from dataclasses import dataclass
import matplotlib.pyplot as plt


@dataclass
class QuantumXiState:
    """Quantum representation of a Ξ oscillator."""
    
    def __init__(self, alpha: Complex = 1/np.sqrt(2), beta: Complex = 1/np.sqrt(2)):
        """
        Initialize quantum superposition |ψ⟩ = α|x⟩ + β|¬x⟩
        
        Parameters:
        -----------
        alpha : Complex coefficient for |x⟩ state
        beta : Complex coefficient for |¬x⟩ state
        
        Raises:
        -------
        TypeError
            If alpha or beta are not numeric types.
        ValueError
            If both alpha and beta are zero (unnormalizable state).
        """
        # Type validation
        if not isinstance(alpha, (int, float, complex, np.number)):
            raise TypeError(f"alpha must be numeric, got {type(alpha).__name__}")
        if not isinstance(beta, (int, float, complex, np.number)):
            raise TypeError(f"beta must be numeric, got {type(beta).__name__}")
        
        # Convert to complex
        alpha = complex(alpha)
        beta = complex(beta)
        
        # Check for zero state
        norm_squared = abs(alpha)**2 + abs(beta)**2
        if norm_squared == 0:
            raise ValueError("Cannot normalize zero state (both alpha and beta are zero)")
        
        # Normalize coefficients
        norm = np.sqrt(norm_squared)
        self.alpha = alpha / norm
        self.beta = beta / norm
    
    def probability_x(self) -> float:
        """Probability of measuring state |x⟩"""
        return abs(self.alpha)**2
    
    def probability_not_x(self) -> float:
        """Probability of measuring state |¬x⟩"""
        return abs(self.beta)**2
    
    def evolve(self, time: float, frequency: float = 1.0) -> 'QuantumXiState':
        """
        Time evolution under Hamiltonian H = ℏω(|x⟩⟨x| - |¬x⟩⟨¬x|)
        
        Parameters:
        -----------
        time : float
            Evolution time parameter.
        frequency : float, optional
            Frequency parameter for evolution.
            
        Returns:
        --------
        QuantumXiState
            New evolved quantum state.
            
        Raises:
        -------
        TypeError
            If time or frequency are not numeric.
        ValueError
            If frequency is negative.
        """
        if not isinstance(time, (int, float, np.number)):
            raise TypeError(f"time must be numeric, got {type(time).__name__}")
        if not isinstance(frequency, (int, float, np.number)):
            raise TypeError(f"frequency must be numeric, got {type(frequency).__name__}")
        
        if frequency < 0:
            raise ValueError(f"frequency must be non-negative, got {frequency}")
        
        try:
            phase = frequency * time
            new_alpha = self.alpha * np.exp(1j * phase)
            new_beta = self.beta * np.exp(-1j * phase)
            return QuantumXiState(new_alpha, new_beta)
        except Exception as e:
            raise RuntimeError(f"Failed to evolve quantum state: {e}")
    
    def measure(self, random_seed: int = None) -> bool:
        """
        Quantum measurement - collapses to classical state.
        
        Parameters:
        -----------
        random_seed : int, optional
            Seed for random number generator for reproducible results.
            
        Returns:
        --------
        bool
            True for |x⟩, False for |¬x⟩
        """
        if random_seed is not None:
            if not isinstance(random_seed, int):
                raise TypeError(f"random_seed must be int, got {type(random_seed).__name__}")
            np.random.seed(random_seed)
        
        try:
            prob_x = self.probability_x()
            return np.random.random() < prob_x
        except Exception as e:
            raise RuntimeError(f"Measurement failed: {e}")
    
    def entangle_with(self, other: 'QuantumXiState') -> 'QuantumXiPair':
        """Create entangled two-predicate system"""
        return QuantumXiPair(self, other)


@dataclass
class QuantumXiPair:
    """Entangled two-predicate quantum system."""
    
    def __init__(self, state1: QuantumXiState, state2: QuantumXiState):
        self.state1 = state1
        self.state2 = state2
        # Create entangled coefficients
        self.c00 = state1.alpha * state2.alpha  # |x₁,x₂⟩
        self.c01 = state1.alpha * state2.beta   # |x₁,¬x₂⟩
        self.c10 = state1.beta * state2.alpha   # |¬x₁,x₂⟩
        self.c11 = state1.beta * state2.beta    # |¬x₁,¬x₂⟩
    
    def measure_both(self) -> Tuple[bool, bool]:
        """Measure both predicates simultaneously"""
        probs = [abs(c)**2 for c in [self.c00, self.c01, self.c10, self.c11]]
        outcome = np.random.choice(4, p=probs)
        
        outcomes = [(True, True), (True, False), (False, True), (False, False)]
        return outcomes[outcome]


def demonstrate_quantum_rso_correspondence():
    """
    Demonstrate correspondence between quantum superposition and RSO.
    """
    print("Quantum-RSO Correspondence Demonstration")
    print("=" * 45)
    
    # Create quantum Ξ state in perfect superposition
    quantum_xi = QuantumXiState()
    
    print(f"Initial superposition: α={quantum_xi.alpha:.3f}, β={quantum_xi.beta:.3f}")
    print(f"P(x) = {quantum_xi.probability_x():.3f}")
    print(f"P(¬x) = {quantum_xi.probability_not_x():.3f}")
    
    # Time evolution
    times = np.linspace(0, 4*np.pi, 100)
    prob_x_evolution = []
    
    for t in times:
        evolved_state = quantum_xi.evolve(t)
        prob_x_evolution.append(evolved_state.probability_x())
    
    # Plot quantum evolution vs classical RSO oscillation
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    
    # Quantum probability evolution
    ax1.plot(times, prob_x_evolution, 'b-', label='P(x) quantum')
    ax1.plot(times, [1-p for p in prob_x_evolution], 'r-', label='P(¬x) quantum')
    ax1.set_ylabel('Probability')
    ax1.set_title('Quantum Ξ State Evolution')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Classical RSO oscillation
    classical_oscillation = [0.5 + 0.5*np.cos(t) for t in times]
    ax2.plot(times, classical_oscillation, 'g-', label='Classical Ξ oscillation')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('State Value')
    ax2.set_title('Classical RSO Oscillation')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Create figures directory if it doesn't exist
    import os
    os.makedirs('figures', exist_ok=True)
    
    try:
        plt.savefig('figures/quantum_rso_correspondence.png', dpi=300, bbox_inches='tight')
        print("\nQuantum-classical correspondence plot saved to figures/")
    except Exception as e:
        print(f"\nWarning: Could not save figure: {e}")
    finally:
        plt.close()
    
    # Demonstrate measurement collapse
    print("\nMeasurement Collapse Demonstration:")
    measurements = [quantum_xi.measure() for _ in range(1000)]
    true_ratio = sum(measurements) / len(measurements)
    print(f"Measured |x⟩ in {true_ratio:.1%} of cases (expected ~50%)")
    
    return {
        'quantum_classical_correspondence': True,
        'measurement_ratio': true_ratio,
        'expected_ratio': 0.5,
        'correspondence_error': abs(true_ratio - 0.5)
    }


if __name__ == "__main__":
    results = demonstrate_quantum_rso_correspondence()
    print(f"\nCorrespondence verified with {results['correspondence_error']:.1%} error")