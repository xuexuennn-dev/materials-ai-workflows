"""AI-assisted materials workflow demonstrations. No private experimental data.

Run: python run_examples.py
Reference structures and synthetic data test software/methods; they are not
measurements of the user's battery project or evidence of experimental success.
"""
from pathlib import Path
import csv
import json
import importlib.metadata
import warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import norm, qmc, linregress
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
RESULTS = {'data_provenance': 'Reference structures and synthetic method-validation data only',
           'private_experimental_data_used': False, 'checks': {}}


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')


def save_table(name, header, data):
    with (OUT / name).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(data)


def structures_and_descriptors():
    from ase.build import bulk
    from ase.io import write
    from pymatgen.io.ase import AseAtomsAdaptor
    from pymatgen.analysis.diffraction.xrd import XRDCalculator
    from pymatgen.core import Composition
    from matminer.featurizers.composition import ElementProperty

    silicon = bulk('Si', 'diamond', a=5.431, cubic=True)
    structure = AseAtomsAdaptor.get_structure(silicon)
    structure.to(filename=str(OUT / 'reference_silicon.cif'))
    structure.to(filename=str(OUT / 'reference_silicon_POSCAR'), fmt='poscar')
    pattern = XRDCalculator(wavelength='CuKa').get_pattern(structure, two_theta_range=(10, 90))
    assert len(structure) == 8 and len(pattern.x) >= 3
    assert abs(float(pattern.x[0]) - 28.44) < 0.2
    save_table('reference_silicon_theoretical_diffraction.csv',
               ['two_theta_deg', 'relative_intensity', 'd_A', 'hkl_from_known_structure'],
               zip(pattern.x, pattern.y, pattern.d_hkls, map(str, pattern.hkls)))
    formulas = ['LiFePO4', 'FePO4', 'LiCoO2', 'TiO2', 'LiMn2O4', 'NaFePO4']
    featurizer = ElementProperty.from_preset('magpie')
    vectors = [featurizer.featurize(Composition(formula)) for formula in formulas]
    save_table('composition_descriptors.csv', ['formula'] + featurizer.feature_labels(),
               [[formula] + vector for formula, vector in zip(formulas, vectors)])
    assert np.isfinite(np.asarray(vectors, dtype=float)).all()
    with (OUT / 'qe_silicon_input_template.in').open('w') as handle:
        write(handle, silicon, format='espresso-in',
              pseudopotentials={'Si': 'Si.pbe-n-kjpaw_psl.1.0.0.UPF'},
              input_data={'control': {'calculation': 'scf', 'pseudo_dir': './pseudo'},
                          'system': {'ecutwfc': 50, 'ecutrho': 400},
                          'electrons': {'conv_thr': 1e-8}}, kpts=(4, 4, 4))
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.vlines(pattern.x, 0, pattern.y, color='#245a81', linewidth=2)
    ax.set(xlabel='2 theta (degrees)', ylabel='Relative intensity',
           title='Calculated silicon reference pattern | not experimental data')
    fig.tight_layout()
    fig.savefig(OUT / 'reference_silicon_theoretical_pattern.png', dpi=180)
    plt.close(fig)
    return {'status': 'passed', 'reference': 'Ideal diamond silicon, a = 5.431 A',
            'atoms': len(structure), 'first_peak_deg': float(pattern.x[0]),
            'composition_count': len(formulas), 'descriptor_count': len(vectors[0]),
            'qe_scope': 'Input preparation only; no DFT run or pseudopotential download'}


