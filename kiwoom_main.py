# DEVELOPED_MODULE_NUMBER = 5
# for module_num in range(DEVELOPED_MODULE_NUMBER):
#     mod_name = 'kiwoom' + str(module_num+1)
#     from mod_name import *

from kiwoom2 import *
from kiwoom3 import *
from kiwoom4 import *
from kiwoom5 import *

def main():
    app = QApplication(sys.argv)
    
    # kiwoom1 and kiwoom2
    # kiwoom1 establishes connection to the Kiwoom server
    # kiwoom2 requests transactions and receives responses
    transaction_req = tr_requests()
    comm_requsts_handler(transaction_req, opt_10081_set_inputs, opt_10081_comm_inputs)
    
    # kiwoom3
    # saves received responses to a dababase file
    df_to_db(transaction_req.results_df, 'daily_records.db', 'Daily_Prices')
    
    # kiwoom4
    # visualizes received responses in graphics
    visualize_finplot(transaction_req.results_df)
    visualize_plotly(transaction_req.results_df)
    # visualize_mplfinance(transaction_req.results_df)

    # kiwoom5
    # backtests strategies employed
    



if __name__ == '__main__':
    main()
