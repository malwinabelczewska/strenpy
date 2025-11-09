"""
Strength of Materials - Tensile test analysis based on MIT course materials.

Reference:
Roylance, D. (2001). "STRESS-STRAIN CURVES"
Department of Materials Science and Engineering
Massachusetts Institute of Technology
August 23, 2001
"""

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
    calculate_necking_strain_from_n,
)
from strenpy.visualizations import (
    plot_engineering_stress_strain,
    plot_engineering_vs_true,
    plot_power_law,
    plot_strain_energy,
    plot_material_comparison,
)

__all__ = [
    "calculate_cross_sectional_area",
    "calculate_engineering_strain",
    "calculate_engineering_stress",
    "calculate_youngs_modulus",
    "calculate_offset_yield_stress",
    "calculate_uts",
    "calculate_true_stress",
    "calculate_true_strain",
    "fit_power_law",
    "calculate_strain_energy",
    "calculate_modulus_of_resilience",
    "calculate_modulus_of_toughness",
    "calculate_necking_strain_from_n",
    "plot_engineering_stress_strain",
    "plot_engineering_vs_true",
    "plot_power_law",
    "plot_strain_energy",
    "plot_material_comparison",
]
