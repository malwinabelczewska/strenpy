"""
Process tensile test data from German .lis files.

Data source: BAM 5.2 tensile testing system via KupferDigital.
"""

import numpy as np
from pathlib import Path
from numpy.typing import NDArray


DATA_DIR = Path(__file__).parent.parent.parent / "data"


def parse_lis_file(
    filepath: Path, gauge_length_mm: float = 25.0
) -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    """
    Parse German .lis file: calculate strain from displacement, filter negative stress.
    """
    with open(filepath, "r", encoding="latin-1") as f:
        lines = f.readlines()

    data_start = None
    for i, line in enumerate(lines):
        if "[Daten]" in line:
            data_start = i + 3
            break

    if data_start is None:
        raise ValueError(f"Could not find [Daten] section in {filepath}")

    displacement_data = []
    stress_data = []

    for line in lines[data_start:]:
        line = line.strip()
        if not line:
            continue

        parts = line.replace(",", ".").split("\t")
        if len(parts) >= 5:
            try:
                displacement_mm = float(parts[1])
                stress_mpa = float(parts[4])

                if stress_mpa >= 0:
                    displacement_data.append(displacement_mm)
                    stress_data.append(stress_mpa)
            except (ValueError, IndexError):
                continue

    displacement = np.array(displacement_data)
    stress = np.array(stress_data)
    strain = displacement / gauge_length_mm

    return strain, stress


def load_cunisi_data() -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    filepath = DATA_DIR / "Tensile_C_08.lis"
    return parse_lis_file(filepath)


def load_cusn12_data() -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    filepath = DATA_DIR / "Tensile_E_01.lis"
    return parse_lis_file(filepath)


def load_cuni12al3_data() -> tuple[NDArray[np.floating], NDArray[np.floating]]:
    filepath = DATA_DIR / "Tensile_F_01.lis"
    return parse_lis_file(filepath)
