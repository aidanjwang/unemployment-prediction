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
            index_col=["CPSIDP", "MISH"])
    return unemp_exits


def get_unemp_duration(unemp_exits):
    return unemp_exits
    

def prepare(unemp_exits):
    return unemp_exits


def write(unemp_exits):
    return


if __name__ == "__main__":
    unemp_exits = read()
    unemp_exits = get_unemp_duration(unemp_exits)
    unemp_exits = prepare(unemp_exits)
    write(unemp_exits)
    
    