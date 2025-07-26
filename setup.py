"""
Setup script for RSO Framework.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rso-framework",
    version="1.0.1",
    author="Gregory Betti",
    # author_email="[email will be added when available]",
    description="Recursive Superpositional Ontology - A framework for contradiction-based computation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Betti-Labs/rso-framework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "black>=22.0.0",
            "mypy>=0.910",
            "flake8>=4.0.0",
        ],
        "quantum": [
            "qiskit>=0.39.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "nbsphinx>=0.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "rso=src.cli:main",
            "rso-benchmark=benchmarks.performance_suite:run_benchmarks",
            "rso-verify=src.formal_proofs:run_formal_verification",
            "rso-figures=src.make_figures:main",
        ],
    },
)