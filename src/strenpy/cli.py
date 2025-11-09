"""
Tensile test analysis CLI.

Analyzes three copper alloys using real experimental data from KupferDigital.
"""

import numpy as np
from pathlib import Path
from numpy.typing import NDArray
from rich import print

from strenpy import (
    calculate_youngs_modulus,
    calculate_offset_yield_stress,
    calculate_uts,
    calculate_true_stress,
    calculate_true_strain,
    fit_power_law,
    calculate_modulus_of_resilience,
    calculate_modulus_of_toughness,
    plot_engineering_stress_strain,
    plot_engineering_vs_true,
    plot_power_law,
    plot_strain_energy,
    plot_material_comparison,
)
from strenpy.data_processing import (
    load_cunisi_data,
    load_cusn12_data,
    load_cuni12al3_data,
)


def analyze_material(
    name: str,
    strain_e: NDArray,
    stress_e: NDArray,
) -> dict:
    """Perform complete tensile test analysis and return all calculated properties."""

    E = calculate_youngs_modulus(stress_e, strain_e, elastic_points=30)

    yield_stress, yield_strain = calculate_offset_yield_stress(
        stress_e, strain_e, E, offset=0.002
    )

    uts_value, uts_idx = calculate_uts(stress_e)
    uts_strain = strain_e[uts_idx]

    strain_t = calculate_true_strain(strain_e[:uts_idx])
    stress_t = calculate_true_stress(stress_e[:uts_idx], strain_e[:uts_idx])

    try:
        A, n = fit_power_law(stress_t, strain_t, start_idx=10, end_idx=uts_idx - 10)
    except Exception:
        A, n = 0, 0

    yield_idx = int(np.argmin(np.abs(strain_e - yield_strain)))
    resilience = calculate_modulus_of_resilience(stress_e, strain_e, yield_idx)
    toughness = calculate_modulus_of_toughness(stress_e, strain_e)

    return {
        "name": name,
        "strain_e": strain_e,
        "stress_e": stress_e,
        "strain_t": strain_t,
        "stress_t": stress_t,
        "E": E,
        "yield_stress": yield_stress,
        "yield_strain": yield_strain,
        "yield_idx": yield_idx,
        "uts": uts_value,
        "uts_strain": uts_strain,
        "uts_idx": uts_idx,
        "A": A,
        "n": n,
        "resilience": resilience,
        "toughness": toughness,
        "fracture_strain": strain_e[-1],
    }


def load_real_alloy_data() -> tuple:
    print("LOADING TENSILE TEST DATA...")
    print("-" * 90)

    cunisi_strain, cunisi_stress = load_cunisi_data()
    cusn12_strain, cusn12_stress = load_cusn12_data()
    cuni12al3_strain, cuni12al3_stress = load_cuni12al3_data()

    print("  ✓ CuNiSi - soft & ductile")
    print("  ✓ CuSn12 - medium strength")
    print("  ✓ CuNi12Al3 - high strength")
    print()

    return (
        cunisi_strain,
        cunisi_stress,
        cusn12_strain,
        cusn12_stress,
        cuni12al3_strain,
        cuni12al3_stress,
    )


