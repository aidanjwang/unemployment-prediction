# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 10:36:02 2021

@author: Aidan
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


def select():
    # Read in raw data, keeping selected vars
    data = pd.read_csv(os.path.join(settings.DATA_DIR, "cps.csv"),
                       index_col=["CPSIDP", "MISH"], usecols=SELECT)
    
    # Generate date var
    data["DATE"] = pd.to_datetime(
            data[["YEAR", "MONTH"]].assign(day=1)).dt.to_period("M")
    
    # Get each individual's next survey emp status and date
    data.sort_index(inplace=True)
    data[["F_EMPSTAT", "F_DATE"]] = data.groupby(level=0)[
            ["EMPSTAT", "DATE"]].shift(-1)

    # Keep obs where individual is unemp and exits in next survey
    print("VALUE COUNTS IN RAW DATA")
    print("OBS:", data.shape[0])
    print(data["EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    print(data["F_EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    
    data = data[data["EMPSTAT"].isin([20, 21, 22]) &
                data["F_EMPSTAT"].notna() &
                ~data["F_EMPSTAT"].isin([00, 20, 21, 22])]
    
    print("\nVALUE COUNTS IN PROCESSED DATA")
    print("OBS:", data.shape[0])
    print(data["EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    print(data["F_EMPSTAT"].value_counts(
            normalize=True, sort=False, dropna=False))
    
    # Save processed data
    data.to_csv(os.path.join(settings.PROCESSED_DIR, "unemp_exits.csv"))
    
    
if __name__ == "__main__":
    select()
    
    