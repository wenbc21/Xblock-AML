import pandas as pd
import os
from decimal import Decimal
import shutil

###
# 输入：BlockchainSpider爬取的该层账户交易记录，以及账户列表csv
# 参数：当前案件名称eventName，当前案件层数depth
# 输出：大量交易的账户分到all_data_large文件夹后续处理，其他普通的洗钱账户分到all_data_token文件夹继续找下游洗钱账户
# 输出：补充普通的洗钱账户信息到当前的accounts-hacker.csv，大量交易账户存到large_addr_info.csv


depth = 1   # 当前数据的层数
eventName = 'DEGOandCocosExploiter'  # 改成事件的名称，自定义

large_size = 1000   # 大量交易的阈值
src_addr_path = '../src_addr_token/'  # 存有起始地址集合的路径
blockchainspider_path = '../../BlockchainSpider/data/'   #改成自己BlockchainSpider的相关路径
large_path = '../all_data_large/'   # 存有大量交易的账户文件夹
if not os.path.exists(large_path):
    os.makedirs(large_path)
raw_path = '../all_data_token/'  # 存有所有可疑的洗钱账户文件夹（和all_data_large是互斥的）
if not os.path.exists(raw_path):
    os.makedirs(raw_path)

# 获取案例以往的大量交易的账户列表
if os.path.exists(large_path+'large_addr_info.csv'):
    df_large_addr = pd.read_csv(large_path+'large_addr_info.csv')
else:
    df_large_addr = pd.DataFrame(columns=['address'])   # 存有大量交易的账户的列表（待处理）

# 获取案例以往的洗钱相关的账户列表
df_hacker = pd.read_csv('../reference_list/accounts-hacker.csv')

# 读取当前层的source地址文件
print("Classify accounts ing...")
df_src = pd.read_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.csv')

# 循环判断每一个账户
for i in df_src.index:
    addr = df_src.loc[i, 'address']
    file_name = addr + '.csv'
    if not os.path.exists(blockchainspider_path + file_name):
        print('num', i, ': ', addr, 'No File!!!')
    else:
        tx_file = pd.read_csv(blockchainspider_path + file_name)
        if len(tx_file) > large_size:  # 判为大量交易的账户
            print('num', i, ': ', addr,'LARGE ADDR')
            shutil.move(blockchainspider_path+file_name, large_path)  # 把blockchainspider爬的数据移动到对应文件夹
            df_large_addr = df_large_addr.append({'address':addr},ignore_index=True)
            df_hacker = df_hacker.append({'address': addr, 'name_tag': 'unknown service', 'label': 'unknown service'},
                             ignore_index=True)
        else:  # 判为普通的陌生账户
            print('num', i, ': ', addr,'Normal')
            shutil.move(blockchainspider_path+file_name, raw_path)  # 把blockchainspider爬的数据移动到对应文件夹
            # 添加到hacker列表中
            df_hacker = df_hacker.append({'address': addr, 'name_tag': 'ml_transit_'+str(depth), 'label': 'heist'},
                             ignore_index=True)


# 输出当前案例最新的大量交易的账户列表
df_large_addr.to_csv(large_path+'large_addr_info.csv', index=None) # 需要过滤的地址列表
df_hacker.to_csv('../reference_list/accounts-hacker.csv', index=None) # 洗钱相关的账户列表