def main():
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    print("=" * 90)
    print(" " * 25 + "COPPER ALLOY ANALYSIS")
    print("=" * 90)
    print()
    print(f"Output directory: {output_dir.absolute()}")
    print()

    (
        cunisi_strain,
        cunisi_stress,
        cusn12_strain,
        cusn12_stress,
        cuni12al3_strain,
        cuni12al3_stress,
    ) = load_real_alloy_data()

    print("ANALYZING CuNiSi (Copper-Nickel-Silicon)")
    print("-" * 90)
    cu1 = analyze_material("CuNiSi", cunisi_strain, cunisi_stress)

    print(f"  Young's Modulus E:                {cu1['E'] / 1000:.0f} GPa")
    print(f"  Yield Stress σᵧ (0.2% offset):    {cu1['yield_stress']:.1f} MPa")
    print(f"  Ultimate Tensile Strength σf:     {cu1['uts']:.1f} MPa")
    print(f"  Strain at UTS:                    {cu1['uts_strain'] * 100:.1f}%")
    print(f"  Fracture strain:                  {cu1['fracture_strain'] * 100:.1f}%")
    if cu1["n"] > 0:
        print(f"  Power-law: σₜ = {cu1['A']:.0f}·εₜ^{cu1['n']:.3f}")
    print(f"  Modulus of Resilience:            {cu1['resilience']:.2f} MJ/m³")
    print(f"  Modulus of Toughness:             {cu1['toughness']:.1f} MJ/m³")
    print()

    print("ANALYZING CuSn12 (Bronze - 12% Tin)")
    print("-" * 90)
    cu2 = analyze_material("CuSn12", cusn12_strain, cusn12_stress)

    print(f"  Young's Modulus E:                {cu2['E'] / 1000:.0f} GPa")
    print(f"  Yield Stress σᵧ (0.2% offset):    {cu2['yield_stress']:.1f} MPa")
    print(f"  Ultimate Tensile Strength σf:     {cu2['uts']:.1f} MPa")
    print(f"  Strain at UTS:                    {cu2['uts_strain'] * 100:.1f}%")
    print(f"  Fracture strain:                  {cu2['fracture_strain'] * 100:.1f}%")
    if cu2["n"] > 0:
        print(f"  Power-law: σₜ = {cu2['A']:.0f}·εₜ^{cu2['n']:.3f}")
    print(f"  Modulus of Resilience:            {cu2['resilience']:.2f} MJ/m³")
    print(f"  Modulus of Toughness:             {cu2['toughness']:.1f} MJ/m³")
    print()

    print("ANALYZING CuNi12Al3 (Copper-Nickel-Aluminum)")
    print("-" * 90)
    cu3 = analyze_material("CuNi12Al3", cuni12al3_strain, cuni12al3_stress)

    print(f"  Young's Modulus E:                {cu3['E'] / 1000:.0f} GPa")
    print(f"  Yield Stress σᵧ (0.2% offset):    {cu3['yield_stress']:.1f} MPa")
    print(f"  Ultimate Tensile Strength σf:     {cu3['uts']:.1f} MPa")
    print(f"  Strain at UTS:                    {cu3['uts_strain'] * 100:.1f}%")
    print(f"  Fracture strain:                  {cu3['fracture_strain'] * 100:.1f}%")
    if cu3["n"] > 0:
        print(f"  Power-law: σₜ = {cu3['A']:.0f}·εₜ^{cu3['n']:.3f}")
    print(f"  Modulus of Resilience:            {cu3['resilience']:.2f} MJ/m³")
    print(f"  Modulus of Toughness:             {cu3['toughness']:.1f} MJ/m³")
    print()

    print("SAVING PROCESSED DATA...")
    print("-" * 90)
    np.savetxt(
        output_dir / "cunisi_stress_strain.csv",
        np.column_stack([cu1["strain_e"], cu1["stress_e"]]),
        delimiter=",",
        header="strain_e,stress_e_MPa",
        comments="",
    )
    np.savetxt(
        output_dir / "cusn12_stress_strain.csv",
        np.column_stack([cu2["strain_e"], cu2["stress_e"]]),
        delimiter=",",
        header="strain_e,stress_e_MPa",
        comments="",
    )
    np.savetxt(
        output_dir / "cuni12al3_stress_strain.csv",
        np.column_stack([cu3["strain_e"], cu3["stress_e"]]),
        delimiter=",",
        header="strain_e,stress_e_MPa",
        comments="",
    )
    print("  ✓ cunisi_stress_strain.csv")
    print("  ✓ cusn12_stress_strain.csv")
    print("  ✓ cuni12al3_stress_strain.csv")
    print()

    print("GENERATING VISUALIZATIONS...")
    print("-" * 90)

    print("  [1/5] Engineering stress-strain for CuNiSi...")
    plot_engineering_stress_strain(
        cu1["strain_e"],
        cu1["stress_e"],
        material_name="CuNiSi (Copper-Nickel-Silicon)",
        youngs_modulus=cu1["E"],
        yield_point=(cu1["yield_strain"], cu1["yield_stress"]),
        uts_point=(cu1["uts_strain"], cu1["uts"]),
        save_path=str(output_dir / "figure_cunisi_engineering.png"),
    )

    print("  [2/5] Engineering vs True stress-strain for CuSn12...")
    plot_engineering_vs_true(
        cu2["strain_e"][: cu2["uts_idx"]],
        cu2["stress_e"][: cu2["uts_idx"]],
        cu2["strain_t"],
        cu2["stress_t"],
        material_name="CuSn12 Bronze",
        uts_idx=None,
        save_path=str(output_dir / "figure_cusn12_eng_vs_true.png"),
    )

    if cu2["n"] > 0:
        print("  [3/5] Power-law representation for CuSn12...")
        plot_power_law(
            cu2["strain_t"],
            cu2["stress_t"],
            cu2["A"],
            cu2["n"],
            material_name="CuSn12 Bronze",
            save_path=str(output_dir / "figure_cusn12_power_law.png"),
        )

    print("  [4/5] Strain energy for CuNi12Al3...")
    plot_strain_energy(
        cu3["strain_e"],
        cu3["stress_e"],
        yield_idx=cu3["yield_idx"],
        material_name="CuNi12Al3",
        save_path=str(output_dir / "figure_strain_energy.png"),
    )

    print("  [5/5] Material comparison...")
    materials = {
        "CuNiSi (soft)": (cu1["strain_e"], cu1["stress_e"]),
        "CuSn12 (medium)": (cu2["strain_e"], cu2["stress_e"]),
        "CuNi12Al3 (strong)": (cu3["strain_e"], cu3["stress_e"]),
    }
    plot_material_comparison(
        materials,
        title="Copper Alloy Comparison: Soft vs Medium vs Strong",
        save_path=str(output_dir / "figure_comparison.png"),
    )

    print()
    print("=" * 90)
    print("ANALYSIS COMPLETE!")
    print("=" * 90)
    print()
    print("Generated figures in output/:")
    print("  • figure_cunisi_engineering.png")
    print("  • figure_cusn12_eng_vs_true.png")
    print("  • figure_cusn12_power_law.png")
    print("  • figure_strain_energy.png")
    print("  • figure_comparison.png")
    print()


if __name__ == "__main__":
    main()
