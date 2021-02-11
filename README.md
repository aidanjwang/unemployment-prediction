# Unemployment Prediction
Predict duration of unemployment for individuals using data from the Current Population Survey (CPS). Uses harmonized microdata from IPUMS CPS.[^1] Work in progress.

# Installation

### Download the Data

1. Clone this repo to your computer and go to the `unemployment-prediction` folder.
2. Create a folder called `data` for the downloaded data.
3. Create an account with IPUMS CPS [here](https://cps.ipums.org/cps/).
4. Select a data extract with only all basic monthly samples from Jan 2017 to Mar 2020 and all core household- and person-level variables. 
5. Download the data extract in CSV format and save it in the `data` folder with the name `cps.csv`.

### Install the Requirements

1. Go to the `unemployment-prediction` folder.
2. Run `pip install -r requirements.txt` to install the required libraries.

# Usage
1. Go to the `unemployment-prediction` folder.
2. Create a folder called `processed` for the processed data.
3. Run the master script `master.sh` to run all scripts, or alternatively:
	1. Run `python select.py` to select necessary variables and observations corresponding to individuals exiting unemployment, drop missings, and save at `processed/unemp_exits.csv`.
	2. Run `python annotate.py` to annotate processed data by adjusting variables dates and preparing for prediction models, split and save at `processed/train.csv` and `processed/test.csv`.

### Extending This
1. Implement the predictions for the duration of unemployment for individuals using the processed data.

[^1]: IPUMS-CPS, University of Minnesota, [www.ipums.org](www.ipums.org).