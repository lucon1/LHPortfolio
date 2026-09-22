# transaction object / data type

class Transaction(object):
    def __init__(self, tran_id, date, amount, cat=None, description=None):
        '''initialize a transaction object'''
        self.tran_id = tran_id
        self.date = date # date transaction occurred
        self.amount = amount # amount of transaction]
        if cat is not None:
            self.cat = cat # category of transaction ie bills, medical, food
        else:
            self.cat = "uncategorized" # give category default uncategorized
        if description is not None:
            self.description = description
        else:
            self.description = "" # give description empty string

    def __str__(self):
        return f"{self.date.normalize()} {self.amount} {self.cat} {self.description}"

    def __repr__(self):
        return (
            f"Transaction("
            f"id={self.tran_id}, "
            f"date={self.date}, "
            f"amount={self.amount}, "
            f"category={self.cat}, "
            f"description={self.description})"
        )

    def get_tran_id(self):
        '''get id of transaction'''
        return self.tran_id

    def get_date(self):
        '''get date of transaction'''
        return self.date

    def get_amount(self):
        '''get amount of transaction'''
        return self.amount

    def get_cat(self):
        '''get category of transaction'''
        return self.cat

    def get_description(self):
        '''get description of transaction'''
        return self.description

    def set_date(self, date):
        '''set date of transaction'''
        self.date = date

    def set_amount(self, amount):
        '''set amount of transaction'''
        self.amount = amount

    def set_cat(self, cat):
        '''set category of transaction'''
        self.cat = cat

    def set_description(self, description):
        '''set description of transaction'''
        self.description = description

    def parse_date(date):
        '''
        parses date to datetime object from string
        '''
        # check if a datetime object, or string and change to datetime, otherwise raise exception
        if isinstance(date, datetime.datetime):
            return date
        elif type(date) == str:
            return datetime.datetime.strptime(date, "%Y-%m-%d")
        else:
            raise TypeError("date must be datetime or string")