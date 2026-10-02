# IGHV4-34 Isotype Comparison: Naive vs. Class-Switched AVY Retention in SLE

A follow-up bioinformatics project examining whether the self-reactive
"AVY" motif in IGHV4-34 is corrected (mutated away) as B cells mature
from naive to class-switched status, in a real SLE patient.

This builds directly on an earlier project,
[ighv4-34-avy-motif](https://github.com/ArdalanLab/ighv4-34-avy-motif),
which first identified that a majority of bulk IGHV4-34-using sequences
in this patient retained an intact AVY motif.

## Background

IGHV4-34 is a human antibody heavy-chain V-gene segment carrying an
intrinsic self-reactive motif ("AVY") in its framework region 1 (FR1).
Normal B-cell tolerance mechanisms are expected to either eliminate
self-reactive B cells or drive them to mutate away from this motif as
they mature and undergo selection.

B cells can be grouped by antibody isotype, which reflects maturation
stage:

- **IGHM (IgM)** — the default, naive isotype; present before a B cell
  has undergone class-switching or significant selection.
- **IGHG (IgG)** — a class-switched isotype; B cells only reach this
  stage after class-switch recombination and (typically) affinity
  maturation in a germinal center, meaning they have been through
  real selection pressure.

**Question:** does the proportion of IGHV4-34 sequences retaining an
intact AVY motif drop from IGHM to IGHG, as would be expected if
tolerance/selection is actively correcting this self-reactive feature
during maturation?

## Data source

Real SLE patient B-cell receptor sequences from the
[Observed Antibody Space (OAS)](http://opig.stats.ox.ac.uk/webapps/oas)
database — Tipton et al. 2015 dataset, Subject-SLE1, heavy chain,
isotype-specific files (IGHM and IGHG).

## Pipeline

`scripts/compare_isotypes.py`:
1. Loads the IGHM and IGHG sequence files separately
2. Filters each for sequences using the IGHV4-34 V-gene
3. Checks whether each sequence's FR1 region retains the AVY motif
   intact or shows a mutation at that position
4. Reports and saves a side-by-side comparison

## Setup

```bash
pip install -r requirements.txt
```

Download the IGHM and IGHG files for Subject-SLE1 from OAS (Disease:
SLE, Chain: Heavy) and place them in `data/`.

## Usage

```bash
cd scripts
python compare_isotypes.py
```

## Results

| Isotype | IGHV4-34 sequences | Intact AVY | Mutated AVY | % Intact |
|---|---|---|---|---|
| IGHM (naive) | 21,424 | 17,713 | 3,656 | **82.9%** |
| IGHG (class-switched) | 4,225 | 2,658 | 1,535 | **63.4%** |

There is a clear drop in AVY retention from naive (82.9%) to
class-switched (63.4%) sequences, indicating that maturation and
selection do exert *some* corrective pressure on this self-reactive
motif. However, the fact that nearly two-thirds of mature,
class-switched IGHV4-34 antibodies in this patient still retain an
intact, self-reactive AVY motif suggests this correction is
substantially incomplete — consistent with the "leaky tolerance
checkpoint" pattern described for IGHV4-34 in SLE.

**Caveat:** as in the companion project, AVY status is determined by
checking the final 3 residues of the annotated FR1 region (`fwr1_aa`),
which does not account for indels or confirm against each sequence's
individual germline alignment. Results from a single patient should
also not be generalized without replication across additional
subjects.

Detailed per-sequence results are saved to
`results/isotype_avy_comparison.csv`.

## Folder structure

```
ighv4-34-isotype-comparison/
├── scripts/
│   └── compare_isotypes.py
├── data/            (not included -- see Setup)
├── results/
├── requirements.txt
└── README.md
```
