#!/bin/bash
# Master bash script for unemployment-prediction/
# Created on 2/8/21 by Aidan Wang

# Select necessary variables and observations corresponding to individuals 
# exiting unemployment. Drop missings. Save at processed/unemp_exits.csv.
python select.py

# Annotate processed data by adjusting variables dates and preparing for 
# prediction models. Split and save at processed/train.csv and 
# processed/test.csv.
python annotate.py
