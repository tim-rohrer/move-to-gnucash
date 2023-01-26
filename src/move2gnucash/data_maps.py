import pandas as pd

def accounts_and_balances(data: pd.DataFrame):
    data.assign(account_names = lambda data: data["Accounts"].map(lambda Accounts: Accounts ))
    # data["account_name"] = data["Accounts"].map({})
    return(data)
    # return pd.DataFrame({"accounts": ["Assets"],
    #                      "balances": ["placeholder"]})
