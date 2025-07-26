"""
Command-line interface for RSO Framework.

This module provides a comprehensive CLI for interacting with the RSO framework,
including running benchmarks, generating figures, and performing formal verification.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from xi import XiOscillator, XiSymbolic, xi_operator, validate_xi_attractor
from formal_proofs import run_formal_verification
from make_figures import main as generate_figures


def cmd_oscillate(args):
    """Run oscillator simulation."""
    try:
        oscillator = XiOscillator(args.initial)
        history = oscillator.iterate(args.steps)
        
        if args.output:
            with open(args.output, 'w') as f:
                for i, state in enumerate(history):
                    f.write(f"{i},{state}\n")
            print(f"Oscillation history saved to {args.output}")
        else:
            print("Oscillation history:")
            for i, state in enumerate(history):
                print(f"Step {i}: {state}")
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_symbolic(args):
    """Generate symbolic Xi attractor."""
    try:
        predicate = XiSymbolic(args.predicate)
        attractor = xi_operator(predicate, args.depth)
        
        print(f"Xi attractor for '{args.predicate}' at depth {args.depth}:")
        print(f"Total expressions: {len(attractor)}")
        
        if args.validate:
            validation = validate_xi_attractor(attractor, predicate)
            print(f"Validation: {'PASSED' if validation['validation_passed'] else 'FAILED'}")
            print(f"Contains contradiction: {validation['contains_contradiction']}")
            print(f"Contains tautology: {validation['contains_tautology']}")
        
        if args.verbose:
            print("\nExpressions:")
            for i, expr in enumerate(attractor):
                print(f"  {i+1}: {expr}")
                
        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Xi attractor for '{args.predicate}' at depth {args.depth}\n")
                f.write(f"Total expressions: {len(attractor)}\n\n")
                for i, expr in enumerate(attractor):
                    f.write(f"{i+1}: {expr}\n")
            print(f"Attractor saved to {args.output}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_verify(args):
    """Run formal verification."""
    try:
        print("Running RSO formal verification suite...")
        results = run_formal_verification()
        
        print("\nVerification Results:")
        print("=" * 40)
        
        for test_name, result in results.items():
            print(f"\n{test_name.upper().replace('_', ' ')}:")
            if isinstance(result, dict):
                for key, value in result.items():
                    print(f"  {key}: {value}")
            else:
                print(f"  Result: {result}")
        
        if args.output:
            import json
            with open(args.output, 'w') as f:
                # Convert results to JSON-serializable format
                json_results = {}
                for key, value in results.items():
                    if isinstance(value, dict):
                        json_results[key] = value
                    else:
                        json_results[key] = str(value)
                json.dump(json_results, f, indent=2)
            print(f"\nResults saved to {args.output}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_benchmark(args):
    """Run performance benchmarks."""
    try:
        sys.path.append(str(Path(__file__).parent.parent / 'benchmarks'))
        from performance_suite import RSOBenchmarkSuite
        
        print("Running RSO performance benchmarks...")
        suite = RSOBenchmarkSuite()
        summary = suite.run_comprehensive_benchmark()
        
        print(f"\nBenchmark Summary:")
        print(f"Total benchmarks: {summary['total_benchmarks']}")
        print(f"Average execution time: {summary['avg_execution_time']:.6f}s")
        print(f"Fastest operation: {summary['fastest_operation'].operation}")
        print(f"Slowest operation: {summary['slowest_operation'].operation}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_figures(args):
    """Generate RSO figures."""
    try:
        print("Generating RSO figures...")
        generate_figures()
        print("Figures generated successfully!")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def cmd_demo(args):
    """Run interactive demo."""
    try:
        print("RSO Framework Interactive Demo")
        print("=" * 30)
        
        # Oscillator demo
        print("\n1. Oscillator Demo:")
        osc = XiOscillator(True)
        history = osc.iterate(8)
        print(f"Oscillation: {history}")
        
        # Symbolic demo
        print("\n2. Symbolic Demo:")
        pred = XiSymbolic('Demo')
        attractor = xi_operator(pred, 2)
        print(f"Xi attractor has {len(attractor)} expressions")
        
        # Validation demo
        print("\n3. Validation Demo:")
        validation = validate_xi_attractor(attractor, pred)
        print(f"Validation passed: {validation['validation_passed']}")
        
        print("\nDemo completed! Use --help for more options.")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="RSO Framework - Recursive Superpositional Ontology",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  rso oscillate --steps 10 --initial true
  rso symbolic --predicate X --depth 3 --validate
  rso verify --output results.json
  rso benchmark
  rso figures
  rso demo
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Oscillate command
    osc_parser = subparsers.add_parser('oscillate', help='Run oscillator simulation')
    osc_parser.add_argument('--steps', type=int, default=10, 
                           help='Number of oscillation steps')
    osc_parser.add_argument('--initial', type=str, choices=['true', 'false'], 
                           default='true', help='Initial state')
    osc_parser.add_argument('--output', type=str, help='Output file for results')
    osc_parser.set_defaults(func=cmd_oscillate)
    
    # Symbolic command
    sym_parser = subparsers.add_parser('symbolic', help='Generate symbolic Xi attractor')
    sym_parser.add_argument('--predicate', type=str, default='X', 
                           help='Predicate name')
    sym_parser.add_argument('--depth', type=int, default=2, 
                           help='Recursion depth')
    sym_parser.add_argument('--validate', action='store_true', 
                           help='Validate the attractor')
    sym_parser.add_argument('--verbose', action='store_true', 
                           help='Show all expressions')
    sym_parser.add_argument('--output', type=str, help='Output file for results')
    sym_parser.set_defaults(func=cmd_symbolic)
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Run formal verification')
    verify_parser.add_argument('--output', type=str, help='Output file for results')
    verify_parser.set_defaults(func=cmd_verify)
    
    # Benchmark command
    bench_parser = subparsers.add_parser('benchmark', help='Run performance benchmarks')
    bench_parser.set_defaults(func=cmd_benchmark)
    
    # Figures command
    fig_parser = subparsers.add_parser('figures', help='Generate RSO figures')
    fig_parser.set_defaults(func=cmd_figures)
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run interactive demo')
    demo_parser.set_defaults(func=cmd_demo)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Convert string boolean to actual boolean for oscillate command
    if hasattr(args, 'initial'):
        args.initial = args.initial.lower() == 'true'
    
    # Execute command
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())