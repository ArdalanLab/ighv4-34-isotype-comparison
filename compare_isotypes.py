"""
compare_isotypes.py

Compare AVY motif status (intact vs mutated) between IGHM (naive)
and IGHG (class-switched) sequences, within the same SLE patient
(Subject-SLE1), to test whether maturation correlates with AVY
motif correction.
"""

import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "..", "data")


def check_avy(fwr1_sequence):
    """Return 'intact', 'mutated', or 'unknown' for one FR1 sequence."""
    if not isinstance(fwr1_sequence, str):
        return "unknown"
    return "intact" if fwr1_sequence[-3:] == "AVY" else "mutated"


def analyze_file(filename, label):
    """
    Load one OAS file, filter for IGHV4-34, check AVY status,
    print a summary, and return the filtered+labeled DataFrame.
    """
    file_path = os.path.join(data_dir, filename)
    df = pd.read_csv(file_path, header=1, compression="gzip")

    ighv4_34 = df[df["v_call"].str.contains("IGHV4-34", na=False)].copy()
    ighv4_34["avy_status"] = ighv4_34["fwr1_aa"].apply(check_avy)

    counts = ighv4_34["avy_status"].value_counts()
    intact = counts.get("intact", 0)
    mutated = counts.get("mutated", 0)
    total_known = intact + mutated
    percent_intact = (intact / total_known * 100) if total_known > 0 else 0

    print(f"=== {label} ===")
    print(f"Total sequences: {len(df)}")
    print(f"IGHV4-34 sequences: {len(ighv4_34)}")
    print(f"Intact: {intact}  |  Mutated: {mutated}")
    print(f"Percent intact: {percent_intact:.1f}%\n")

    ighv4_34["isotype"] = label
    return ighv4_34


ighm_results = analyze_file("ighm_subject_sle1.csv.gz", "IGHM")
ighg_results = analyze_file("ighg_subject_sle1.csv.gz", "IGHG")

combined = pd.concat([ighm_results, ighg_results])

results_dir = os.path.join(script_dir, "..", "results")
os.makedirs(results_dir, exist_ok=True)

results_path = os.path.join(results_dir, "isotype_avy_comparison.csv")
combined[["isotype", "v_call", "fwr1_aa", "avy_status"]].to_csv(results_path, index=False)

print(f"Saved combined results to: {results_path}")