import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime
import logic.logic_manager as lm
import data.data_manager as dm

class FinanceApp:
    def __init__(self):
        # initialize window
        self.root = tk.Tk()
        self.root.title("Budget Tracker by LH")
        self.root.geometry("1280x680")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(0, weight=1)

        # initialize starting data
        self.transactions = None
        self.transactions_is_loaded = False
        # if a previous file was loaded
        self.current_file = "data/test_data_initial.csv" # will be prev file in settings
        self.load_transaactions(self.current_file)
        ###

        # build interface
        self.build_menu()
        self.build_transaction_panel()
        self.build_button_panel()

        if self.transactions_is_loaded:
            self.update_transactions(self.transaction_tree)

    def build_transaction_panel(self):
        ''' create transactions panel '''
        transaction_frame = tk.Frame(master=self.root, relief=tk.GROOVE, borderwidth=2)
        transaction_frame.grid(column=0, row=0, sticky="nsew")
        scrollbar = tk.Scrollbar(master=transaction_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #create a treeview for the transactions
        self.transaction_tree = ttk.Treeview(
            master=transaction_frame,
            columns=("Date", "Amount", "Category", "Description"),
            show="headings",
            selectmode="browse")
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Description", text="Description")
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.transaction_tree.yview)


    def build_button_panel(self):
        ''' create button panel '''
        button_frame = tk.Frame(master=self.root, borderwidth=2)
        button_frame.grid(column=1, row=0, sticky = "n")
        add_button = tk.Button(
            button_frame,
            text="Add Transaction",
            width=50,
            command=lambda: self.transaction_input_window(mode='add'))
        add_button.pack()
        del_button = tk.Button(
            button_frame,
            text="Delete Transaction",
            width=50,
            command= lambda: self.del_transaction_command(self.transaction_tree.selection()[0]))
        del_button.pack()
        modify_button = tk.Button(
            button_frame,
            text="Modify Transaction",
            width=50,
            command= lambda: self.transaction_input_window(mode='mod', tran_id=self.transaction_tree.selection()[0]))
        modify_button.pack()

    def build_menu(self):
        ''' create menu '''
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command= self.new_transaction_list)
        file_menu.add_command(label="Open...", command= self.open_transactions)
        file_menu.add_separator()
        file_menu.add_command(label="Save", command= self.save_transactions_current)
        file_menu.add_command(label="Save As", command= self.save_transactions_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About")

    def load_transaactions(self, filename):
        self.current_file = filename
        self.transactions = dm.df_to_transactions(dm.load_data(filename))
        self.transactions_is_loaded = True

    def update_transactions(self, field):
        ''' update transactions in given field '''
        for item in field.get_children():
            field.delete(item)
        display_transactions = lm.sort_transactions(self.transactions)
        for transaction in display_transactions:
            field.insert("",
                tk.END,
                iid=transaction.tran_id,
                values=(
                    transaction.date.strftime("%b/%d/%y"),
                    transaction.amount,
                    transaction.cat,
                    transaction.description
                    ))

    def save_transactions_current(self):
        dm.save_data(dm.transactions_to_df(self.transactions.values()), self.current_file)

    def save_transactions_as(self):
        filename = filedialog.asksaveasfilename(filetypes=[
            ("CSV files", "*.csv"),
            ("All files", "*.*")],
            defaultextension=".csv")
        if filename:
            dm.save_data(dm.transactions_to_df(self.transactions.values()), filename)

    def open_transactions(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            self.load_transaactions(filename)
            self.update_transactions(self.transaction_tree)

    def new_transaction_list(self):
        self.transactions = {}
        self.update_transactions(self.transaction_tree)

    def transaction_input_window(self, mode=None, tran_id=None):
        '''create a new transactions window'''
        top_add = tk.Toplevel(master=self.root)
        if mode == 'add':
            top_add.title("Add Transaction")
        elif mode == 'mod':
            top_add.title("Modify Transaction")
        else:
            top_add.title("Transaction")
        date_text = tk.Label(top_add, text="Date (YYYY/MM/DD")
        date_text.grid(column=0, row=0)
        date_entry = tk.Entry(top_add, )
        date_entry.grid(column=1, row=0)
        amount_text = tk.Label(top_add, text="Amount")
        amount_text.grid(column=0, row=1)
        amount_entry = tk.Entry(top_add)
        amount_entry.grid(column=1, row=1)
        cat_text = tk.Label(top_add, text="Category")
        cat_text.grid(column=0, row=2)
        cat_entry = tk.Entry(top_add)
        cat_entry.grid(column=1, row=2)
        description_text = tk.Label(top_add, text="Description")
        description_text.grid(column=0, row=3)
        description_entry = tk.Entry(top_add)
        description_entry.grid(column=1, row=3)
        if mode == 'mod':
            transaction = self.transactions[tran_id]
            date_entry.insert(0,datetime.date.strftime(transaction.get_date(), "%Y/%m/%d"))
            amount_entry.insert(0,transaction.get_amount())
            cat_entry.insert(0,transaction.get_cat())
            description_entry.insert(0,transaction.get_description())
        enter_button = tk.Button(top_add, text="Enter", width=50,
                command= lambda: self.submit_transaction(
                    top_add,
                    mode=mode,
                    tran_id=tran_id,
                    amount=amount_entry.get(),
                    date=date_entry.get(),
                    cat=cat_entry.get(),
                    description=description_entry.get()))
        enter_button.grid(column=1, row=4, columnspan=2)

    def submit_transaction(self, toplevel, mode=None, tran_id=None, amount=None, date=None, cat=None, description=None):
        ''' submit transaction from input '''
        if mode == 'add':
            processed = self.add_transaction_command(toplevel, amount, date=date, cat=cat, description=description)
        elif mode == 'mod':
            processed = self.modify_transaction_command(toplevel, tran_id, amount=amount, date=date, cat=cat, description=description)
        if processed:
            toplevel.destroy()

    def add_transaction_command(self, window, amount, date=None, cat=None, description=None):
        ''' add transaction to the transaction dict '''
        #makes sure amount is filled as its a required field
        if amount == '':
            print("must enter an amount")
            tk.messagebox.showerror(
                master=window,
                message="must enter an amount",
                title="no amount entered",
                default=tk.messagebox.OK,)
            window.lift()
            return False
        lm.add_transaction(lm.create_transaction(amount, date, cat, description), self.transactions)
        self.update_transactions(self.transaction_tree)
        return True

    def del_transaction_command(self, transaction_id):
        ''' delete transaction from the transaction dict '''
        lm.remove_transaction(transaction_id, self.transactions)
        self.update_transactions(self.transaction_tree)

    def modify_transaction_command(self, window, tran_id, amount=None, date=None, cat=None, description=None):
        ''' modify transaction dict '''
        if tran_id is None or tran_id == "":
            print("invalid Transaction ID")
            tk.messagebox.showerror(
                master=window,
                message="must select a valid transaction",
                title="invalid transaction",
                default=tk.messagebox.OK,)
            window.lift()
            return False
        lm.modify_transaction(tran_id, self.transactions, date=date, amount=amount, category=cat, description=description)
        self.update_transactions(self.transaction_tree)
        return True

    def run(self):
        self.root.mainloop()