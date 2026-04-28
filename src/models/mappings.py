"""
MIMIC-III Antibiotic and Organism Name Mappings.
Maps human-readable names to encoded values used by the model.
"""

# Common MIMIC-III antibiotics (mapped to encoded values)
ANTIBIOTIC_MAP = {
    "AMPICILLIN": 90002.0,
    "CEFAZOLIN": 90003.0,
    "CEFTRIAXONE": 90004.0,
    "CIPROFLOXACIN": 90005.0,
    "GENTAMICIN": 90006.0,
    "LEVOFLOXACIN": 90007.0,
    "MEROPENEM": 90008.0,
    "OXACILLIN": 90009.0,
    "PENICILLIN": 90010.0,
    "PIPERACILLIN-TAZOBACTAM": 90011.0,
    "VANCOMYCIN": 90012.0,
    "CEFEPIME": 90013.0,
    "IMIPENEM": 90014.0,
    "TOBRAMYCIN": 90015.0,
    "AMIKACIN": 90016.0,
    "AZTREONAM": 90017.0,
    "CEFTAZIDIME": 90018.0,
    "CLINDAMYCIN": 90019.0,
    "DAPTOMYCIN": 90020.0,
    "ERTAPENEM": 90021.0,
    "LINEZOLID": 90022.0,
    "METRONIDAZOLE": 90023.0,
    "NITROFURANTOIN": 90024.0,
    "RIFAMPIN": 90025.0,
    "TETRACYCLINE": 90026.0,
    "TRIMETHOPRIM-SULFAMETHOXAZOLE": 90027.0,
    "AMPICILLIN-SULBACTAM": 90028.0,
    "CEFOXITIN": 90029.0,
    "TIGECYCLINE": 90030.0,
    "COLISTIN": 90031.0,
}

# Common MIMIC-III organisms (mapped to encoded values)
ORGANISM_MAP = {
    "STAPHYLOCOCCUS AUREUS": 80002.0,
    "ESCHERICHIA COLI": 80004.0,
    "KLEBSIELLA PNEUMONIAE": 80005.0,
    "PSEUDOMONAS AERUGINOSA": 80006.0,
    "ENTEROCOCCUS FAECALIS": 80007.0,
    "ENTEROCOCCUS FAECIUM": 80008.0,
    "ACINETOBACTER BAUMANNII": 80009.0,
    "STREPTOCOCCUS PNEUMONIAE": 80010.0,
    "ENTEROBACTER CLOACAE": 80011.0,
    "PROTEUS MIRABILIS": 80012.0,
    "SERRATIA MARCESCENS": 80013.0,
    "CITROBACTER FREUNDII": 80014.0,
    "STENOTROPHOMONAS MALTOPHILIA": 80015.0,
    "CANDIDA ALBICANS": 80016.0,
    "CANDIDA GLABRATA": 80017.0,
    "HAEMOPHILUS INFLUENZAE": 80018.0,
    "MORAXELLA CATARRHALIS": 80019.0,
    "BACTEROIDES FRAGILIS": 80020.0,
    "CLOSTRIDIUM DIFFICILE": 80021.0,
    "STREPTOCOCCUS PYOGENES": 80022.0,
}

# Lab value means from MIMIC-III training set (for imputation)
LAB_MEANS = {
    "lab_bun": 23.5,
    "lab_creatinine": 1.2,
    "lab_glucose": 128.0,
    "lab_hemoglobin": 10.8,
    "lab_platelets": 215.0,
    "lab_potassium": 4.1,
    "lab_sodium": 138.5,
    "lab_wbc": 11.2,
}


def get_antibiotic_code(name: str) -> float | None:
    return ANTIBIOTIC_MAP.get(name.upper())


def get_organism_code(name: str) -> float | None:
    return ORGANISM_MAP.get(name.upper())


def list_antibiotics() -> list[str]:
    return sorted(ANTIBIOTIC_MAP.keys())


def list_organisms() -> list[str]:
    return sorted(ORGANISM_MAP.keys())
