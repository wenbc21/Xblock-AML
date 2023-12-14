import pandas as pd
import os

###
# 非必要步骤
# 如果发现有少了的账户交易记录，则运行该代码检查遗漏了哪些，生成新的待爬账户列表csv

depth = 0   # 当前数据的层数
eventName = 'DEGOandCocosExploiter'  # 改成事件的名称，自定义
src_addr_path = '../src_addr_token/'
raw_path = '../../BlockchainSpider/data/'

next_addr_list = []

if __name__ == '__main__':
    df_src = pd.read_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.csv')
    next_addr_file = pd.DataFrame(columns=['address'])
    print(" no file!")
    for i in range(len(df_src)):
        addr = df_src.loc[i, 'address']
        if os.path.exists(raw_path+addr+'.csv') == False:
            print(addr)
            next_addr_list.append(addr)
    print('(len(next_addr_list)', len(next_addr_list))
    if len(next_addr_list) > 0 :
        df_left = pd.DataFrame(next_addr_list, columns=['address'])
        df_left.to_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.0.csv', index=None)