def electrochemistry():
    from impedance.models.circuits import CustomCircuit
    rng = np.random.default_rng(42)
    frequencies = np.logspace(5, -2, 100)
    actual = np.array([4.0, 80.0, 2.5e-4])
    omega = 2 * np.pi * frequencies
    clean = actual[0] + actual[1] / (1 + 1j * omega * actual[1] * actual[2])
    observations = clean + rng.normal(0, .08, len(clean)) + 1j * rng.normal(0, .08, len(clean))
    circuit = CustomCircuit(circuit='R0-p(R1,C1)', initial_guess=[3.0, 60.0, 1.5e-4])
    circuit.fit(frequencies, observations)
    prediction = circuit.predict(frequencies)
    relative_errors = abs((circuit.parameters_ - actual) / actual)
    rmse = float(np.sqrt(np.mean(abs(prediction - observations) ** 2)))
    assert float(max(relative_errors)) < .03 and rmse < .3
    save_table('synthetic_eis.csv', ['frequency_Hz', 'Zreal_ohm', 'Zimag_ohm', 'fit_real', 'fit_imag'],
               zip(frequencies, observations.real, observations.imag, prediction.real, prediction.imag))

    rates = np.array([.002, .005, .01, .02, .05, .1])
    k1, k2 = .8, .2
    currents = k1 * rates + k2 * np.sqrt(rates)
    fitted = linregress(np.sqrt(rates), currents / np.sqrt(rates))
    b_fit = linregress(np.log(rates), np.log(currents))
    assert abs(fitted.slope - k1) < 1e-10 and abs(fitted.intercept - k2) < 1e-10
    save_table('synthetic_cv_rate_decomposition.csv',
               ['scan_rate_V_per_s', 'current_A', 'capacitive_component_A', 'diffusion_component_A'],
               zip(rates, currents, k1 * rates, k2 * np.sqrt(rates)))
    # Planar, short-time approximation. This is an apparent diffusivity example.
    length_cm, pulse_seconds, delta_es, delta_et = .001, 600., .01, .08
    d_app = 4 * length_cm ** 2 / (np.pi * pulse_seconds) * (delta_es / delta_et) ** 2
    assert np.isfinite(d_app) and d_app > 0
    gitt = {'data_kind': 'synthetic parameters', 'length_cm': length_cm,
            'pulse_seconds': pulse_seconds, 'delta_Es_V': delta_es, 'delta_Et_V': delta_et,
            'apparent_D_cm2_per_s': d_app,
            'assumptions': 'Planar short-time diffusion, suitable voltage regime and pulse/rest response',
            'interpretation': 'Not proof of a mobile species or a conversion-reaction mechanism'}
    write_json('synthetic_gitt_example.json', gitt)

    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    axes[0].scatter(observations.real, -observations.imag, s=12, label='Synthetic data')
    axes[0].plot(prediction.real, -prediction.imag, color='#c4583b', label='Circuit fit')
    axes[0].set(xlabel="Z real (ohm)", ylabel='-Z imaginary (ohm)', title='EIS: equivalent-circuit inference')
    axes[0].legend(frameon=False)
    axes[1].plot(np.sqrt(rates), currents / np.sqrt(rates), 'o', label='Synthetic CV series')
    axes[1].plot(np.sqrt(rates), fitted.slope * np.sqrt(rates) + fitted.intercept, label='Rate decomposition')
    axes[1].set(xlabel='sqrt(scan rate)', ylabel='current / sqrt(scan rate)', title='CV: rate-dependent contributions')
    axes[1].legend(frameon=False)
    fig.suptitle('Method validation on synthetic data', fontsize=12)
    fig.tight_layout()
    fig.savefig(OUT / 'electrochemical_method_validation.png', dpi=180)
    plt.close(fig)
    return {'status': 'passed', 'data_kind': 'Synthetic EIS/CV/GITT inputs',
            'circuit': 'R0-p(R1,C1)', 'true_parameters': actual.tolist(),
            'fitted_parameters': circuit.parameters_.tolist(), 'complex_RMSE_ohm': rmse,
            'max_relative_parameter_error': float(max(relative_errors)),
            'recovered_cv_k1': fitted.slope, 'recovered_cv_k2': fitted.intercept,
            'effective_cv_b': b_fit.slope, 'gitt_apparent_D_cm2_per_s': d_app}


def experiment_recommendation():
    rng = np.random.default_rng(14)
    design_pool = qmc.LatinHypercube(2, seed=14).random(64)
    design = design_pool[design_pool.sum(axis=1) <= 1.45][:16]
    assert len(design) == 16 and np.all(design.sum(axis=1) <= 1.45)
    # Synthetic score surface. Its outputs are not experimental measurements.
    def response(x):
        return np.exp(-((x[:, 0] - .68) ** 2 / .065 + (x[:, 1] - .35) ** 2 / .09)) + .1 * np.sin(8 * x[:, 0])
    measured = response(design) + rng.normal(0, .012, len(design))
    kernel = ConstantKernel(1., (.1, 10.)) * Matern(length_scale=[.3, .3], nu=2.5) + WhiteKernel(.0002, (1e-6, .01))
    gp = GaussianProcessRegressor(kernel=kernel, normalize_y=True, random_state=14, n_restarts_optimizer=2)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        gp.fit(design, measured)
    grid = np.linspace(.02, .98, 45)
    a, b = np.meshgrid(grid, grid)
    candidates = np.c_[a.ravel(), b.ravel()]
    # Example feasibility constraint, expressed on normalized factors.
    feasible = candidates.sum(axis=1) <= 1.45
    candidates = candidates[feasible]
    mean, sd = gp.predict(candidates, return_std=True)
    improvement = mean - max(measured) - .01
    z = improvement / np.maximum(sd, 1e-12)
    ei = improvement * norm.cdf(z) + sd * norm.pdf(z)
    selected = np.argsort(ei)[-5:][::-1]
    save_table('synthetic_design_history.csv', ['factor_A_normalized', 'factor_B_normalized', 'synthetic_score'],
               zip(design[:, 0], design[:, 1], measured))
    save_table('next_experiment_candidates.csv', ['factor_A_normalized', 'factor_B_normalized',
               'predicted_score', 'posterior_standard_deviation', 'expected_improvement'],
               [[*candidates[i], mean[i], sd[i], ei[i]] for i in selected])
    assert np.isfinite(mean).all() and (sd > 0).all() and np.all(candidates[selected].sum(axis=1) <= 1.45)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    for ax, values, title in zip(axes, [mean, ei], ['Surrogate prediction', 'Expected improvement']):
        artist = ax.scatter(candidates[:, 0], candidates[:, 1], c=values, s=9, cmap='viridis')
        ax.scatter(design[:, 0], design[:, 1], facecolors='none', edgecolors='white', s=38, linewidths=1.2)
        ax.scatter(candidates[selected, 0], candidates[selected, 1], marker='x', color='#e3573a', s=60)
        ax.set(xlabel='Normalized factor A', ylabel='Normalized factor B', title=title)
        fig.colorbar(artist, ax=ax, shrink=.8)
    fig.suptitle('Constrained next-experiment ranking | synthetic response surface')
    fig.tight_layout()
    fig.savefig(OUT / 'bayesian_experiment_planning.png', dpi=180)
    plt.close(fig)
    return {'status': 'passed', 'data_kind': 'Synthetic function, not lab measurements',
            'initial_design_size': len(design), 'feasible_candidates': len(candidates),
            'recommendations': len(selected), 'best_next_candidate': candidates[selected[0]].tolist(),
            'model': str(gp.kernel_)}


