import pandas as pd
import os
import os.path
import time

###
# 输入：all_data_token文件夹，包括了所有可疑账户的交易记录
# 输出：合并为all-tx.csv，同时划分为all-normal-tx.csv和all-erc20-tx.csv

def MergeCSV( filepath, outfile):
    print("Executing function MergeCsv(", filepath, outfile, ")")
    t1 = time.time()
    MergeCsvOutput = pd.DataFrame()
    # 遍历目标文件夹下所有的交易文件
    for parent, dirnames, filenames in os.walk(filepath):
        for filepath in filenames:
            csvPath = os.path.join(parent, filepath)  #
            print('csvPath: ', csvPath)
            f = pd.read_csv(csvPath)
            MergeCsvOutput = pd.concat([MergeCsvOutput, f])
    t2 = time.time()
    print("Time for executing function MergeCsv: ", t2 - t1, "s")
    #MergeCsvOutput.reset_index(drop=True)
    MergeCsvOutput.drop_duplicates(inplace=True)
    MergeCsvOutput.to_csv(outfile, index=None)
    return

### 只保留一年的交易记录
def Filter_tx(input_file):
    tx_file = pd.read_csv(input_file)
    print('len(Origin): ', len(tx_file))

    start_time = min(tx_file['timeStamp']) # 第一笔转入的交易时间
    YEAR_SEC = 31536000
    tx_file = tx_file[(tx_file['timeStamp'] >= start_time) & (tx_file['timeStamp'] <= start_time + YEAR_SEC)]
    print('len(Origin): ', len(tx_file))
    tx_file.to_csv(input_file, index=None)
    return

### 分割ETH和token的交易
def Separation(input_file):
    tx_file = pd.read_csv(input_file)
    print('len(Origin): ', len(tx_file))

    tx_eth = tx_file[pd.isnull(tx_file.contractAddress)]
    print('len(tx_eth): ', len(tx_eth))
    tx_eth = tx_eth.sort_values(by='timeStamp')
    tx_eth.to_csv('../dataset/all-normal-tx.csv', index=None)

    tx_token = tx_file[pd.notnull(tx_file.contractAddress)]
    print('len(tx_token): ', len(tx_token))
    tx_token = tx_token.sort_values(by='timeStamp')
    tx_token.to_csv('../dataset/all-erc20-tx.csv', index=None)

    if len(tx_eth)+len(tx_token) != len(tx_file):
        print('WARNING !!!')
    return


if __name__ == '__main__':
    filepath = '../all_data_token'
    if not os.path.exists('../dataset/'):
        os.makedirs('../dataset/')
    outfile = '../dataset/all-tx.csv'
    MergeCSV(filepath, outfile)
    # Filter_tx(outfile)
    Separation(outfile)
    # filepath = eventName +"/all_data_token"
    # outfile = eventName+"/dataset/all-tx.csv"
    # MergeCSV(filepath, outfile)
    # # Filter_tx(outfile)
    # Separation(eventName,outfile)


