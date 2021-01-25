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
    # Get duration of unemp at end: halfway between current and next survey 
    # dates
    unemp_exits["DURUNEMP_END"] = unemp_exits["DURUNEMP"] + (
            (unemp_exits["F_DATE"] - unemp_exits["DATE"]).dt.days / 7) / 2
    
    return unemp_exits
    

def prepare(unemp_exits):
    return unemp_exits


def write(unemp_exits):
    return


if __name__ == "__main__":
    unemp_exits = read()
    unemp_exits = adjust_dates(unemp_exits)
    unemp_exits = prepare(unemp_exits)
    write(unemp_exits)
    
    