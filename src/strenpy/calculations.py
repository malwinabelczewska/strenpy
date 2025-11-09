"""
Core calculations for tensile testing.

Reference: Roylance, D. (2001). "STRESS-STRAIN CURVES"
MIT Department of Materials Science and Engineering
"""

import numpy as np
from numpy.typing import NDArray


def calculate_cross_sectional_area(diameter: float) -> float:
    return np.pi * (diameter / 2) ** 2


def calculate_engineering_strain(
    displacement: NDArray[np.floating], original_length: float
) -> NDArray[np.floating]:
    return displacement / original_length


def calculate_engineering_stress(
    load: NDArray[np.floating], original_area: float
) -> NDArray[np.floating]:
    return load / original_area


def calculate_youngs_modulus(
    stress: NDArray[np.floating], strain: NDArray[np.floating], elastic_points: int = 20
) -> float:
    """Calculate Young's Modulus from linear elastic region."""
    coeffs = np.polyfit(strain[:elastic_points], stress[:elastic_points], 1)
    return coeffs[0]


def calculate_offset_yield_stress(
    stress: NDArray[np.floating],
    strain: NDArray[np.floating],
    youngs_modulus: float,
    offset: float = 0.002,
) -> tuple[float, float]:
    """
    Calculate offset yield stress by finding intersection of stress-strain curve
    with a line of slope E offset by the specified strain (default 0.2%).
    """
    offset_line_stress = youngs_modulus * (strain - offset)

    for i in range(len(stress) - 1):
        if offset_line_stress[i] >= 0 and stress[i] >= offset_line_stress[i]:
            return stress[i], strain[i]

    return stress[-1], strain[-1]


def calculate_uts(stress: NDArray[np.floating]) -> tuple[float, int]:
    """Find maximum engineering stress (UTS) and its index."""
    idx = np.argmax(stress)
    return float(stress[idx]), int(idx)


def calculate_true_stress(
    engineering_stress: NDArray[np.floating], engineering_strain: NDArray[np.floating]
) -> NDArray[np.floating]:
    """Convert engineering stress to true stress. Valid only up to necking."""
    return engineering_stress * (1 + engineering_strain)


def calculate_true_strain(
    engineering_strain: NDArray[np.floating],
) -> NDArray[np.floating]:
    return np.log(1 + engineering_strain)


def fit_power_law(
    true_stress: NDArray[np.floating],
    true_strain: NDArray[np.floating],
    start_idx: int = 0,
    end_idx: int | None = None,
) -> tuple[float, float]:
    """Fit power-law σₜ = A·εₜⁿ to true stress-strain data in plastic region."""
    if end_idx is None:
        end_idx = len(true_stress)

    mask = (true_strain[start_idx:end_idx] > 0) & (true_stress[start_idx:end_idx] > 0)
    log_strain = np.log(true_strain[start_idx:end_idx][mask])
    log_stress = np.log(true_stress[start_idx:end_idx][mask])

    coeffs = np.polyfit(log_strain, log_stress, 1)
    n = coeffs[0]
    log_A = coeffs[1]
    A = np.exp(log_A)

    return A, n


def calculate_strain_energy(
    stress: NDArray[np.floating], strain: NDArray[np.floating]
) -> float:
    """Calculate strain energy as area under stress-strain curve."""
    return np.trapezoid(stress, strain)


def calculate_modulus_of_resilience(
    stress: NDArray[np.floating], strain: NDArray[np.floating], yield_idx: int
) -> float:
    """Calculate strain energy up to yield (elastic energy storage capacity)."""
    return np.trapezoid(stress[: yield_idx + 1], strain[: yield_idx + 1])


def calculate_modulus_of_toughness(
    stress: NDArray[np.floating], strain: NDArray[np.floating]
) -> float:
    """Calculate total strain energy to fracture (impact resistance)."""
    return np.trapezoid(stress, strain)


def calculate_necking_strain_from_n(n: float) -> float:
    return n
