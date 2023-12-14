import sys

import pandas as pd
import os

###
# 输入：大量交易的账户的all_data_large文件夹，大量交易账户列表large_addr_info.csv
# 输出：只保留和上游洗钱账户一周的交易记录addr_filter.csv，放到all_data_token文件夹

WEEK_SEC = 604800           # 一周的秒数
large_path = '../all_data_large/'      # 需要过滤的大文件夹
raw_path = '../all_data_token/'        # 输出的文件夹
file_name = large_path+'large_addr_info.csv'   # 需要过滤的地址列表
df_account = pd.read_csv(file_name)
if len(df_account) == 0:
    print('No large files! Finished')
    sys.exit(0)
ref_path = '../reference_list/'
label_file = ref_path + '/accounts-hacker.csv'  # 存有洗钱节点的列表

if os.path.exists(file_name) == False:
    print(file_name, 'Not exist!!!')

for addr in df_account['address']:
    # 获取其交易文件
    print(addr)
    tx_file = pd.read_csv(large_path+addr+'.csv')
    tx_file[['value']] = tx_file[['value']].astype(float)  # 转换value这一列的金额
    tx_file = tx_file.sort_values(by='timeStamp')           # 按照时间顺序排列
    # print(tx_file)
    print('Origin len: ', len(tx_file))

    # 读取标签，选出洗钱节点
    label = pd.read_csv(label_file)
    heist = list(label[label['label'] == 'heist']['address'])
    # print('heist', heist)

    # 所有从洗钱节点往下游大节点的交易都被保留
    related = tx_file[tx_file['from'].isin(heist)]
    if len(related) == 0:
        print('len(related): 0 !!!!!')
    else:
        tx_file_1 = related
        # 筛选out-going的交易，根据First In First Out (FIFO)的原则，选择一周
        start_time = min(related[related['to'] == addr]['timeStamp']) # 第一笔转入的交易时间
        end_time = max(related[related['to'] == addr]['timeStamp'])   # 最后的转入的交易时间
        tx_file_out = tx_file[tx_file['from'] == addr]
        # 选择start_time≤ x ≤ end_time+week
        tx_file_2 = tx_file_out[(tx_file_out['timeStamp'] >= start_time) & (tx_file_out['timeStamp'] <= end_time + WEEK_SEC)]

        # 拼接in-coming和out-going的交易
        tx_file = pd.concat([tx_file_1, tx_file_2])
        print("After filter, len: ", len(tx_file))
        print('----------')
        tx_file.to_csv(raw_path+ addr + '_filter.csv', index=None)
        # tx_file.to_csv(eventName+raw_path+ addr + '_filter_tmp.csv', index=None)

