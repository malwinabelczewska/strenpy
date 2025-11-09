# StrengPy - Strength of Materials

Python implementation of tensile test analysis based on MIT course materials.

## Overview

This project implements comprehensive stress-strain analysis from tensile
testing, based on the MIT Department of Materials Science and Engineering
course module ["STRESS-STRAIN CURVES" by David Roylance (August 23, 2001)](https://resources.saylor.org/wwwresources/archived/site/wp-content/uploads/2012/09/ME1022.2.4.pdf), [also in docs](docs/stress-strain-curves.pdf).

## What This Project Does

StrengPy performs complete tensile test analysis following MIT's engineering
curriculum, calculating material properties and generating professional
stress-strain diagrams. The implementation uses real experimental tensile test
data from copper alloys.

### Key Concepts from MIT Module

**Engineering Stress & Strain**:

```text
σₑ = P/A₀    (engineering stress)
εₑ = δ/L₀     (engineering strain)
```

- P = applied load
- A₀ = original cross-sectional area
- δ = displacement
- L₀ = original gauge length

**Hooke's Law** (elastic region):

```text
σₑ = E·εₑ
```

- E = Young's Modulus (material stiffness)

**0.2% Offset Yield Stress**:

```text
Used when material has no sharp yield point
Draw line of slope E from εₑ = 0.002
Intersection with curve = yield stress σᵧ
```

**True Stress & Strain** (accounts for changing cross-section):

```text
σₜ = σₑ(1 + εₑ)              (true stress)
εₜ = ln(1 + εₑ)              (logarithmic strain)
```

**Power-Law Plasticity** (ductile metals):

```text
σₜ = A·εₜⁿ
```

- n = strain hardening exponent (typically 0.02-0.5)
- Example: Copper has n ≈ 0.474

**Strain Energy**:

```text
U* = ∫σ dε   (area under stress-strain curve)
```

- **Modulus of Resilience**: Energy absorbed up to yield
  (elastic recovery)
- **Modulus of Toughness**: Total energy to fracture
  (impact resistance)

## Installation

Requires Python 3.13+.

### For Development (Recommended)

Uses [uv](https://docs.astral.sh/uv/) for dependency management and development tools.

Install uv if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then sync dependencies:

```bash
uv sync
```

This installs all dependencies including development tools (pytest, ty, ruff)
needed for running tests, type checking, and linting.

### For Running Only (Without uv)

If you just want to run the tool without development dependencies:

**Using pip:**

```bash
pip install .
```

**Using pipx (installs CLI tool globally):**

```bash
pipx install .
```

Note: Development tasks (tests, type checking, linting) require uv.
The non-uv installations only support running the CLI tool.

The package uses modern src-layout with CLI entry point.

## Usage

### Running the Demo

```bash
uv run strenpy
```

Or if installed:

```bash
strenpy
```

This performs complete analysis:

1. Parse original .lis files from `data/`
2. Calculate engineering strain from displacement (ε = δ/L₀, L₀=25mm)
3. Filter out post-failure negative stress values
4. Calculate all mechanical properties:
   - Young's modulus
   - 0.2% offset yield stress
   - Ultimate tensile strength (UTS)
   - True stress-strain relations
   - Power-law parameters (A, n)
   - Modulus of resilience
   - Modulus of toughness
5. Save processed data and visualizations to `output/`:
   - `cunisi_stress_strain.csv`, `cusn12_stress_strain.csv`,
     `cuni12al3_stress_strain.csv`
   - `figure_cunisi_engineering.png` - CuNiSi engineering stress-strain
   - `figure_cusn12_eng_vs_true.png` - CuSn12 engineering vs true
   - `figure_cusn12_power_law.png` - CuSn12 log-log power-law
   - `figure_strain_energy.png` - CuNi12Al3 resilience & toughness
   - `figure_comparison.png` - All three alloys compared

### Using as Library

The package can be imported and used programmatically.
See `src/strenpy/__init__.py` for available functions and
`src/strenpy/cli.py` for usage examples.

## Development

### Running Tests

```bash
uv run pytest
```

Tests cover:

- Engineering stress & strain calculations
- Young's modulus determination
- 0.2% offset yield stress method
- UTS calculation
- True stress & strain conversions
- Power-law fitting
- Strain energy, resilience, toughness

## Project Structure

Modern Python package using src-layout:

```text
strenpy/
├── src/
│   └── strenpy/
│       ├── __init__.py
│       ├── calculations.py      # All MIT formulas
│       ├── visualizations.py    # Creates stress-strain figures
│       ├── data_processing.py   # Parse .lis files
│       └── cli.py               # CLI entry point
├── tests/
│   └── test_calculations.py    # Calculation tests
├── docs/
│   └── stress-strain-curves.pdf # MIT source document
├── data/
│   ├── Tensile_C_08.lis         # CuNiSi original data
│   ├── Tensile_E_01.lis         # CuSn12 original data
│   └── Tensile_F_01.lis         # CuNi12Al3 original data
├── output/                      # Generated files (gitignored)
├── pyproject.toml               # Package config
└── README.md
```

## Materials Analyzed

The project analyzes real experimental tensile test data from three copper
alloys, obtained from a BAM 5.2 tensile testing system and published by
[KupferDigital](https://dataportal.material-digital.de/de/organization/about/kupferdigital),
a research data infrastructure for copper materials science. Original data
files are in `data/`:

- [`Tensile_C_08.lis`](https://dataportal.material-digital.de/de/dataset/kupferdigital_bam_tensile_c_08) (CuNiSi)
- [`Tensile_E_01.lis`](https://dataportal.material-digital.de/de/dataset/kupferdigital_bam_tensile_e_01) (CuSn12)
- [`Tensile_F_01.lis`](https://dataportal.material-digital.de/de/dataset/kupferdigital_bam_tensile_f_01) (CuNi12Al3)

The program parses these German-format .lis files, calculates engineering
strain from displacement measurements (ε = δ/L₀ with L₀=25mm), filters out
post-failure negative stress values, and saves processed data and
visualizations to `output/`.

### CuNiSi (Copper-Nickel-Silicon Alloy)

- Ultimate Tensile Strength: ~236 MPa
- Strain hardening exponent: n ≈ 0.275
- Very ductile: ~50% elongation
- Soft and ductile copper alloy
- Used for electrical connectors and springs

### CuSn12 (Bronze - Copper-Tin 12%)

- Ultimate Tensile Strength: ~410 MPa
- Strain hardening exponent: n ≈ 0.138
- Medium strength bronze
- ~30% elongation
- Traditional bronze alloy used in bearings and marine applications

### CuNi12Al3 (Copper-Nickel-Aluminum Alloy)

- Ultimate Tensile Strength: ~637 MPa
- Strain hardening exponent: n ≈ 0.086
- High strength copper alloy
- ~20% elongation
- Used in marine engineering and high-strength applications

The original .lis files contain time-series measurements of displacement
(Weg), force (Kraft), and stress (Spannung). The program calculates
engineering strain from displacement using the gauge length (25mm) and
filters out post-failure negative stress values.

## Understanding the MIT Analysis

### Stress-Strain Curve Regions

1. **Elastic Region**: Linear, follows Hooke's Law (σₑ = E·εₑ)
2. **Proportional Limit**: End of linear behavior
3. **Yield Point**: Onset of permanent (plastic) deformation
4. **Strain Hardening**: Material strengthens with deformation
5. **UTS**: Maximum engineering stress, necking begins
6. **Necking**: Localized thinning, true stress continues rising
7. **Fracture**: Complete failure

### Why True Stress Differs from Engineering Stress

Engineering stress uses original area (A₀), but material actually thins during
stretching. True stress accounts for this:

- σₜ = P/A (actual area)
- True stress keeps rising even when engineering stress falls
- At UTS: -dA/A = dσₜ/σₜ (necking criterion)

### Power-Law Plasticity

Ductile metals follow: σₜ = A·εₜⁿ

- **n value** indicates strain hardening rate
- Higher n = better resistance to necking
- Copper n=0.474 is typical for ductile metals
- Can be determined from log-log plot

### Strain Energy & Toughness

- **Resilience**: Elastic energy storage (springs, bows)
- **Toughness**: Impact resistance (crash protection)
- Natural materials (wood, tendon) excel at energy absorption per
  weight

## Educational Background

This implementation follows:

- MIT Course 3.11: Mechanics of Materials
- First-year graduate materials science
- ASTM standards: E8 (metals), D638 (plastics), D3039 (composites)

All formulas, notation, and concepts match the MIT module exactly.

## Visualizations Generated

Creates stress-strain analysis figures following MIT course module methodology:

1. **Engineering stress-strain curves**: Full tensile test curves showing
   elastic and plastic regions
2. **Engineering vs true stress-strain**: Overlay comparing engineering and
   true stress-strain relationships
3. **Power-law log-log plot**: Logarithmic plot for determining strain
   hardening exponent (n)
4. **Strain energy visualization**: Resilience and toughness areas under curves
5. **Material comparison**: Three copper alloys compared on single plot

## Reference

**Primary Source**:  
Roylance, D. (2001). "STRESS-STRAIN CURVES"  
Department of Materials Science and Engineering  
Massachusetts Institute of Technology  
Cambridge, MA 02139  
August 23, 2001

Available in: `docs/ss.pdf`

**Topics Covered**:

- Engineering vs true stress-strain curves
- Hooke's Law and Young's modulus
- Proportional limit, elastic limit, yield stress
- 0.2% offset yield stress method
- Ultimate tensile strength and necking
- Cup-and-cone fracture in metals
- Drawing in semicrystalline polymers
- Power-law plasticity (σₜ = A·εₜⁿ)
- Considère construction
- Strain energy, modulus of resilience, modulus of toughness
- Compression testing and hysteresis

**ASTM Standards Referenced**:

- ASTM E8: Tension testing of metallic materials
- ASTM D638: Tensile properties of plastics
- ASTM D3039: Tensile properties of polymer matrix composite
  materials

## License

MIT
