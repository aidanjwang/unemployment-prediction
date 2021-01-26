"""
Created on Sat Jan 16 10:36:02 2021

@author: aidan
"""

import os
import pandas as pd
import settings


SELECT = [
    "YEAR",
    "MONTH",
    "MISH",
    "HHTENURE",
    "GQTYPE",
    "REGION",
    "STATEFIP",
    "METRO",
    "METAREA",
    "COUNTY",
    "CBSASZ",
    "METFIPS",
    "INDIVIDCC",
    "FAMINC",
    "NFAMS",
    "NCOUPLES",
    "NMOTHERS",
    "NFATHERS",
    "CPSIDP",
    "RELATE",
    "AGE",
    "SEX",
    "RACE",
    "MARST",
    "POPSTAT",
    "VETSTAT",
    "MOMLOC",
    "MOMLOC2",
    "POPLOC",
    "POPLOC2",
    "SPLOC",
    "FAMSIZE",
    "NCHILD",
    "NCHLT5",
    "ELDCH",
    "YNGCH",
    "NSIBS",
    "PECOHAB",
    "PEMOMTYP",
    "PEDADTYP",
    "FTYPE",
    "BPL",
    "YRIMMIG",
    "CITIZEN",
    "MBPL",
    "FBPL",
    "NATIVITY",
    "HISPAN",
    "EMPSTAT",
    "OCC2010",
    "IND1990",
    "CLASSWKR",
    "UHRSWORKT",
    "UHRSWORK1",
    "UHRSWORK2",
    "DURUNEMP",
    "WHYUNEMP",
    "WKSTAT",
    "PROFCERT",
    "STATECERT",
    "JOBCERT",
    "WRKOFFER",
    "EDUC",
    "EDCYC",
    "EDDIPGED",
    "EDHGCGED",
    "SCHLCOLL",
    "DIFFHEAR",
    "DIFFEYE",
    "DIFFREM",
    "DIFFPHYS",
    "DIFFMOB",
    "DIFFCARE",
    "DIFFANY"
]


def read():
    # Read in raw data, keeping selected vars
    cps = pd.read_csv(os.path.join(settings.DATA_DIR, "cps.csv"),
                       index_col=["CPSIDP", "MISH"], usecols=SELECT)
    return cps


def select(cps):
    # Generate date var
    cps["DATE"] = pd.to_datetime(cps[["YEAR", "MONTH"]].assign(day=15))
    
    # Get each individual's next survey emp status and date
    cps.sort_index(inplace=True)
    cps[["F_EMPSTAT", "F_DATE"]] = cps.groupby(level=0)[
            ["EMPSTAT", "DATE"]].shift(-1)

    # Keep obs where individual is unemp and exits in next survey
    print("VALUE COUNTS IN RAW DATA")
    print("OBS:", cps.shape[0])
    print(cps["EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    print(cps["F_EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    
    cps = cps[cps["EMPSTAT"].isin([20, 21, 22]) &
                cps["F_EMPSTAT"].notna() &
                ~cps["F_EMPSTAT"].isin([00, 20, 21, 22])]
    
    print("\nVALUE COUNTS IN PROCESSED DATA")
    print("OBS:", cps.shape[0])
    print(cps["EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    print(cps["F_EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    
    return cps


def clean(cps):
    # TODO: clean variables based on codebook
    return cps


def write(cps):
    cps.to_csv(os.path.join(settings.PROCESSED_DIR, "unemp_exits.csv"))
    
    
if __name__ == "__main__":
    cps = read()
    cps = select(cps)
    cps = clean(cps)
    write(cps)
    
    