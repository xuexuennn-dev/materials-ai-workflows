"""
Curated Benchmark & Rubric Suite: Expert-Constructed Evaluation Cases Demonstrating Scientific AI Error Taxonomies
(人工构造的科学推理评测示例与多维评分细则)

Demonstrates how domain-specific rubrics systematically evaluate scientific reasoning
against peer-reviewed materials chemistry, electrochemistry, and crystallography principles.
All responses and scores are curated reference cases illustrating specific error taxonomies.
"""

import json
from pathlib import Path

CASES_FILE = Path(__file__).parent / "scientific_evaluation_cases.json"
OUTPUT_FILE = Path(__file__).parent / "evaluation_results.json"

def run_benchmarks():
    with open(CASES_FILE, "r", encoding="utf-8") as f:
        cases_data = json.load(f)

    rubric = cases_data["rubric"]
    
    # 8 curated benchmark cases demonstrating passing and failing/hallucinating responses
    audited_evaluations = [
        {
            "case_id": "capacity_units",
            "prompt": "Derive theoretical gravimetric capacity from electron count and molar mass. Explain every unit conversion.",
            "tested_model_response": "Theoretical capacity is Q = (n * F) / (3.6 * M) in mAh/g, where n is transferred electrons per formula unit, F = 96485.3 C/mol is Faraday's constant, M is the molar mass in g/mol, and the 3.6 factor converts Coulombs (A*s) to milliampere-hours (1 mAh = 3.6 C). Note that theoretical capacity represents the thermodynamic stoichiometric upper bound under a postulated redox equation and cannot be equated with reversible discharge capacity without experimental validation.",
            "rubric_scores": {
                "physical_and_chemical_validity": 2,
                "assumptions_and_uncertainty": 2,
                "evidence_grounding": 2,
                "reproducibility": 2
            },
            "total_score": 8,
            "max_score": 8,
            "verdict": "PASS (Canonical Reference)",
            "evaluator_audit_notes": "Flawless dimensional conversion (explicit 3.6 conversion factor); explicitly decouples stoichiometric theoretical limit from practical reversible cell capacity."
        },
        {
            "case_id": "cv_mechanism",
            "prompt": "An electrode has a CV power-law exponent between 0.5 and 1. Does that establish its ion-storage mechanism?",
            "tested_model_response": "Yes, b = 0.75 definitively proves that the electrode operates via a pseudocapacitive charge storage mechanism with fast surface kinetics.",
            "rubric_scores": {
                "physical_and_chemical_validity": 0,
                "assumptions_and_uncertainty": 0,
                "evidence_grounding": 0,
                "reproducibility": 1
            },
            "total_score": 1,
            "max_score": 8,
            "verdict": "FAIL (Handcrafted Error Taxonomy: Mechanism Overclaim)",
            "evaluator_audit_notes": "CRITICAL REASONING DRIFT: Over-interprets an intermediate b-value (0.5 < b < 1.0) as definitive proof of pseudocapacitance. Fails to account for ohmic resistance (IR drop), uncompensated solution resistance, porous electrode geometric effects, or slow ion diffusion in semi-infinite linear transport. Dunn's method deconvolution and independent operando structural confirmation are strictly required."
        },
        {
            "case_id": "eis_identifiability",
            "prompt": "An equivalent-circuit fit has a very low residual. Is the circuit therefore the unique physical model?",
            "tested_model_response": "No. Low numerical residual (chi-squared) indicates mathematical goodness-of-fit within the sampled frequency domain, but equivalent electrical circuits are notoriously non-unique (e.g., Voigt vs. Maxwell ladders, nested RC vs. transmission line models). Assigning physical processes (SEI resistance, charge transfer, solid-state diffusion) requires validating parameter physical plausibility, checking Kramers-Kronig consistency, and correlating parameters with temperature/potential dependence.",
            "rubric_scores": {
                "physical_and_chemical_validity": 2,
                "assumptions_and_uncertainty": 2,
                "evidence_grounding": 2,
                "reproducibility": 2
            },
            "total_score": 8,
            "max_score": 8,
            "verdict": "PASS (Canonical Reference)",
            "evaluator_audit_notes": "Correctly distinguishes mathematical optimization convergence from physical identifiability; highlights non-uniqueness and requirement for Kramers-Kronig transform validation."
        },
        {
            "case_id": "gitt_conversion_electrode",
            "prompt": "Assess the use of a short-time GITT diffusion expression during a conversion reaction with changing phases.",
            "tested_model_response": "Applying the classical Weppner-Huggins equation (D_app = (4/pi)*(V_m/(S*F))^2 * [I_0*(dE/d_delta)/(dE/dt^0.5)]^2) to a multi-phase conversion reaction violates the core assumptions of single-phase solid solution diffusion and invariant molar volume/contact area. The resulting value can only be reported as a lumped 'apparent diffusion metric' and cannot be interpreted as intrinsic chemical diffusivity of a single migrating ion species.",
            "rubric_scores": {
                "physical_and_chemical_validity": 2,
                "assumptions_and_uncertainty": 2,
                "evidence_grounding": 2,
                "reproducibility": 2
            },
            "total_score": 8,
            "max_score": 8,
            "verdict": "PASS (Canonical Reference)",
            "evaluator_audit_notes": "Penalizes naive application of Weppner-Huggins equation; correctly identifies phase boundary movement and volume expansion as confounding factors in conversion reactions."
        },
        {
            "case_id": "diffraction_provenance",
            "prompt": "A calculated pattern from an ideal structure resembles three experimental peaks. What has been established?",
            "tested_model_response": "We have synthesized phase-pure rutile titanium dioxide (TiO2), as evidenced by matching the three main diffraction peaks.",
            "rubric_scores": {
                "physical_and_chemical_validity": 0,
                "assumptions_and_uncertainty": 0,
                "evidence_grounding": 0,
                "reproducibility": 1
            },
            "total_score": 1,
            "max_score": 8,
            "verdict": "FAIL (Handcrafted Error Taxonomy: Unverified Phase Purity)",
            "evaluator_audit_notes": "CRITICAL FLAW: Claiming phase purity based on matching 3 reflections ignores peak overlapping from common polymorphic or secondary phases (e.g., anatase, brookite, sub-oxides) and unindexed reflections. Requires full Rietveld refinement, background modeling, and complementary EDX/XPS spectroscopy."
        },
        {
            "case_id": "dft_and_neb_scope",
            "prompt": "What is needed before a migration-barrier calculation can support a battery-mechanism conclusion?",
            "tested_model_response": "A reliable migration barrier requires: (1) fully relaxed initial and final endpoint structures with verified charge state and magnetic spin configurations, (2) converged climbing-image NEB images with forces < 0.05 eV/Å, (3) validated exchange-correlation functional (and Hubbard U / dispersion corrections if transition metals are present), and (4) validation that the atomistic path corresponds to the lowest-energy percolation network verified experimentally by activation energy measurements (Arrhenius plots). A classical empirical potential (like EMT) on a model metal cannot be substituted for DFT/MLIP barriers in complex ternary materials.",
            "rubric_scores": {
                "physical_and_chemical_validity": 2,
                "assumptions_and_uncertainty": 2,
                "evidence_grounding": 2,
                "reproducibility": 2
            },
            "total_score": 8,
            "max_score": 8,
            "verdict": "PASS (Canonical Reference)",
            "evaluator_audit_notes": "Accurately enumerates convergence thresholds, functional dependencies, and explicit warning against extrapolating empirical potentials to complex multivalent intercalation materials."
        },
        {
            "case_id": "bayesian_recommendation",
            "prompt": "A Gaussian-process model ranks a new synthesis condition first. How should the result be reported?",
            "tested_model_response": "The condition should be reported as the current model-predicted acquisition optimum (e.g. via Expected Improvement) under an active learning policy, accompanied by the epistemic standard deviation sigma(x). It must NOT be reported as confirmed synthesis yield until an actual physical laboratory experiment is synthesized and characterized.",
            "rubric_scores": {
                "physical_and_chemical_validity": 2,
                "assumptions_and_uncertainty": 2,
                "evidence_grounding": 2,
                "reproducibility": 2
            },
            "total_score": 8,
            "max_score": 8,
            "verdict": "PASS (Canonical Reference)",
            "evaluator_audit_notes": "Maintains strict boundary between probabilistic surrogate suggestion and physical ground truth; correctly reports acquisition uncertainty."
        },
        {
            "case_id": "literature_condition_transfer",
            "prompt": "Two papers use similar reagent names but different formulas and reaction conditions. Can their protocols be merged?",
            "tested_model_response": "No. Reagents with similar common names may have distinct degrees of hydration, coordination states, or oxidation states (e.g., iron(II) sulfate heptahydrate FeSO4·7H2O with molar mass 278.01 g/mol vs. anhydrous iron(II) sulfate FeSO4 with molar mass 151.91 g/mol). Merging their mass quantities or hydrothermal temperatures arbitrarily will cause an ~83% stoichiometric discrepancy, altering solute supersaturation and triggering parasitic secondary phase precipitation. Protocol adaptation requires stoichiometric re-calculation and thermodynamic phase diagram verification.",
            "rubric_scores": {
                "physical_and_chemical_validity": 2,
                "assumptions_and_uncertainty": 2,
                "evidence_grounding": 2,
                "reproducibility": 2
            },
            "total_score": 8,
            "max_score": 8,
            "verdict": "PASS (Canonical Reference)",
            "evaluator_audit_notes": "Highlights real-world precursor ambiguity (hydrated vs. anhydrous salts); emphasizes quantitative stoichiometric recalculation and thermodynamic re-equilibration."
        }
    ]

    summary = {
        "benchmark_title": "Curated Benchmark: Scientific AI Reasoning Rubrics & Error Taxonomies",
        "benchmark_type": "Expert-constructed reference evaluation dataset (人工构造的科学推理评测示例与多维评分细则)",
        "provenance_note": "Curated exemplar benchmark for rubric calibration and demonstration; does not represent automated live API polling of external proprietary models.",
        "rubric_definitions": rubric,
        "total_cases_audited": len(audited_evaluations),
        "canonical_pass_cases": sum(1 for c in audited_evaluations if "PASS" in c["verdict"]),
        "handcrafted_fail_taxonomies": sum(1 for c in audited_evaluations if "FAIL" in c["verdict"]),
        "audit_cases": audited_evaluations
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated curated benchmark: {len(audited_evaluations)} cases written to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_benchmarks()
