"""
Created on Thu Jan 21 18:55:30 2021

@author: aidan
"""

import os
import pandas as pd
import settings


def read():
    unemp_exits = pd.read_csv(
            os.path.join(settings.PROCESSED_DIR, "unemp_exits.csv"), 
            index_col=["CPSIDP", "MISH"], parse_dates=["DATE", "F_DATE"])
    return unemp_exits


def adjust_dates(unemp_exits):
    # TODO: edit for individuals exiting unemp into NILF
    # Get duration of unemp at end: halfway between current and next survey
    unemp_exits["DURUNEMP_END"] = unemp_exits["DURUNEMP"] + (
            (unemp_exits["F_DATE"] - unemp_exits["DATE"]).dt.days / 7) / 2
    
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
    return unemp_exits


def write(unemp_exits):
    return


if __name__ == "__main__":
    unemp_exits = read()
    unemp_exits = adjust_dates(unemp_exits)
    unemp_exits = prepare_variables(unemp_exits)
    write(unemp_exits)
    
    