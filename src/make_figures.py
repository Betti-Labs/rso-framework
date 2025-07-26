"""
Utility functions to generate visual representations of the Recursive
Superpositional Ontology (RSO) framework.  Each function draws a
specific kind of diagram described in Gregory Betti's framework and
saves the result both as a PNG and a PDF.  These diagrams are
generated using only deterministic computations so that they are
completely reproducible across runs.

The diagrams include:

* A one‑predicate Ξ graph showing the recursive loop between a property
  and its negation.  Nodes are arranged in a circle with arrows
  representing the superpositional operator (⊕) cycling between x
  and ¬x.  There is also a self‑loop on the contradictory state
  x∧¬x.
* A two‑predicate Ξ² graph showing four nodes (x, ¬x, y, ¬y) with
  bidirectional edges capturing the richer recursion space.  This
  diagram illustrates how combinations of properties generate more
  complex attractors.
* A contradiction lattice describing the space of truth values
  available in the RSO framework (True, False, Both, Neither).  This
  lattice highlights that the "both" state is a legitimate, stable
  attractor rather than an error state.
* A recursive orbit plot visualising the temporal cycling of a
  property and its negation.  This diagram uses a sine wave to show
  how the state flips back and forth over time while remaining
  bounded between the two extremes.
* A toy simulation output from the hot/cold example.  Here, the
  oscillator toggles between True and False and we plot this as a
  discrete time series.

All images are saved into the ``figures/`` directory when this
module is executed as a script.  Example usage:

>>> python -m make_figures

Requirements: networkx, matplotlib, numpy
"""

import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
import numpy as np


FIG_DIR = Path(__file__).resolve().parents[1] / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_figure(fig: plt.Figure, name: str) -> None:
    """Save a Matplotlib figure in PNG and PDF formats.

    Parameters
    ----------
    fig : plt.Figure
        The figure to save.
    name : str
        Base filename (without extension).  Files will be written
        under ``FIG_DIR`` with both ``.png`` and ``.pdf`` extensions.
    """
    png_path = FIG_DIR / f"{name}.png"
    pdf_path = FIG_DIR / f"{name}.pdf"
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(pdf_path, dpi=300, bbox_inches="tight")
    print(f"Saved {png_path} and {pdf_path}")


def draw_xi_one(predicate: str = "x") -> None:
    """Draw a one‑predicate Ξ graph.

    Parameters
    ----------
    predicate : str, optional
        The name of the predicate.  Default is "x".
    """
    # Define node labels
    pos = predicate
    neg = f"¬{predicate}"
    both = f"{predicate}∧¬{predicate}"
    # Assign fixed positions
    positions = {
        pos: (0, 1),
        both: (1, 0),
        neg: (0, -1),
    }
    # Define directed edges: list of (src, dst)
    edges = [
        (pos, both),
        (both, neg),
        (neg, both),
        (both, pos),
    ]
    # Plot using matplotlib primitives
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title(f"Ξ graph for predicate {predicate}")
    # Draw nodes as circles
    for label, (x, y) in positions.items():
        circ = Circle((x, y), 0.2, facecolor="lightblue", edgecolor="black")
        ax.add_patch(circ)
        ax.text(x, y, label, fontsize=12, ha="center", va="center")
    # Draw arrows
    for src, dst in edges:
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        # Calculate arrow positions slightly offset from node boundaries
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        # Normalise
        if length != 0:
            dxn = dx / length
            dyn = dy / length
        else:
            dxn = dyn = 0
        start = (x1 + 0.2 * dxn, y1 + 0.2 * dyn)
        end = (x2 - 0.2 * dxn, y2 - 0.2 * dyn)
        arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=10,
                                color="black", lw=1.0)
        ax.add_patch(arrow)
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_axis_off()
    save_figure(fig, f"xi_one_{predicate}")
    plt.close(fig)


def draw_xi_two(p1: str = "x", p2: str = "y") -> None:
    """Draw a two‑predicate Ξ² graph.

    Parameters
    ----------
    p1 : str, optional
        Name of the first predicate.
    p2 : str, optional
        Name of the second predicate.
    """
    # Prepare node labels and positions
    labels = [p1, f"¬{p1}", p2, f"¬{p2}"]
    positions = {
        p1: (-1, 1),
        f"¬{p1}": (-1, -1),
        p2: (1, 1),
        f"¬{p2}": (1, -1),
    }
    # Define edges to illustrate cycles and cross‑links
    edges = [
        (p1, p2), (p2, f"¬{p1}"), (f"¬{p1}", f"¬{p2}"), (f"¬{p2}", p1),
        (p1, f"¬{p2}"), (f"¬{p2}", f"¬{p1}"), (f"¬{p1}", p2), (p2, p1)
    ]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(f"Ξ² graph for predicates {p1} and {p2}")
    # Draw nodes
    for label in labels:
        x, y = positions[label]
        circ = Circle((x, y), 0.25, facecolor="lightgreen", edgecolor="black")
        ax.add_patch(circ)
        ax.text(x, y, label, fontsize=12, ha="center", va="center")
    # Draw arrows
    for src, dst in edges:
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        dxn = dx / length
        dyn = dy / length
        start = (x1 + 0.25 * dxn, y1 + 0.25 * dyn)
        end = (x2 - 0.25 * dxn, y2 - 0.25 * dyn)
        arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=10,
                                color="black", lw=1.0)
        ax.add_patch(arrow)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_axis_off()
    save_figure(fig, f"xi_two_{p1}_{p2}")
    plt.close(fig)


