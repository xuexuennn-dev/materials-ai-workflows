# Materials Research Workflows & LLM Scientific Evaluation Suite

A modular Python framework demonstrating materials informatics, quantitative electrochemical kinetics modeling, uncertainty-aware experimental design, and primary-source grounded evaluation rubrics for frontier AI models.

---

## 🔬 Core Workflows & Methodological Demonstrations

1. **Materials Informatics & Atomistic Structures (`pymatgen`, `ase`, `matminer`)**
   - Crystal structure manipulation, format transformation (CIF, POSCAR), and electronic input preparation.
   - Theoretical X-ray diffraction pattern simulation from structural models.
   - Extraction of composition-based physical/chemical descriptors (electronegativity differences, valence electron concentrations) for downstream statistical learning.

2. **Electrochemical Transport & Kinetic Modeling (`impedance.py`, `scipy`, `numpy`)**
   - **EIS Equivalent Circuit Modeling**: Automated non-linear least-squares fitting of complex impedance data with explicit parameter recovery error bounds (< 0.08% relative error on synthetic validation spectra).
   - **CV Scan-Rate Decomposition**: Deconvolution of surface capacitive vs. diffusion-controlled currents via power-law peak-current regression ($i = a \cdot v^b$).
   - **GITT Titration Transport Analysis**: Computation of state-of-charge dependent apparent diffusion coefficients ($D_{\text{app}}$) via Weppner-Huggins boundary conditions, explicitly flagging transport assumptions.

3. **Uncertainty-Aware Experimental Design (`scikit-learn`)**
   - Space-filling initial sampling (Latin hypercube / uniform design).
   - Gaussian Process (GP) regression with Matern/RBF covariance kernels.
   - Acquisition function ranking (Expected Improvement, Upper Confidence Bound) under synthesis feasibility constraints to minimize exploratory wet-chemical iterations.

4. **Atomistic Migration Barrier Automation (`ase`)**
   - Climbing-Image Nudged Elastic Band (CI-NEB) workflow demonstration utilizing the classical Effective Medium Theory (EMT) reference potential.
   - Automates minimum energy pathway (MEP) image generation, force convergence monitoring, and activation barrier extraction.
   - *Note*: Classical potentials provide workflow verification; quantitative barriers in complex multivalent materials require converged DFT / validated MLIP engines.

---

## 🎯 Curated Scientific AI Evaluation Rubrics & Error Taxonomies (人工构造的科学推理评测示例与多维评分细则)

The repository provides a domain-specific evaluation framework (`scientific_evaluation_cases.json`, `evaluate_stem_cases.py`, `evaluation_results.json`) demonstrating how expert rubrics audit scientific reasoning across physical chemistry, electrochemistry, and crystallography.

> **Provenance & Scope**: This suite serves as a curated reference benchmark for rubric calibration and error taxonomy demonstration. It contains handcrafted canonical responses and deliberate failure modes to illustrate systematic scoring criteria, rather than automated live API benchmarking of third-party commercial models.

### Multi-Dimensional Evaluation Rubric
- **Physical & Chemical Validity (0–2)**: Strict adherence to conservation laws, dimensional analysis, reaction stoichiometry, and redox equilibrium.
- **Assumptions & Uncertainty Bounds (0–2)**: Explicit statement of applicable regimes, non-uniqueness, and boundary conditions.
- **Evidence & Primary-Source Grounding (0–2)**: Rigorous verification against peer-reviewed literature; zero tolerance for hallucinated citations or fabricated synthesis protocols.
- **Reproducibility & Provenance (0–2)**: Complete specification of thermodynamic parameters, concentrations, and computational settings.

### Exemplar Audit Cases & Error Taxonomies (`evaluation_results.json`)
- **Total Curated Scenarios**: 8 domain-specific benchmark cases.
- **Demonstrated Penalty Mechanics for High-Frequency LLM Errors**:
  1. *Dimensional Error*: Omission of the 3.6 unit-conversion constant when converting Coulombic to gravimetric capacity ($\text{mAh}\cdot\text{g}^{-1}$).
  2. *Mechanism Overclaim*: Naive assignment of pseudocapacitive charge storage solely from a fitted $b$-value ($0.5 < b < 1.0$) without accounting for uncompensated resistance or verifying via operando spectroscopy.
  3. *Diffraction Hallucination*: Declaring single-phase purity based on matching 3 primary reflections of rutile $\text{TiO}_2$ while ignoring overlapping polymorphs (anatase/brookite) and unindexed reflections.
  4. *Precursor Hydration Drift*: Silently confusing reagent hydration state or coordination equivalents (e.g., hydrated salt $\text{FeSO}_4\cdot 7\text{H}_2\text{O}$ vs. anhydrous $\text{FeSO}_4$), resulting in an ~83% stoichiometric discrepancy and solute supersaturation drift.

---

## 📁 Repository Structure

```text
materials-ai-workflows/
├── run_examples.py                 # Core workflow demonstrations (Pymatgen, EIS, CV, GITT, GP, NEB)
├── evidence_retrieval.py           # Citation-backed primary literature retrieval module
├── evaluate_stem_cases.py          # Automated evaluation benchmark runner
├── scientific_evaluation_cases.json# 8 scientific evaluation prompts, rubrics, and error taxonomies
├── evaluation_results.json         # Benchmark audit log: tested responses, rubric scores & evaluator notes
├── research_evidence.json          # Curated literature ground-truth assertions
├── requirements.txt                # Direct dependencies
├── requirements-verified.txt       # Tested version pins
└── results/                        # Generated plots, CSV data, and verification logs
```

---

## 🚀 Quickstart

```bash
# Clone the repository
git clone https://github.com/xuexuennn-dev/materials-ai-workflows.git
cd materials-ai-workflows

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run all workflow demonstrations
python run_examples.py

# Run scientific AI evaluation audit
python evaluate_stem_cases.py
```

---

## 🛡️ Data Provenance & Boundary Clarification

- All electrochemical and experimental design datasets in `results/` are synthetic method-validation data generated to benchmark analytical code.
- Structural models and NEB pathways use standard benchmark systems to demonstrate script execution; no proprietary or unverified laboratory measurements are presented.
- Equivalent circuit representations are demonstrative; physical mechanism assignment requires independent multi-modal characterization.

---

## 👤 Maintainer

- **Maintainer**: [@xuexuennn-dev](https://github.com/xuexuennn-dev)
- **License**: MIT
