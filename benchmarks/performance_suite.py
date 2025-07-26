"""
Performance benchmarking suite for RSO framework.

This module provides comprehensive benchmarks to measure the computational
efficiency and scalability of RSO operations.
"""

import time
import numpy as np
from typing import Dict, List, Callable
from dataclasses import dataclass
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from xi import XiOscillator, XiSymbolic, xi_operator


@dataclass
class BenchmarkResult:
    """Container for benchmark results."""
    operation: str
    input_size: int
    execution_time: float
    memory_usage: float
    iterations_per_second: float


class RSOBenchmarkSuite:
    """Comprehensive benchmarking suite for RSO operations."""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
    
    def benchmark_oscillator_performance(self, max_steps: int = 10000) -> List[BenchmarkResult]:
        """Benchmark XiOscillator performance across different step counts.
        
        Parameters:
        -----------
        max_steps : int
            Maximum number of steps to benchmark.
            
        Returns:
        --------
        List[BenchmarkResult]
            List of benchmark results.
            
        Raises:
        -------
        TypeError
            If max_steps is not an integer.
        ValueError
            If max_steps is not positive.
        """
        if not isinstance(max_steps, int):
            raise TypeError(f"max_steps must be int, got {type(max_steps).__name__}")
        if max_steps <= 0:
            raise ValueError(f"max_steps must be positive, got {max_steps}")
        
        step_sizes = [100, 500, 1000, 2500, 5000, max_steps]
        # Filter out step sizes larger than max_steps
        step_sizes = [s for s in step_sizes if s <= max_steps]
        # Ensure max_steps is included
        if max_steps not in step_sizes:
            step_sizes.append(max_steps)
        step_sizes.sort()
        
        results = []
        
        for steps in step_sizes:
            try:
                oscillator = XiOscillator(True)
                
                # Measure execution time
                start_time = time.perf_counter()
                history = oscillator.iterate(steps)
                end_time = time.perf_counter()
                
                execution_time = end_time - start_time
                iterations_per_second = steps / execution_time if execution_time > 0 else float('inf')
                
                # Estimate memory usage (simplified)
                memory_usage = len(history) * 8  # 8 bytes per boolean (rough estimate)
                
                result = BenchmarkResult(
                    operation="oscillator_iteration",
                    input_size=steps,
                    execution_time=execution_time,
                    memory_usage=memory_usage,
                    iterations_per_second=iterations_per_second
                )
                
                results.append(result)
                self.results.append(result)
                
                print(f"Oscillator {steps} steps: {execution_time:.4f}s, "
                      f"{iterations_per_second:.0f} iter/s")
                      
            except Exception as e:
                print(f"Warning: Failed to benchmark {steps} steps: {e}")
                continue
        
        if not results:
            raise RuntimeError("All oscillator benchmarks failed")
        
        return results
    
    def benchmark_xi_operator_scaling(self, max_depth: int = 6) -> List[BenchmarkResult]:
        """Benchmark xi_operator performance across different recursion depths."""
        depths = list(range(1, max_depth + 1))
        results = []
        
        for depth in depths:
            predicate = XiSymbolic('X')
            
            # Measure execution time and memory
            start_time = time.perf_counter()
            attractor = xi_operator(predicate, depth)
            end_time = time.perf_counter()
            
            execution_time = end_time - start_time
            memory_usage = len(attractor) * 100  # Rough estimate for SymPy expressions
            
            result = BenchmarkResult(
                operation="xi_operator",
                input_size=depth,
                execution_time=execution_time,
                memory_usage=memory_usage,
                iterations_per_second=1.0 / execution_time if execution_time > 0 else float('inf')
            )
            
            results.append(result)
            self.results.append(result)
            
            print(f"Xi operator depth {depth}: {execution_time:.4f}s, "
                  f"{len(attractor)} expressions")
        
        return results
    
    def benchmark_symbolic_operations(self) -> List[BenchmarkResult]:
        """Benchmark symbolic predicate operations."""
        operations = [
            ("create_predicate", lambda: XiSymbolic('P')),
            ("base_set", lambda p: p.base_set()),
            ("xi_depth_1", lambda p: xi_operator(p, 1)),
            ("xi_depth_2", lambda p: xi_operator(p, 2)),
        ]
        
        results = []
        predicate = XiSymbolic('TestPredicate')
        
        for op_name, operation in operations:
            # Run operation multiple times for accurate timing
            iterations = 1000 if 'create' in op_name else 100
            
            start_time = time.perf_counter()
            for _ in range(iterations):
                if op_name == "create_predicate":
                    operation()
                else:
                    operation(predicate)
            end_time = time.perf_counter()
            
            total_time = end_time - start_time
            avg_time = total_time / iterations
            
            result = BenchmarkResult(
                operation=op_name,
                input_size=iterations,
                execution_time=avg_time,
                memory_usage=0.0,  # Not measured for symbolic ops
                iterations_per_second=1.0 / avg_time if avg_time > 0 else float('inf')
            )
            
            results.append(result)
            self.results.append(result)
            
            print(f"Symbolic {op_name}: {avg_time:.6f}s avg, "
                  f"{result.iterations_per_second:.0f} ops/s")
        
        return results
    
    def run_comprehensive_benchmark(self) -> Dict:
        """Run all benchmarks and return summary statistics."""
        print("RSO Framework Performance Benchmark Suite")
        print("=" * 50)
        
        print("\n1. Oscillator Performance:")
        oscillator_results = self.benchmark_oscillator_performance()
        
        print("\n2. Xi Operator Scaling:")
        xi_results = self.benchmark_xi_operator_scaling()
        
        print("\n3. Symbolic Operations:")
        symbolic_results = self.benchmark_symbolic_operations()
        
        # Generate performance plots
        self.plot_performance_results()
        
        # Calculate summary statistics
        summary = {
            'total_benchmarks': len(self.results),
            'fastest_operation': min(self.results, key=lambda r: r.execution_time),
            'slowest_operation': max(self.results, key=lambda r: r.execution_time),
            'avg_execution_time': np.mean([r.execution_time for r in self.results]),
            'total_benchmark_time': sum(r.execution_time for r in self.results)
        }
        
        return summary
    
    def plot_performance_results(self):
        """Generate performance visualization plots."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        
        # Oscillator performance scaling
        oscillator_results = [r for r in self.results if r.operation == "oscillator_iteration"]
        if oscillator_results:
            sizes = [r.input_size for r in oscillator_results]
            times = [r.execution_time for r in oscillator_results]
            ax1.loglog(sizes, times, 'bo-', linewidth=2, markersize=6)
            ax1.set_xlabel('Steps')
            ax1.set_ylabel('Execution Time (s)')
            ax1.set_title('Oscillator Performance Scaling')
            ax1.grid(True, alpha=0.3)
        
        # Xi operator complexity
        xi_results = [r for r in self.results if r.operation == "xi_operator"]
        if xi_results:
            depths = [r.input_size for r in xi_results]
            times = [r.execution_time for r in xi_results]
            ax2.semilogy(depths, times, 'ro-', linewidth=2, markersize=6)
            ax2.set_xlabel('Recursion Depth')
            ax2.set_ylabel('Execution Time (s)')
            ax2.set_title('Xi Operator Complexity')
            ax2.grid(True, alpha=0.3)
        
        # Operations per second comparison
        operations = list(set(r.operation for r in self.results))
        avg_ops_per_sec = []
        for op in operations:
            op_results = [r for r in self.results if r.operation == op]
            avg_ops = np.mean([r.iterations_per_second for r in op_results])
            avg_ops_per_sec.append(avg_ops)
        
        ax3.bar(range(len(operations)), avg_ops_per_sec, color='green', alpha=0.7)
        ax3.set_xlabel('Operation Type')
        ax3.set_ylabel('Operations per Second')
        ax3.set_title('Performance Comparison')
        ax3.set_xticks(range(len(operations)))
        ax3.set_xticklabels(operations, rotation=45, ha='right')
        ax3.set_yscale('log')
        
        # Memory usage estimation
        memory_results = [r for r in self.results if r.memory_usage > 0]
        if memory_results:
            sizes = [r.input_size for r in memory_results]
            memory = [r.memory_usage for r in memory_results]
            ax4.plot(sizes, memory, 'mo-', linewidth=2, markersize=6)
            ax4.set_xlabel('Input Size')
            ax4.set_ylabel('Memory Usage (bytes)')
            ax4.set_title('Memory Usage Scaling')
            ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save performance plots
        figures_dir = Path(__file__).parent.parent / 'figures'
        figures_dir.mkdir(exist_ok=True)
        plt.savefig(figures_dir / 'performance_benchmarks.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\nPerformance plots saved to {figures_dir}/performance_benchmarks.png")


def run_benchmarks():
    """Main function to run all benchmarks."""
    suite = RSOBenchmarkSuite()
    summary = suite.run_comprehensive_benchmark()
    
    print(f"\n{'='*50}")
    print("BENCHMARK SUMMARY")
    print(f"{'='*50}")
    print(f"Total benchmarks run: {summary['total_benchmarks']}")
    print(f"Average execution time: {summary['avg_execution_time']:.6f}s")
    print(f"Fastest operation: {summary['fastest_operation'].operation} "
          f"({summary['fastest_operation'].execution_time:.6f}s)")
    print(f"Slowest operation: {summary['slowest_operation'].operation} "
          f"({summary['slowest_operation'].execution_time:.6f}s)")
    print(f"Total benchmark time: {summary['total_benchmark_time']:.3f}s")
    
    return summary


if __name__ == "__main__":
    run_benchmarks()