def atomistic_path():
    from ase.build import bulk
    from ase.calculators.emt import EMT
    from ase.constraints import FixAtoms
    from ase.mep import NEB
    from ase.optimize import BFGS
    from ase.io import write
    lattice = bulk('Cu', 'fcc', a=3.61, cubic=True).repeat((2, 2, 2))
    vacancy_position = lattice.positions[0].copy()
    del lattice[0]
    distances = np.linalg.norm(lattice.positions - vacancy_position, axis=1)
    moving = int(np.argmin(distances))
    fixed = int(np.argmax(distances))
    initial = lattice.copy()
    final = lattice.copy()
    final.positions[moving] = vacancy_position
    for atoms in (initial, final):
        atoms.set_constraint(FixAtoms(indices=[fixed]))
        atoms.calc = EMT()
        BFGS(atoms, logfile=None).run(fmax=.04, steps=80)
    images = [initial] + [initial.copy() for _ in range(3)] + [final]
    for atoms in images:
        atoms.calc = EMT()
    neb = NEB(images, climb=True, method='improvedtangent')
    neb.interpolate(mic=True)
    converged = BFGS(neb, logfile=str(OUT / 'reference_copper_neb.log')).run(fmax=.08, steps=120)
    energies = np.array([atoms.get_potential_energy() for atoms in images])
    relative = energies - energies[0]
    write(OUT / 'reference_copper_neb.extxyz', images)
    save_table('reference_copper_neb_profile.csv', ['image_index', 'relative_energy_eV'], enumerate(relative))
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(np.arange(len(images)), relative, 'o-', color='#245a81')
    ax.set(xlabel='NEB image', ylabel='Relative energy (eV)', title='Copper vacancy reference path | classical EMT')
    fig.tight_layout()
    fig.savefig(OUT / 'reference_copper_neb.png', dpi=180)
    plt.close(fig)
    assert np.isfinite(energies).all()
    return {'status': 'passed' if converged else 'ran_not_converged',
            'system': '31-atom FCC copper vacancy reference cell', 'calculator': 'ASE EMT, not DFT or MLIP',
            'images': len(images), 'optimizer_converged': bool(converged),
            'reference_barrier_eV': float(max(relative)),
            'scope': 'Workflow demonstration; no claim about ion transport in the battery material'}


if __name__ == '__main__':
    for package in ['pymatgen', 'ase', 'matminer', 'impedance', 'scikit-learn', 'numpy', 'scipy']:
        try:
            RESULTS.setdefault('versions', {})[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            pass
    for name, function in [('materials_informatics', structures_and_descriptors),
                           ('electrochemical_analysis', electrochemistry),
                           ('bayesian_experiment_planning', experiment_recommendation),
                           ('atomistic_migration_workflow', atomistic_path)]:
        try:
            RESULTS['checks'][name] = function()
            print(name, json.dumps(RESULTS['checks'][name], ensure_ascii=False), flush=True)
        except Exception as error:
            RESULTS['checks'][name] = {'status': 'failed', 'error': repr(error)}
            print(name, repr(error), flush=True)
        write_json('verification.json', RESULTS)
    if any(item['status'] != 'passed' for item in RESULTS['checks'].values()):
        raise SystemExit(1)
