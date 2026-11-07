# CPCS-223 Algorithm Trainer

An interactive web-based educational suite designed to help computer science students practice and master foundational data structures and algorithms.

## Featured Trainers

* **AVL Tree Insertion Trainer (`avl.html`):** Interactive practice for inserting values into an AVL tree, identifying imbalance cases (LL, RR, LR, RL), selecting correct rotations, and computing balance factors (height(left) - height(right)).
* **Interpolation Search Trainer (`interpolation.html`):** Step-by-step decrease-and-conquer search execution on sorted arrays, evaluating probing index formulas and tracking search boundary limits ($l, r$).
* **Johnson–Trotter Permutations (`jt.html`):** Permutation generation tracking mobile elements, directional vectors (leftarrow  rightarrow), and element swaps.
* **Russian Peasant Multiplication (`russian.html`):** Halving and doubling table constructor with parity evaluation (n mod 2 neq 0) to compute integer products.

## Technical Highlights

* **Zero-Dependency Architecture:** Written in vanilla JavaScript (ES6+), HTML5, and pure CSS without heavy external frameworks.
* **Dynamic Tree Layout & SVG Engine:** Implements a custom two-pass leaf-positioning algorithm to calculate node (x, y) coordinates and renders dynamic SVG connector paths.
* **State Machine Validation:** Evaluates user inputs against algorithmic ground truths at each step, keeping score of attempts and providing localized error feedback.

## Project Structure

```text
├── index.html          # Hub homepage linking to all trainer tools
├── avl.html            # AVL tree insertion & balance factor module
├── interpolation.html  # Interpolation search step-by-step module
├── jt.html             # Johnson–Trotter algorithm module
├── russian.html        # Russian peasant multiplication module
└── styles.css          # Design system & shared UI variables
