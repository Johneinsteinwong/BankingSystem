from decimal import Decimal

def convert_decimal(amount: str):
    '''
    A function to convert to Decimal, 
    different from the default Decimal(),'NaN' and 'Inifity' are not allowed
    '''
    try:
        amount = Decimal(amount)
        # check for 'NaN' and 'Inifity' 
        if not amount.is_finite():
            raise ValueError("Invalid input, please input numbers only!")
        return amount
    except:
        raise ValueError("Invalid input, please input numbers only!")