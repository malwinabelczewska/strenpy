"""
Tests for MIT stress-strain calculations.
"""

import numpy as np
from strenpy.calculations import (
    calculate_cross_sectional_area,
    calculate_engineering_strain,
    calculate_engineering_stress,
    calculate_youngs_modulus,
    calculate_offset_yield_stress,
    calculate_uts,
    calculate_true_stress,
    calculate_true_strain,
    fit_power_law,
    calculate_strain_energy,
    calculate_modulus_of_resilience,
    calculate_modulus_of_toughness,
)


def test_calculate_cross_sectional_area():
    diameter = 10.0
    area = calculate_cross_sectional_area(diameter)
    expected = np.pi * 25.0
    assert np.isclose(area, expected)
    assert np.isclose(area, 78.539816, atol=0.001)


def test_calculate_engineering_strain():
    original_length = 50.0
    displacement = np.array([0.0, 1.0, 2.5, 5.0])
    strain = calculate_engineering_strain(displacement, original_length)

    expected = np.array([0.0, 0.02, 0.05, 0.10])
    assert np.allclose(strain, expected)


def test_calculate_engineering_stress():
    load = np.array([1000.0, 2000.0, 5000.0])
    area = 78.54
    stress = calculate_engineering_stress(load, area)

    expected = np.array([12.732, 25.465, 63.662])
    assert np.allclose(stress, expected, atol=0.01)


def test_calculate_youngs_modulus():
    strain = np.linspace(0, 0.005, 50)
    youngs_modulus = 120000
    stress = youngs_modulus * strain

    calculated_E = calculate_youngs_modulus(stress, strain, elastic_points=40)
    assert np.isclose(calculated_E, youngs_modulus, rtol=0.01)


def test_calculate_offset_yield_stress():
    strain = np.linspace(0, 0.05, 100)
    youngs_modulus = 70000

    stress = np.zeros_like(strain)
    for i, s in enumerate(strain):
        if s < 0.001:
            stress[i] = youngs_modulus * s
        else:
            stress[i] = youngs_modulus * 0.001 + 15000 * (s - 0.001)

    yield_stress, yield_strain = calculate_offset_yield_stress(
        stress, strain, youngs_modulus, offset=0.002
    )

    assert yield_stress > 0
    assert yield_strain >= 0.002


def test_calculate_uts():
    stress = np.array([100, 200, 300, 400, 500, 450, 400, 350])
    uts_value, uts_idx = calculate_uts(stress)

    assert uts_value == 500
    assert uts_idx == 4


def test_calculate_true_stress():
    engineering_stress = np.array([100.0, 200.0, 300.0])
    engineering_strain = np.array([0.0, 0.1, 0.2])

    true_stress = calculate_true_stress(engineering_stress, engineering_strain)

    expected = np.array([100.0, 220.0, 360.0])
    assert np.allclose(true_stress, expected)


def test_calculate_true_strain():
    engineering_strain = np.array([0.0, 0.1, 0.5, 1.0])
    true_strain = calculate_true_strain(engineering_strain)

    expected = np.array([0.0, 0.09531, 0.40547, 0.69315])
    assert np.allclose(true_strain, expected, atol=0.001)


def test_fit_power_law():
    true_strain = np.linspace(0.01, 0.3, 50)
    n_expected = 0.474
    A_expected = 500
    true_stress = A_expected * (true_strain**n_expected)

    A_fit, n_fit = fit_power_law(true_stress, true_strain)

    assert np.isclose(A_fit, A_expected, rtol=0.05)
    assert np.isclose(n_fit, n_expected, rtol=0.05)


def test_calculate_strain_energy():
    strain = np.array([0.0, 0.01, 0.02, 0.03])
    stress = np.array([0.0, 100.0, 200.0, 300.0])

    energy = calculate_strain_energy(stress, strain)

    expected = np.trapezoid(stress, strain)
    assert np.isclose(energy, expected)
    assert energy > 0


def test_calculate_modulus_of_resilience():
    strain = np.linspace(0, 0.05, 100)
    stress = 100000 * strain
    stress[20:] = stress[19]

    resilience = calculate_modulus_of_resilience(stress, strain, yield_idx=19)

    assert resilience > 0
    assert resilience < calculate_strain_energy(stress, strain)


def test_calculate_modulus_of_toughness():
    strain = np.linspace(0, 0.5, 100)
    stress = np.linspace(0, 400, 100)

    toughness = calculate_modulus_of_toughness(stress, strain)

    assert toughness > 0