def draw_contradiction_lattice() -> None:
    """Draw a simple contradiction lattice.

    This lattice illustrates the four truth values in RSO: True (T),
    False (F), Both (B), and Neither (N).  Edges show how one can
    transition between these values by adding or removing assertions.
    """
    # Define nodes and positions manually
    labels = ["True", "False", "Both", "Neither"]
    positions = {
        "True": (0, 1),
        "False": (0, -1),
        "Both": (1, 0),
        "Neither": (-1, 0),
    }
    # Edges mapping transitions
    edges = [
        ("True", "Both"),
        ("False", "Both"),
        ("Neither", "True"),
        ("Neither", "False"),
        ("Both", "True"),
        ("Both", "False"),
    ]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title("Contradiction lattice in RSO")
    # Draw nodes
    for label in labels:
        x, y = positions[label]
        circ = Circle((x, y), 0.25, facecolor="lightcoral", edgecolor="black")
        ax.add_patch(circ)
        ax.text(x, y, label, fontsize=12, ha="center", va="center")
    # Draw arrows
    for src, dst in edges:
        x1, y1 = positions[src]
        x2, y2 = positions[dst]
        dx = x2 - x1
        dy = y2 - y1
        length = (dx**2 + dy**2) ** 0.5
        dxn = dx / length
        dyn = dy / length
        start = (x1 + 0.25 * dxn, y1 + 0.25 * dyn)
        end = (x2 - 0.25 * dxn, y2 - 0.25 * dyn)
        arrow = FancyArrowPatch(start, end, arrowstyle="->", mutation_scale=10,
                                color="black", lw=1.0)
        ax.add_patch(arrow)
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_axis_off()
    save_figure(fig, "contradiction_lattice")
    plt.close(fig)


def draw_recursive_orbit(periods: int = 2, points: int = 200) -> None:
    """Draw a continuous oscillation representing a recursive orbit.

    The oscillation is drawn as a sine wave to emphasise the smooth
    transition between states.  High values correspond to the
    predicate being "active" (True), while low values correspond to
    its negation (False).  The horizontal axis denotes iterative
    steps or time, and the vertical axis shows the state.

    Parameters
    ----------
    periods : int, optional
        Number of complete oscillation cycles to plot.
    points : int, optional
        Number of sample points used in the plot.
    """
    t = np.linspace(0, periods * 2 * np.pi, points)
    y = np.sin(t)
    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(t, y, color="steelblue")
    ax.set_title("Recursive oscillation orbit (sine representation)")
    ax.set_xlabel("Iteration (arbitrary units)")
    ax.set_ylabel("State amplitude")
    # Add horizontal lines marking the two extremes
    ax.axhline(1, color="grey", linestyle="--", linewidth=0.5)
    ax.axhline(-1, color="grey", linestyle="--", linewidth=0.5)
    save_figure(fig, "recursive_orbit")
    plt.close(fig)


def draw_hot_cold_simulation(steps: int = 20) -> None:
    """Draw a discrete hot/cold toy simulation as a step plot.

    A simple oscillator toggles between True (hot) and False (cold).

    Parameters
    ----------
    steps : int, optional
        Number of steps in the discrete simulation.
    """
    states = [i % 2 for i in range(steps)]  # 0 for hot/True, 1 for cold/False
    t = np.arange(steps)
    fig, ax = plt.subplots(figsize=(7, 2))
    ax.step(t, states, where="post", color="darkorange")
    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Hot (True)", "Cold (False)"])
    ax.set_xlabel("Iteration")
    ax.set_title("Discrete hot/cold Ξ simulation")
    save_figure(fig, "hot_cold_simulation")
    plt.close(fig)


def main() -> None:
    """Generate all figures."""
    draw_xi_one("X")
    draw_xi_two("X", "Y")
    draw_contradiction_lattice()
    draw_recursive_orbit()
    draw_hot_cold_simulation()


if __name__ == "__main__":
    main()