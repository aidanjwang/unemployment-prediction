"""
Select from downloaded data the necessary variables and observations 
corresponding to individuals exiting unemployment. Drop missings. Save 
processed data at processed/unemp_exits.csv.

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
    # Generate date var. Survey usually administered in week of the 12th
    cps["DATE"] = pd.to_datetime(cps[["YEAR", "MONTH"]].assign(day=12))
    
    # Get each individual's next survey emp status and date
    cps.sort_index(inplace=True)
    cps[["F_EMPSTAT", "F_DATE"]] = cps.groupby(level=0)[
            ["EMPSTAT", "DATE"]].shift(-1)

    # Keep obs where individual is unemp and exits in next survey
    print("VALUE COUNTS BEFORE SELECTION")
    print(cps["EMPSTAT"].value_counts(sort=False, dropna=False))
    print(cps["F_EMPSTAT"].value_counts(sort=False, dropna=False))
    
    cps = cps[cps["EMPSTAT"].isin([20, 21, 22]) &
                cps["F_EMPSTAT"].notna() &
                ~cps["F_EMPSTAT"].isin([00, 20, 21, 22])]
    
    print("VALUE COUNTS AFTER SELECTION")
    print(cps["EMPSTAT"].value_counts(sort=False, dropna=False))
    print(cps["F_EMPSTAT"].value_counts(sort=False, dropna=False))
    
    return cps


def drop_missings(cps):
    # Drop obs missing these vars
    print("OBS BEFORE DROPPING MISSINGS:", cps.shape[0])
    
    cps = cps[cps["REGION"]!=97]
    cps = cps[cps["STATEFIP"]!=99]
    cps = cps[cps["METRO"]!=9]
    cps = cps[cps["METAREA"]!=9999]
    cps = cps[~cps["FAMINC"].isin([995, 999])]
    cps = cps[cps["RACE"]!=999]
    cps = cps[cps["FAMSIZE"]!=0]
    cps = cps[cps["FTYPE"]!=9]
    cps = cps[cps["CLASSWKR"]!=99]
    cps = cps[cps["DURUNEMP"]!=999]
    cps = cps[cps["EDUC"]!=999]
    
    print("OBS AFTER DROPPING MISSINGS:", cps.shape[0])       
       
    return cps


def write(cps):
    cps.to_csv(os.path.join(settings.PROCESSED_DIR, "unemp_exits.csv"))
    
    
if __name__ == "__main__":
    cps = read()
    cps = select(cps)
    cps = drop_missings(cps)
    write(cps)
    
    