"""
Test suite for quantum mechanics bridge in RSO framework.
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from quantum_bridge import QuantumXiState, QuantumXiPair, demonstrate_quantum_rso_correspondence


class TestQuantumXiState:
    """Test quantum Ξ state functionality."""
    
    def test_initialization(self):
        """Test quantum state initialization and normalization."""
        # Test default initialization (equal superposition)
        state = QuantumXiState()
        assert abs(abs(state.alpha)**2 + abs(state.beta)**2 - 1.0) < 1e-10
        
        # Test custom initialization
        state = QuantumXiState(alpha=0.6, beta=0.8)
        assert abs(abs(state.alpha)**2 + abs(state.beta)**2 - 1.0) < 1e-10
    
    def test_probability_calculation(self):
        """Test probability calculations."""
        state = QuantumXiState(alpha=0.6, beta=0.8)
        
        prob_x = state.probability_x()
        prob_not_x = state.probability_not_x()
        
        assert 0.0 <= prob_x <= 1.0
        assert 0.0 <= prob_not_x <= 1.0
        assert abs(prob_x + prob_not_x - 1.0) < 1e-10
    
    def test_time_evolution(self):
        """Test quantum time evolution."""
        initial_state = QuantumXiState()
        evolved_state = initial_state.evolve(time=np.pi, frequency=1.0)
        
        # After π time with frequency 1, should have phase shift
        assert evolved_state.probability_x() >= 0.0
        assert evolved_state.probability_not_x() >= 0.0
        
        # Probability conservation
        total_prob = evolved_state.probability_x() + evolved_state.probability_not_x()
        assert abs(total_prob - 1.0) < 1e-10
    
    def test_measurement(self):
        """Test quantum measurement process."""
        state = QuantumXiState()
        
        # Run multiple measurements to test statistical behavior
        measurements = [state.measure() for _ in range(1000)]
        true_ratio = sum(measurements) / len(measurements)
        
        # For equal superposition, should be approximately 50/50
        assert 0.4 < true_ratio < 0.6  # Allow for statistical variation


class TestQuantumXiPair:
    """Test entangled quantum pair functionality."""
    
    def test_entanglement_creation(self):
        """Test creation of entangled quantum pairs."""
        state1 = QuantumXiState(alpha=0.6, beta=0.8)
        state2 = QuantumXiState(alpha=0.8, beta=0.6)
        
        pair = state1.entangle_with(state2)
        
        assert isinstance(pair, QuantumXiPair)
        assert pair.state1 == state1
        assert pair.state2 == state2
    
    def test_joint_measurement(self):
        """Test joint measurement of entangled pairs."""
        state1 = QuantumXiState()
        state2 = QuantumXiState()
        pair = state1.entangle_with(state2)
        
        # Run multiple joint measurements
        measurements = [pair.measure_both() for _ in range(100)]
        
        # Each measurement should return a tuple of two booleans
        for measurement in measurements:
            assert isinstance(measurement, tuple)
            assert len(measurement) == 2
            assert isinstance(measurement[0], bool)
            assert isinstance(measurement[1], bool)


class TestQuantumRSOCorrespondence:
    """Test quantum-RSO correspondence demonstration."""
    
    def test_correspondence_demonstration(self):
        """Test that quantum-RSO correspondence runs without errors."""
        results = demonstrate_quantum_rso_correspondence()
        
        assert isinstance(results, dict)
        
        # Check expected result structure
        expected_keys = [
            'quantum_classical_correspondence',
            'measurement_ratio',
            'expected_ratio',
            'correspondence_error'
        ]
        
        for key in expected_keys:
            assert key in results
        
        # Verify result types and ranges
        assert isinstance(results['quantum_classical_correspondence'], bool)
        assert 0.0 <= results['measurement_ratio'] <= 1.0
        assert results['expected_ratio'] == 0.5
        assert results['correspondence_error'] >= 0.0
        
        # For large number of measurements, error should be small
        assert results['correspondence_error'] < 0.1


if __name__ == "__main__":
    pytest.main([__file__])