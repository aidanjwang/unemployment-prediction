"""
Created on Thu Jan 21 18:55:30 2021

@author: aidan
"""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
import settings


def read():
    unemp_exits = pd.read_csv(
            os.path.join(settings.PROCESSED_DIR, "unemp_exits.csv"), 
            index_col=["CPSIDP", "MISH"], parse_dates=["DATE", "F_DATE"])
    return unemp_exits


def adjust_dates(unemp_exits):
    # Get duration of unemp at end: halfway between current and next survey
    unemp_exits["DURUNEMP_END"] = unemp_exits["DURUNEMP"] + (
            (unemp_exits["F_DATE"] - unemp_exits["DATE"]).dt.days / 7) / 2
    # Hard code max duration of unemp for indivudals that exit unemp into NILF
    unemp_exits.loc[~unemp_exits["F_EMPSTAT"].isin([10, 12]), 
                    "DURUNEMP_END"] = 146
            
    # Get date and ages at start of unemp
    unemp_exits["YEAR_START"] = (
            unemp_exits["DATE"] 
            - pd.to_timedelta(unemp_exits["DURUNEMP"], unit="W")).dt.year
    unemp_exits["MONTH_START"] = (
            unemp_exits["DATE"] 
            - pd.to_timedelta(unemp_exits["DURUNEMP"], unit="W")).dt.month
    unemp_exits["AGE_START"] = unemp_exits["AGE"] - round(
            unemp_exits["DURUNEMP"] / 52.143)
    unemp_exits["ELDCH_START"] = unemp_exits["ELDCH"] - round(
            unemp_exits["DURUNEMP"] / 52.143)
    unemp_exits["YNGCH_START"] = unemp_exits["YNGCH"] - round(
            unemp_exits["DURUNEMP"] / 52.143)
    
    # Drop unnecessary vars and unadjusted date vars
    unemp_exits.drop(columns=["DURUNEMP", "DATE", "F_DATE", "EMPSTAT", 
                              "F_EMPSTAT", "YEAR", "MONTH", "AGE", "ELDCH", 
                              "YNGCH"], inplace=True)
    
    return unemp_exits
    

def prepare_variables(unemp_exits):
    # Convert categorical vars to dummies
    unemp_exits = pd.get_dummies(unemp_exits, columns=[
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
            "RELATE",
            "SEX",
            "RACE",
            "MARST",
            "POPSTAT",
            "VETSTAT",
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
            "OCC2010",
            "IND1990",
            "CLASSWKR",
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
            "DIFFANY",
            "MONTH_START"], drop_first=True)
    
    # Convert vars of person being in same household to dummies
    for var in ["MOMLOC", "MOMLOC2", "POPLOC", "POPLOC2", "SPLOC", "PECOHAB"]:
        unemp_exits[var] = (unemp_exits[var] != 0).astype(int)
    
    return unemp_exits


def write(unemp_exits):
    train, test = train_test_split(unemp_exits, random_state=1)
    train.to_csv(os.path.join(settings.PROCESSED_DIR, "train.csv"))
    test.to_csv(os.path.join(settings.PROCESSED_DIR, "test.csv"))


if __name__ == "__main__":
    unemp_exits = read()
    unemp_exits = adjust_dates(unemp_exits)
    unemp_exits = prepare_variables(unemp_exits)
    write(unemp_exits)
    
    