"""
Comprehensive test suite for core RSO xi module functionality.
"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from xi import (
    XiOscillator, XiSymbolic, xi_operator, validate_xi_attractor,
    RSORuntimeError, InvalidPredicateError, DepthLimitError
)


class TestXiOscillator:
    """Test XiOscillator with comprehensive error handling."""
    
    def test_valid_initialization(self):
        """Test valid oscillator initialization."""
        osc_true = XiOscillator(True)
        osc_false = XiOscillator(False)
        
        assert osc_true.initial == True
        assert osc_false.initial == False
    
    def test_invalid_initialization(self):
        """Test invalid oscillator initialization."""
        with pytest.raises(TypeError):
            XiOscillator("not_bool")
        
        with pytest.raises(TypeError):
            XiOscillator(1)
        
        with pytest.raises(TypeError):
            XiOscillator(None)
    
    def test_valid_iteration(self):
        """Test valid iteration scenarios."""
        osc = XiOscillator(True)
        
        # Test zero steps
        result = osc.iterate(0)
        assert result == []
        
        # Test single step
        result = osc.iterate(1)
        assert result == [True]
        
        # Test multiple steps
        result = osc.iterate(4)
        assert result == [True, False, True, False]
    
    def test_invalid_iteration(self):
        """Test invalid iteration parameters."""
        osc = XiOscillator(True)
        
        with pytest.raises(TypeError):
            osc.iterate("not_int")
        
        with pytest.raises(TypeError):
            osc.iterate(3.14)
        
        with pytest.raises(ValueError):
            osc.iterate(-1)
    
    def test_period_and_stability(self):
        """Test period calculation and stability checking."""
        osc = XiOscillator(True)
        
        assert osc.get_period() == 2
        assert osc.is_stable(10) == True
        assert osc.is_stable(2) == True  # Minimum steps adjusted internally


class TestXiSymbolic:
    """Test XiSymbolic with comprehensive validation."""
    
    def test_valid_predicates(self):
        """Test valid predicate names."""
        valid_names = ['x', 'P', 'predicate', 'test_var', 'X1', 'var_name']
        
        for name in valid_names:
            pred = XiSymbolic(name)
            assert pred.name == name
            assert pred.symbol.name == name
            assert len(pred.base_set()) == 2
    
    def test_invalid_predicate_types(self):
        """Test invalid predicate types."""
        with pytest.raises(TypeError):
            XiSymbolic(123)
        
        with pytest.raises(TypeError):
            XiSymbolic(None)
        
        with pytest.raises(TypeError):
            XiSymbolic(['not', 'string'])
    
    def test_invalid_predicate_names(self):
        """Test invalid predicate names."""
        invalid_names = [
            '',  # empty
            '123',  # starts with number
            'if',  # reserved keyword
            'True',  # reserved
            'not',  # reserved
            'x-y',  # invalid character
            'x y',  # space
        ]
        
        for name in invalid_names:
            with pytest.raises(InvalidPredicateError):
                XiSymbolic(name)
    
    def test_symbolic_operations(self):
        """Test symbolic operations."""
        pred = XiSymbolic('X')
        
        base_set = pred.base_set()
        assert len(base_set) == 2
        
        contradiction = pred.get_contradiction()
        tautology = pred.get_tautology()
        
        # These should be different expressions
        assert str(contradiction) != str(tautology)


class TestXiOperator:
    """Test xi_operator with comprehensive error handling."""
    
    def test_valid_operations(self):
        """Test valid xi_operator calls."""
        pred = XiSymbolic('X')
        
        # Test different depths
        for depth in range(5):
            result = xi_operator(pred, depth)
            assert isinstance(result, list)
            assert len(result) >= 2  # At least base set
    
    def test_invalid_predicate_type(self):
        """Test invalid predicate type."""
        with pytest.raises(TypeError):
            xi_operator("not_symbolic", 2)
        
        with pytest.raises(TypeError):
            xi_operator(None, 2)
    
    def test_invalid_depth_type(self):
        """Test invalid depth type."""
        pred = XiSymbolic('X')
        
        with pytest.raises(TypeError):
            xi_operator(pred, "not_int")
        
        with pytest.raises(TypeError):
            xi_operator(pred, 3.14)
    
    def test_invalid_depth_value(self):
        """Test invalid depth values."""
        pred = XiSymbolic('X')
        
        with pytest.raises(ValueError):
            xi_operator(pred, -1)
    
    def test_depth_limit(self):
        """Test depth limit enforcement."""
        pred = XiSymbolic('X')
        
        with pytest.raises(DepthLimitError):
            xi_operator(pred, 15, max_depth=10)
    
    def test_zero_depth(self):
        """Test zero depth operation."""
        pred = XiSymbolic('X')
        result = xi_operator(pred, 0)
        
        assert len(result) == 2  # Just base set
        base_set = pred.base_set()
        assert all(expr in result for expr in base_set)
    
    def test_convergence_behavior(self):
        """Test that xi_operator converges reasonably."""
        pred = XiSymbolic('X')
        
        results = {}
        for depth in range(5):
            result = xi_operator(pred, depth)
            results[depth] = len(result)
        
        # Should generally increase with depth (at least initially)
        assert results[1] >= results[0]
        assert results[2] >= results[1]


class TestValidateXiAttractor:
    """Test xi attractor validation."""
    
    def test_valid_attractor(self):
        """Test validation of valid attractor."""
        pred = XiSymbolic('X')
        attractor = xi_operator(pred, 2)
        
        validation = validate_xi_attractor(attractor, pred)
        
        assert isinstance(validation, dict)
        assert 'total_expressions' in validation
        assert 'validation_passed' in validation
        assert validation['total_expressions'] > 0
    
    def test_invalid_attractor_type(self):
        """Test validation with invalid attractor type."""
        pred = XiSymbolic('X')
        
        with pytest.raises(TypeError):
            validate_xi_attractor("not_list", pred)
        
        with pytest.raises(TypeError):
            validate_xi_attractor(None, pred)
    
    def test_invalid_predicate_type(self):
        """Test validation with invalid predicate type."""
        attractor = []
        
        with pytest.raises(TypeError):
            validate_xi_attractor(attractor, "not_symbolic")


class TestErrorHierarchy:
    """Test RSO exception hierarchy."""
    
    def test_exception_inheritance(self):
        """Test that RSO exceptions inherit correctly."""
        assert issubclass(InvalidPredicateError, RSORuntimeError)
        assert issubclass(DepthLimitError, RSORuntimeError)
        assert issubclass(RSORuntimeError, Exception)
    
    def test_exception_messages(self):
        """Test that exceptions carry meaningful messages."""
        try:
            XiSymbolic("")
        except InvalidPredicateError as e:
            assert "empty" in str(e).lower()
        
        try:
            pred = XiSymbolic('X')
            xi_operator(pred, -1)
        except ValueError as e:
            assert "negative" in str(e).lower()


class TestIntegration:
    """Integration tests combining multiple components."""
    
    def test_oscillator_symbolic_integration(self):
        """Test integration between oscillator and symbolic components."""
        # Create oscillator and symbolic predicate with same concept
        osc = XiOscillator(True)
        pred = XiSymbolic('X')
        
        # Generate oscillation sequence
        sequence = osc.iterate(10)
        
        # Generate symbolic attractor
        attractor = xi_operator(pred, 2)
        
        # Both should represent the same underlying concept
        assert len(sequence) == 10
        assert len(attractor) >= 2
        
        # Validation should pass
        validation = validate_xi_attractor(attractor, pred)
        assert validation['validation_passed']
    
    def test_error_recovery(self):
        """Test that system recovers gracefully from errors."""
        # This should not crash the system
        try:
            XiSymbolic("invalid-name")
        except InvalidPredicateError:
            pass  # Expected
        
        # System should still work normally after error
        pred = XiSymbolic('Y')
        result = xi_operator(pred, 1)
        assert len(result) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])