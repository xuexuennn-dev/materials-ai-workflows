# Materials research workflows with AI assistance

This portfolio demonstrates materials informatics, quantitative electrochemical analysis,
uncertainty-aware experimental planning and atomistic workflow automation.
Codex prepared the code with AI assistance. The owner should review the methods and
practice explaining the inputs, assumptions and interpretation before presenting the work.

## Run

Python 3.11 or newer is recommended. Install requirements in an isolated environment:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-verified.txt
.venv\Scripts\python run_examples.py
```

The script writes figures, data tables, structure files and an execution record to `results/`.
`verification.json` records actual package versions and each check's result.
The supplied version pins were executed on Windows with Python 3.13.
The broader `requirements.txt` lists the direct dependencies without pins.

Run `python evidence_retrieval.py --query "electrochemical impedance fitting"` for a small
local citation-backed retrieval component. Its input records are AI-prepared summaries of
linked primary descriptions/abstracts. It does not automatically extract full papers.
`scientific_evaluation_cases.json` contains eight draft cases and a common scientific rubric.

## Demonstrations

1. **Materials informatics**: pymatgen/ASE structure interoperability, CIF/POSCAR export,
   theoretical diffraction from a known silicon structure, and matminer composition descriptors.
   The Quantum ESPRESSO file demonstrates input preparation. It requires an appropriate
   pseudopotential and a DFT engine before it can produce a DFT result.
2. **Electrochemical analysis**: impedance.py circuit fitting with parameter-recovery checks,
   CV rate decomposition, and a GITT apparent-diffusivity calculation with explicit assumptions.
3. **Experimental planning**: space-filling initial design, a Gaussian-process surrogate,
   uncertainty estimates, expected improvement and constrained candidate ranking.
4. **Atomistic workflows**: an ASE climbing-image NEB calculation on a copper vacancy
   reference system using the classical EMT calculator. This is not a DFT/MLIP calculation.

## Data provenance

All electrochemical and optimization data are synthetic method-validation data.
The structure examples are reference models. No private battery measurements,
unresolved experimental diffraction patterns or claims of phase-pure synthesis are included.
The new theoretical diffraction figure represents silicon and is explicitly labelled.

## Interpretation

An executable workflow demonstrates tool use. A research conclusion additionally requires
appropriate experimental data, physical assumptions, convergence/fit assessment and domain review.
EIS circuits can be non-unique. GITT estimates require a suitable transport regime and do not
identify the mobile species. The copper EMT migration result does not establish a barrier in
the owner's battery system.

## Upstream projects

- pymatgen: https://github.com/materialsproject/pymatgen
- ASE: https://gitlab.com/ase/ase
- matminer: https://github.com/hackingmaterials/matminer
- impedance.py: https://github.com/ECSHackWeek/impedance.py
- scikit-learn: https://github.com/scikit-learn/scikit-learn

The code imports these libraries; it does not reproduce their implementations or claim
authorship of them. Their respective licenses apply to the installed libraries.
