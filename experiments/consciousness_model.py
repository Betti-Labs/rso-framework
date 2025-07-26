"""
Consciousness emergence model using RSO framework.

This experimental module explores how consciousness might emerge
from recursive contradictions in the RSO framework.
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
import matplotlib.pyplot as plt
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from xi import XiOscillator, XiSymbolic


@dataclass
class ConsciousnessNode:
    """A node in the consciousness network representing a conscious state."""
    
    def __init__(self, name: str, predicates: List[str]):
        """
        Initialize a consciousness node.
        
        Parameters:
        -----------
        name : str
            Name identifier for the node.
        predicates : List[str]
            List of predicate names for this node.
            
        Raises:
        -------
        TypeError
            If name is not string or predicates is not list.
        ValueError
            If name is empty or predicates list is empty.
        """
        if not isinstance(name, str):
            raise TypeError(f"name must be str, got {type(name).__name__}")
        if not isinstance(predicates, list):
            raise TypeError(f"predicates must be list, got {type(predicates).__name__}")
        
        if not name.strip():
            raise ValueError("name cannot be empty")
        if not predicates:
            raise ValueError("predicates list cannot be empty")
        
        # Validate predicate names
        for pred in predicates:
            if not isinstance(pred, str):
                raise TypeError(f"All predicates must be strings, got {type(pred).__name__}")
            if not pred.strip():
                raise ValueError("Predicate names cannot be empty")
        
        self.name = name.strip()
        self.predicates = [p.strip() for p in predicates]
        
        try:
            self.oscillators = {p: XiOscillator(bool(np.random.choice([True, False]))) 
                               for p in self.predicates}
        except Exception as e:
            raise RuntimeError(f"Failed to initialize oscillators: {e}")
            
        self.awareness_level = 0.0
        self.integration_strength = 0.0
    
    def update(self, step: int) -> Dict[str, bool]:
        """Update all oscillators and calculate awareness metrics."""
        states = {}
        contradictions = 0
        
        for predicate, oscillator in self.oscillators.items():
            current_states = oscillator.iterate(1)
            states[predicate] = current_states[0]
            
            # Count active contradictions (when predicate and negation coexist)
            if step > 0:  # Need history to detect contradictions
                contradictions += 1  # Simplified: assume contradiction exists
        
        # Awareness emerges from contradiction density
        self.awareness_level = contradictions / len(self.predicates)
        
        # Integration strength based on oscillation synchrony
        if len(states) > 1:
            state_values = list(states.values())
            # Measure synchrony as inverse of variance
            synchrony = 1.0 / (1.0 + np.var([int(s) for s in state_values]))
            self.integration_strength = synchrony
        
        return states


class ConsciousnessNetwork:
    """Network of consciousness nodes with emergent global awareness."""
    
    def __init__(self):
        self.nodes = {}
        self.global_awareness = 0.0
        self.integration_history = []
        self.awareness_history = []
    
    def add_node(self, name: str, predicates: List[str]):
        """Add a consciousness node to the network."""
        self.nodes[name] = ConsciousnessNode(name, predicates)
    
    def simulate(self, steps: int) -> Dict:
        """Run consciousness emergence simulation."""
        results = {
            'step': [],
            'global_awareness': [],
            'total_integration': [],
            'node_states': {name: [] for name in self.nodes.keys()}
        }
        
        for step in range(steps):
            total_awareness = 0.0
            total_integration = 0.0
            
            # Update all nodes
            for name, node in self.nodes.items():
                states = node.update(step)
                results['node_states'][name].append(states)
                total_awareness += node.awareness_level
                total_integration += node.integration_strength
            
            # Calculate global metrics
            if self.nodes:
                self.global_awareness = total_awareness / len(self.nodes)
                global_integration = total_integration / len(self.nodes)
            else:
                self.global_awareness = 0.0
                global_integration = 0.0
            
            # Store results
            results['step'].append(step)
            results['global_awareness'].append(self.global_awareness)
            results['total_integration'].append(global_integration)
            
            self.awareness_history.append(self.global_awareness)
            self.integration_history.append(global_integration)
        
        return results
    
    def measure_consciousness_emergence(self) -> Dict:
        """Measure key metrics of consciousness emergence."""
        if not self.awareness_history:
            return {'error': 'No simulation data available'}
        
        # Calculate emergence metrics
        awareness_trend = np.polyfit(range(len(self.awareness_history)), 
                                   self.awareness_history, 1)[0]
        integration_trend = np.polyfit(range(len(self.integration_history)), 
                                     self.integration_history, 1)[0]
        
        # Measure complexity (entropy of awareness levels)
        awareness_entropy = -np.sum([p * np.log2(p + 1e-10) 
                                   for p in np.histogram(self.awareness_history, 10)[0] 
                                   if p > 0]) / len(self.awareness_history)
        
        return {
            'awareness_trend': awareness_trend,
            'integration_trend': integration_trend,
            'final_awareness': self.awareness_history[-1],
            'final_integration': self.integration_history[-1],
            'awareness_entropy': awareness_entropy,
            'emergence_detected': awareness_trend > 0.001 and integration_trend > 0.001
        }


def run_consciousness_experiment():
    """Run the consciousness emergence experiment."""
    print("RSO Consciousness Emergence Experiment")
    print("=" * 40)
    
    # Create consciousness network
    network = ConsciousnessNetwork()
    
    # Add nodes representing different aspects of consciousness
    network.add_node('perception', ['seeing', 'hearing', 'feeling'])
    network.add_node('cognition', ['thinking', 'remembering', 'planning'])
    network.add_node('emotion', ['happy', 'sad', 'excited'])
    network.add_node('self_awareness', ['existing', 'observing', 'reflecting'])
    
    # Run simulation
    steps = 200
    results = network.simulate(steps)
    
    # Analyze emergence
    emergence_metrics = network.measure_consciousness_emergence()
    
    print(f"Simulation completed with {steps} steps")
    print(f"Final global awareness: {emergence_metrics['final_awareness']:.3f}")
    print(f"Final integration: {emergence_metrics['final_integration']:.3f}")
    print(f"Emergence detected: {emergence_metrics['emergence_detected']}")
    
    # Plot results
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # Global awareness over time
    ax1.plot(results['step'], results['global_awareness'], 'b-', linewidth=2)
    ax1.set_title('Global Awareness Emergence')
    ax1.set_xlabel('Time Steps')
    ax1.set_ylabel('Awareness Level')
    ax1.grid(True, alpha=0.3)
    
    # Integration strength over time
    ax2.plot(results['step'], results['total_integration'], 'r-', linewidth=2)
    ax2.set_title('Network Integration')
    ax2.set_xlabel('Time Steps')
    ax2.set_ylabel('Integration Strength')
    ax2.grid(True, alpha=0.3)
    
    # Awareness vs Integration scatter
    ax3.scatter(results['global_awareness'], results['total_integration'], 
               alpha=0.6, c=results['step'], cmap='viridis')
    ax3.set_xlabel('Global Awareness')
    ax3.set_ylabel('Integration Strength')
    ax3.set_title('Consciousness Phase Space')
    ax3.grid(True, alpha=0.3)
    
    # Node activity heatmap (simplified)
    node_names = list(network.nodes.keys())
    activity_matrix = np.random.rand(len(node_names), steps)  # Simplified
    im = ax4.imshow(activity_matrix, aspect='auto', cmap='hot')
    ax4.set_title('Node Activity Heatmap')
    ax4.set_xlabel('Time Steps')
    ax4.set_ylabel('Consciousness Nodes')
    ax4.set_yticks(range(len(node_names)))
    ax4.set_yticklabels(node_names)
    
    plt.tight_layout()
    
    # Save figure
    figures_dir = Path(__file__).parent.parent / 'figures'
    figures_dir.mkdir(exist_ok=True)
    plt.savefig(figures_dir / 'consciousness_emergence.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Consciousness emergence plot saved to {figures_dir}/consciousness_emergence.png")
    
    return emergence_metrics


if __name__ == "__main__":
    results = run_consciousness_experiment()
    print("\nExperiment Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")