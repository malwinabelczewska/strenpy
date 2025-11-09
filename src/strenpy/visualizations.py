"""
Visualization tools for stress-strain curves.

Based on MIT course materials: "STRESS-STRAIN CURVES" by David Roylance, 2001.
"""

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


def plot_engineering_stress_strain(
    strain: NDArray[np.floating],
    stress: NDArray[np.floating],
    material_name: str = "Material",
    youngs_modulus: float | None = None,
    yield_point: tuple[float, float] | None = None,
    uts_point: tuple[float, float] | None = None,
    proportional_limit: tuple[float, float] | None = None,
    save_path: str | None = None,
) -> None:
    """Plot engineering stress-strain curve with key points annotated."""
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(strain, stress, "b-", linewidth=2.5, label=material_name)

    if youngs_modulus and len(strain) > 0:
        elastic_strain = np.linspace(0, min(0.01, max(strain) * 0.3), 50)
        elastic_stress = youngs_modulus * elastic_strain
        ax.plot(
            elastic_strain,
            elastic_stress,
            "g--",
            linewidth=1.5,
            label=f"Hooke's Law (E = {youngs_modulus / 1000:.0f} GPa)",
            alpha=0.7,
        )

    if proportional_limit:
        ax.plot(proportional_limit[0], proportional_limit[1], "go", markersize=8)
        ax.annotate(
            "Proportional\nLimit",
            xy=proportional_limit,
            xytext=(proportional_limit[0] + 0.02, proportional_limit[1] + 10),
            fontsize=10,
            arrowprops=dict(arrowstyle="->", color="green", lw=1.5),
        )

    if yield_point:
        ax.plot(yield_point[0], yield_point[1], "ro", markersize=9)
        ax.annotate(
            "Yield Stress σᵧ\n(0.2% offset)",
            xy=yield_point,
            xytext=(yield_point[0] + 0.03, yield_point[1] - 15),
            fontsize=10,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="red", lw=2),
        )

        if youngs_modulus:
            offset = 0.002
            offset_strain = np.linspace(
                offset, min(yield_point[0] * 1.5, max(strain) * 0.4), 50
            )
            offset_stress = youngs_modulus * (offset_strain - offset)
            ax.plot(
                offset_strain,
                offset_stress,
                "r--",
                linewidth=1.2,
                label="0.2% offset line",
                alpha=0.6,
            )

    if uts_point:
        ax.plot(uts_point[0], uts_point[1], "ks", markersize=10)
        ax.annotate(
            "UTS (σf)",
            xy=uts_point,
            xytext=(uts_point[0] - 0.05, uts_point[1] + 15),
            fontsize=10,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="black", lw=2),
        )

    ax.set_xlabel("Engineering Strain εₑ", fontsize=13, fontweight="bold")
    ax.set_ylabel("Engineering Stress σₑ (MPa)", fontsize=13, fontweight="bold")
    ax.set_title(
        f"Engineering Stress-Strain Curve: {material_name}",
        fontsize=14,
        fontweight="bold",
    )
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(fontsize=10, loc="best")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_engineering_vs_true(
    engineering_strain: NDArray[np.floating],
    engineering_stress: NDArray[np.floating],
    true_strain: NDArray[np.floating],
    true_stress: NDArray[np.floating],
    material_name: str = "Material",
    uts_idx: int | None = None,
    save_path: str | None = None,
) -> None:
    """Plot engineering vs true stress-strain curves on same axes."""
    fig, ax = plt.subplots(figsize=(11, 7))

    ax.plot(
        engineering_strain,
        engineering_stress,
        "b-",
        linewidth=2.5,
        label="Engineering (σₑ vs εₑ)",
    )
    ax.plot(true_strain, true_stress, "r-", linewidth=2.5, label="True (σₜ vs εₜ)")

    if uts_idx is not None:
        ax.plot(
            engineering_strain[uts_idx],
            engineering_stress[uts_idx],
            "bs",
            markersize=10,
            label="UTS on engineering curve",
        )
        ax.plot(
            true_strain[uts_idx],
            true_stress[uts_idx],
            "r^",
            markersize=10,
            label="Same point on true curve",
        )

        ax.arrow(
            engineering_strain[uts_idx],
            engineering_stress[uts_idx],
            true_strain[uts_idx] - engineering_strain[uts_idx],
            true_stress[uts_idx] - engineering_stress[uts_idx],
            head_width=0.01,
            head_length=5,
            fc="gray",
            ec="gray",
            linestyle="--",
            linewidth=1.5,
            alpha=0.6,
        )

    ax.set_xlabel("Strain (ε)", fontsize=13, fontweight="bold")
    ax.set_ylabel("Stress σ (MPa)", fontsize=13, fontweight="bold")
    ax.set_title(
        f"Engineering vs True Stress-Strain: {material_name}",
        fontsize=14,
        fontweight="bold",
    )
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(fontsize=10, loc="best")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_power_law(
    true_strain: NDArray[np.floating],
    true_stress: NDArray[np.floating],
    A: float,
    n: float,
    material_name: str = "Material",
    save_path: str | None = None,
) -> None:
    """Plot power-law fit on log-log axes."""
    fig, ax = plt.subplots(figsize=(10, 7))

    mask = (true_strain > 0) & (true_stress > 0)

    ax.loglog(
        true_strain[mask],
        true_stress[mask],
        "bo",
        markersize=6,
        alpha=0.6,
        label="Experimental data",
    )

    strain_fit = np.logspace(
        np.log10(true_strain[mask].min()), np.log10(true_strain[mask].max()), 100
    )
    stress_fit = A * (strain_fit**n)
    ax.loglog(
        strain_fit,
        stress_fit,
        "r-",
        linewidth=2.5,
        label=f"Power-law fit: σₜ = {A:.0f}·εₜ^{n:.3f}",
    )

    ax.set_xlabel("True Strain εₜ (log scale)", fontsize=13, fontweight="bold")
    ax.set_ylabel("True Stress σₜ (MPa, log scale)", fontsize=13, fontweight="bold")
    ax.set_title(
        f"Power-Law Representation: {material_name}", fontsize=14, fontweight="bold"
    )
    ax.grid(True, alpha=0.3, linestyle="--", which="both")
    ax.legend(fontsize=11, loc="best")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_strain_energy(
    strain: NDArray[np.floating],
    stress: NDArray[np.floating],
    yield_idx: int | None = None,
    material_name: str = "Material",
    save_path: str | None = None,
) -> None:
    """Plot strain energy visualization showing resilience and toughness."""
    fig, ax = plt.subplots(figsize=(10, 7))

    ax.plot(strain, stress, "b-", linewidth=2.5, label=material_name)

    if yield_idx:
        ax.fill_between(
            strain[: yield_idx + 1],
            0,
            stress[: yield_idx + 1],
            alpha=0.3,
            color="green",
            label="Modulus of Resilience",
        )
        ax.fill_between(
            strain[yield_idx:],
            0,
            stress[yield_idx:],
            alpha=0.3,
            color="orange",
            label="Additional energy to fracture",
        )
    else:
        ax.fill_between(
            strain, 0, stress, alpha=0.3, color="blue", label="Modulus of Toughness"
        )

    ax.set_xlabel("Engineering Strain εₑ", fontsize=13, fontweight="bold")
    ax.set_ylabel("Engineering Stress σₑ (MPa)", fontsize=13, fontweight="bold")
    ax.set_title(f"Strain Energy: {material_name}", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(fontsize=11, loc="best")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()


def plot_material_comparison(
    materials: dict[str, tuple[NDArray[np.floating], NDArray[np.floating]]],
    title: str = "Stress-Strain Comparison",
    save_path: str | None = None,
) -> None:
    """Plot multiple stress-strain curves on same axes for comparison."""
    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ["blue", "red", "green", "orange", "purple", "brown"]

    for idx, (material_name, (strain, stress)) in enumerate(materials.items()):
        color = colors[idx % len(colors)]
        ax.plot(strain, stress, color=color, linewidth=2.5, label=material_name)

    ax.set_xlabel("Engineering Strain εₑ", fontsize=13, fontweight="bold")
    ax.set_ylabel("Engineering Stress σₑ (MPa)", fontsize=13, fontweight="bold")
    ax.set_title(title, fontsize=15, fontweight="bold")
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(fontsize=12, loc="best")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")

    plt.show()
