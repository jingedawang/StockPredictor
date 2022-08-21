from qlib.contrib.data.handler import Alpha158

class Alpha158TwoWeeks(Alpha158):
    
    """
    Override the get_label_config method in Alpha158.
    This will build a data handler that labels the items with price increase in next 10 trading days.
    """
    def get_label_config(self):
        return (["Ref($close, -10)/Ref($close, -1) - 1"], ["LABEL0"])
