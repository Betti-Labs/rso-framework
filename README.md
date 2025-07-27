# Recursive Superpositional Ontology (RSO) Laboratory

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen?style=flat-square&logo=github)](https://betti-labs.github.io/rso-framework/)
[![Academia.edu](https://img.shields.io/badge/Academia.edu-Published-blue?style=flat-square&logo=academia)](https://www.academia.edu/143089984/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/downloads/)

## 🎉 **PUBLISHED RESEARCH** 🎉

🔊 **[Listen to the RSO Deep Dive](https://betti-labs.github.io/rso-framework/)** | 📄 **[Read the Full Paper on Academia.edu](https://www.academia.edu/143089984/Recursive_Superpositional_Ontology_A_Computational_Framework_for_Contradiction_Preserving_Logic_and_Reality_Modeling)**

*"Recursive Superpositional Ontology: A Computational Framework for Contradiction-Preserving Logic and Reality Modeling"* by Gregory Betti is now available for the global research community.

---

Welcome to the **RSO Laboratory**, an open repository for exploring the
metaphysical and symbolic logic framework introduced in _Recursive Superpositional Ontology: A Computational Framework for Contradiction-Preserving Logic and Reality Modeling_.

This repository accompanies the scientific paper written by
**Gregory Betti (Betti Labs)** and contains reproducible code,
visualisations, and documentation needed to investigate the
**Recursive Superpositional Ontology (RSO)**.  The lab is organised
around the idea that reality is not composed of resolved states but of
recursive contradictions captured by the operator ⊕ and its
associated contradiction field Ξ.

## Philosophy

RSO begins from a radical ontological axiom: **every property \(x\)
coexists with its negation \(¬x\)**.  Rather than treating the
contradiction \(x ∧ ¬x\) as an impossibility, RSO elevates it to a
fundamental ingredient of being.  The universe is described as a
superposition of every predicate and its opposite, generating a
network of **Ξ‑nodes** that constantly loop between states.  This
recursion is not a failure of logic; it is the engine of existence.

### Key Principles

* **Contradiction‑preserving superposition (⊕):** A binary operator that
  combines a predicate with its negation without resolving their
  opposition.  Iterating ⊕ generates a **Ξ attractor**, a symbolic
  structure containing all variations of \(x\) and \(¬x\).
* **Ξ fields:** The self‑referential sets resulting from the ⊕
  operation.  Each Ξ contains the predicate, its negation, their
  conjunction, and further nested superpositions.  Ξ‑graphs visualise
  these structures as loops with tension arrows.
* **Recursion as reality:** Time, space, matter, and consciousness
  emerge from the velocities and orientations of Ξ cycles.  Nothing
  ultimately collapses—every collapse is a local projection of a
  deeper recursion.

For philosophical context, RSO resonates with ideas from **Heraclitus**
(unity of opposites and flux), **Daoist yin–yang** (interdependence of
contrary forces), and modern **paraconsistent logics** that reject
explosion in the presence of contradictions【800088766790706†L41-L54】.  It also echoes the
**many‑worlds interpretation** of quantum mechanics, which removes
wave function collapse and treats the universe as an ever‑branching
superposition【751751222457522†L457-L464】.  These influences underscore
the plausibility of a reality built on recursive contradiction.

## Contents

```
RSO-Lab/
├── figures/            # PNG and PDF diagrams generated from code
├── notebooks/          # Jupyter notebooks for interactive exploration
├── src/                # Python modules implementing RSO concepts
├── README.md           # This file
├── requirements.txt    # Python package requirements
└── …
```

### `figures/`

The **figures** directory contains reproductions of the key diagrams
used in the paper.  They are generated programmatically by
`src/make_figures.py` and include:

* **xi_one_X.(png|pdf)** – one‑predicate Ξ graph showing the loop
  between \(x\), \(¬x\), and the contradictory state \(x∧¬x\).
* **xi_two_X_Y.(png|pdf)** – two‑predicate Ξ² graph illustrating the
  richer structure of combining predicates \(x\) and \(y\).
* **contradiction_lattice.(png|pdf)** – lattice of the four truth
  values (True, False, Both, Neither) highlighting the legitimacy of
  the “Both” state in paraconsistent reasoning.
* **recursive_orbit.(png|pdf)** – continuous oscillation representing
  a recursive orbit.
* **hot_cold_simulation.(png|pdf)** – discrete toy model toggling
  between hot and cold states.

### `src/`

* **`xi.py`** – Implements the `XiOscillator` class for discrete
  oscillations, the `XiSymbolic` class for symbolic predicates using
  SymPy, and the `xi_operator` function to build finite
  approximations to Ξ fields.
* **`make_figures.py`** – Generates all diagrams in the `figures`
  directory.  It uses only `matplotlib` primitives so that no
  external graph library is required.

### `notebooks/`

* **`xi_simulation.ipynb`** – A short Jupyter notebook acting as a
  **Ξ playground**.  It demonstrates how to create an oscillator,
  iterate its states, and construct symbolic contradiction fields.

## Testable Predictions

The RSO framework makes several qualitative predictions that can be
investigated computationally:

1. **Stability thresholds:** A Ξ attractor remains stable only if the
   recursion is continued indefinitely.  If the oscillation is
   interrupted or one state is favoured, a “collapse” occurs.  Simple
   models, such as the hot/cold simulation in this repository, can
   explore how long it takes for such interruptions to occur under
   perturbations.
2. **Emergent time:** The period of oscillation in a Ξ cycle defines
   an emergent temporal scale.  Simulations of coupled oscillators may
   exhibit phase synchronisation that resembles thermodynamic or
   causal arrows of time.
3. **Composite attractors:** Combining predicates via Ξ² should yield
   richer dynamics, potentially displaying quasi‑periodic or chaotic
   behaviour.  One can numerically explore these multi‑predicate
   systems by extending `XiOscillator` to more than one dimension.

## Getting Started

### Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/Betti-Labs/rso-framework.git
   cd rso-framework
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Install in development mode:
   ```bash
   pip install -e .
   ```

### Quick Start

#### Command Line Interface

The RSO framework includes a comprehensive CLI for easy interaction:

```bash
# Run interactive demo
python src/cli.py demo

# Generate oscillation sequence
python src/cli.py oscillate --steps 20 --initial true

# Create symbolic Xi attractor
python src/cli.py symbolic --predicate X --depth 3 --validate --verbose

# Run formal verification
python src/cli.py verify

# Generate performance benchmarks
python src/cli.py benchmark

# Generate all figures
python src/cli.py figures
```

#### Python API

```python
from src.xi import XiOscillator, XiSymbolic, xi_operator

# Create and run oscillator
oscillator = XiOscillator(True)
history = oscillator.iterate(10)
print(f"Oscillation: {history}")

# Create symbolic predicate and Xi attractor
predicate = XiSymbolic('Consciousness')
attractor = xi_operator(predicate, depth=2)
print(f"Xi attractor has {len(attractor)} expressions")

# Validate the attractor
from src.xi import validate_xi_attractor
validation = validate_xi_attractor(attractor, predicate)
print(f"Validation passed: {validation['validation_passed']}")
```

#### Jupyter Notebooks

Launch the interactive notebook for experimentation:

```bash
jupyter notebook notebooks/xi_simulation.ipynb
```

### Advanced Usage

#### Formal Verification

```python
from src.formal_proofs import run_formal_verification

results = run_formal_verification()
print("Verification results:", results)
```

#### Quantum Bridge

```python
from src.quantum_bridge import QuantumXiState

# Create quantum superposition state
quantum_state = QuantumXiState(alpha=0.6, beta=0.8)
print(f"P(x) = {quantum_state.probability_x():.3f}")

# Time evolution
evolved = quantum_state.evolve(time=3.14, frequency=1.0)
print(f"Evolved P(x) = {evolved.probability_x():.3f}")
```

#### Performance Benchmarking

```python
from benchmarks.performance_suite import RSOBenchmarkSuite

suite = RSOBenchmarkSuite()
summary = suite.run_comprehensive_benchmark()
print(f"Average execution time: {summary['avg_execution_time']:.6f}s")
```

We hope these tools help you delve deeper into the paradoxical yet
structured world of Recursive Superpositional Ontology.

## 📚 How to Cite

If you use the RSO framework in your research, please cite the published paper:

**APA Style:**
```
Betti, G. (2025). Recursive Superpositional Ontology: A Computational Framework for Contradiction-Preserving Logic and Reality Modeling. Academia.edu. https://www.academia.edu/143089984/
```

**BibTeX:**
```bibtex
@article{betti2025rso,
  title={Recursive Superpositional Ontology: A Computational Framework for Contradiction-Preserving Logic and Reality Modeling},
  author={Betti, Gregory},
  journal={Academia.edu},
  year={2025},
  url={https://www.academia.edu/143089984/Recursive_Superpositional_Ontology_A_Computational_Framework_for_Contradiction_Preserving_Logic_and_Reality_Modeling}
}
```

**Software Citation:**
```
Betti, G. (2025). RSO Framework: Recursive Superpositional Ontology (Version 1.0.1) [Computer software]. GitHub. https://github.com/Betti-Labs/rso-framework
```
