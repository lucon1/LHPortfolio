import pandas as pd
import datetime
import uuid

from .transaction import Transaction

def load_data(filename):
    '''load data from csv file with given filename to new pandas dataframe'''
    df = pd.read_csv(filename)
    return df


def save_data(df, filename):
    '''save data from given pandas dataframe to csv file with given filename'''
    df.to_csv(filename, index=False)

def see_data(df):
    '''see data from given pandas dataframe used for debugging'''
    print("===INFO===")
    df.info()
    print("===data types===")
    print(df.dtypes)
    print("===Head===")
    print(df.head())
    print("===Tail===")
    print(df.tail())




def df_to_transactions(df):
    '''convert given pandas dataframe to a dict'''
    new_dict = {}
    for tran_id, date, amount, cat, description in df.itertuples(index=False, name=None):
        try:
            if len(str(tran_id)) < 5 or tran_id is None:
                tran_id = uuid.uuid4()
            date = pd.to_datetime(date)
            if pd.isna(cat):
                cat = "Uncategorized"
            if pd.isna(description):
                description = ""

            t =  Transaction(tran_id, date, amount, cat, description)
            new_dict[tran_id] = t
        except ValueError as r:
            print(f"Skipping row {r}")
    return new_dict

def transactions_to_df(transaction_list):
    '''coverts a given list or dict of trnasctions to a pandas dataframe'''
    rows = []
    for transaction in transaction_list:
        rows.append({"ID": transaction.get_tran_id(),
                     "Date": transaction.get_date(),
                     "Amount": transaction.get_amount(),
                     "Category": transaction.get_cat(),
                     "Description": transaction.get_description()})
    df = pd.DataFrame(rows)
    return df

# temp = load_data("Budget_test_data_1.csv")
# see_data(temp)
