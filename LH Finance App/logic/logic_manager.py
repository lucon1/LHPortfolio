import datetime
import uuid
from data.transaction import Transaction
import data.data_manager as dm

def add_transaction(new_transaction, tran_dict):
    '''given a new transaction object, adds it to transactions dict'''
    tran_dict[new_transaction.tran_id] = new_transaction

def remove_transaction(tran_id, tran_dict):
    '''given a dict of transactions removes transaction at given transaction id'''
    if tran_id in tran_dict:
        del tran_dict[tran_id]

def modify_transaction(tran_id, tran_dict, date=None, amount=None, category=None, description=None):
    '''given a dict of transactions modifies transaction dict by given transaction id'''
    if tran_id in tran_dict:
        if date != None or date != "":
            tran_dict[tran_id].set_date(parse_date(date))
        if amount != None or amount != "":
            tran_dict[tran_id].set_amount(amount)
        if category != None or category != "":
            tran_dict[tran_id].set_cat(category)
        if description != None:
            tran_dict[tran_id].set_description(description)


def remove_transaction_visible(line_num, display_list, transactions):
    '''given a list of visible transactions and a dict of stored transactions removes transaction at given line number'''
    #no longer used, was for command line view
    remove_transaction(display_list[line_num-1].get_tran_id(), transactions)

def sort_transactions(tran_dict, sort_mode=None):
    '''given a dict of transactions, sorts them and returns list of transactions, defaults to sort by date'''
    if sort_mode == "amount":
        display_list = sorted(tran_dict.values(), key=lambda t: t.get_amount())
    elif sort_mode == "category":
        display_list = sorted(tran_dict.values(), key=lambda t: t.get_category())
    elif sort_mode == "description":
        display_list = sorted(tran_dict.values(), key=lambda t: t.get_description())
    else:
        display_list = sorted(tran_dict.values(), key=lambda t: t.get_date())
    return display_list

def display_transactions(display_list, start_range=0, end_range=None):
    '''given a list of transactions, displays them in rows with given start and end range'''
    if end_range is None:
        end_range = len(display_list)
    for i in range(start_range, end_range):
        print((i+1), ": ", display_list[i]) #print line number and transaction

def create_transaction(amount, date=None, category=None, description=None):
    '''creates a new transaction object required amount, everything else is optional. If no date will default to "now"'''
    if date == "" or date == "now":
        date = datetime.datetime.now()
    elif type(date) != datetime.datetime:
        date = datetime.datetime.strptime(date, "%Y/%m/%d")
    tran_id = str(uuid.uuid4())
    return Transaction(tran_id, date, amount, category, description)

def parse_date(date):
    '''parses date to datetime object from string'''
    # check if a datetime object, or string and change to datetime, otherwise raise exception
    if isinstance(date, datetime.datetime):
        return date
    elif type(date) == str:
        return datetime.datetime.strptime(date, "%Y/%m/%d")
    else:
        raise TypeError("date must be datetime or string")

##-----Tests-----

# transactions_df = dm.load_data("data/Budget_test_data_1.csv")
# transactions = dm.df_to_transactions(transactions_df)
# # dm.see_data(transactions_df)
# # # print("=====test transaction=====")
# # # t = Transaction("01/02/2020", 100.15)
# # # print(t)
# print("=====transaction list=====")
# display_transactions(transactions)
# print("=====added transaction list=====")
# add_transaction(Transaction("abc123", dm.parse_date("2026-08-08"), 120.15, "Bills", "test bill"), transactions)
# display_list = get_transactions_sorted(transactions)
# display_transactions(display_list, len(transactions)-10)
# print("=====removed transaction list=====")
# remove_transaction_visible(450, display_list, transactions)
# display_list = get_transactions_sorted(transactions)
# display_transactions(display_list, start_range=len(transactions)-10)
# # new_transactions_df = dm.transactions_to_df(transactions)
# # dm.save_data(new_transactions_df,"data/Budget_test_data_2.csv")
# # transactions_df = dm.load_data("data/Budget_test_data_2.csv")
# # transactions = dm.df_to_transactions(transactions_df)
# # dm.see_data(transactions_df)
# print("=====removed transaction list deux=====")
# remove_transaction_visible(444, display_list, transactions)
# remove_transaction_visible(446, display_list, transactions)
# display_list = get_transactions_sorted(transactions)
# display_transactions(display_list, len(transactions) - 10)