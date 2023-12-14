import pandas as pd
import os
from decimal import Decimal
import shutil

###
# 输入：该层的可疑洗钱账户列表和交易记录，已知标签文件
# 参数：当前案件名称eventName，当前案件层数depth
# 输出：下一层待爬取的可疑的洗钱账户列表

depth = 1   # 当前数据的层数
eventName = 'DEGOandCocosExploiter'  # 改成事件的名称，自定义
event_time = 1644449357
   # 需要手动输入起始时间

raw_path = '../all_data_token/'  # '../all_data_token/'+str(depth)+'/'
large_path = '../all_data_large/'
src_addr_path = '../src_addr_token/'
filter_path = '../filter_labels_token/' # 输出中间结果，人工排查用
if not os.path.exists(filter_path):
    os.makedirs(filter_path)

ref_path = '../reference_list/'

file_1 = pd.read_csv(ref_path + 'exchange-list.csv', encoding='utf-8')
file_2 = pd.read_csv(ref_path + 'wallet-list.csv')
file_3 = pd.read_csv(ref_path + 'accounts-hacker.csv')
file_4 = pd.read_csv(ref_path + 'ERC20TokenInfo.csv', encoding='ansi')
file_5 = pd.read_csv(ref_path + 'ERC721TokenInfo.csv', encoding='ansi')
file_6 = pd.read_csv(ref_path + 'dex_defi_labels.labelcloud.csv', encoding='utf-8')
file_7 = pd.read_csv(ref_path + 'addr_labels.csv', encoding='utf-8')

def wei2ether(s) -> Decimal:
    """
    'value'的字符串转数值
    """
    length = len(s)
    t = length - 18
    if t > 0:
        s1 = ""
        s1 = s1 + s[0:t]
        s1 = s1 + "."
        s1 = s1 + s[t:]
    else:
        x = 18 - length
        s1 = "0."
        for i in range(0, x):
            s1 = s1 + "0"
        s1 = s1 + s
    return Decimal(s1)

def discover_address_label(file_name, large_addr=False):
    print("discover_address_label...")
    if os.path.exists(raw_path + file_name) == False:
        print("no file!")
        return
    else:
        tx_file = pd.read_csv(raw_path + file_name)

        # 获取满足时序递增要求的下游账户                
        tx_file = tx_file[tx_file['value'] != '0']
        # 读取标签，选出洗钱节点
        heist = list(file_3[file_3['label'] == 'heist']['address'])
        # print('heist', heist)

        # 所有从洗钱节点往下游大节点的交易都被保留
        related = tx_file[tx_file['from'].isin(heist)]
        if len(related) == 0:
            print('len(related): 0 !!!!! ERROR')
        else:
            print('related (previous heist)')
            print(related)
            try:
                start_time = min(related[related['to'] == addr]['timeStamp']) # 第一笔转入的交易时间
            except:
                start_time = event_time # 最早的一笔交易/被攻击的交易的时间

            # # 计算累积收到黑钱金额
            # for i in related.index:
            #     related.loc[i, 'value'] = wei2ether(related.loc[i,'value'])
            # heist_coin = sum(related[related['to'] == addr]['value'])     # 该账户由上游黑钱转入的金额
            # print('heist_coin:', heist_coin)
            tx_file = tx_file[tx_file['timeStamp'] >= start_time]     # 只保留时间大于最早的第一笔转入黑钱的交易

        # # 根据金额原则筛选下游交易
        # tx_file.reset_index()
        # transferred = 0
        # for i in tx_file.index:
        #     if (heist_coin-transferred>0.1):
        #         transferred += related.loc[i, 'value']
        #     else:
        #         tx_file = tx_file.loc[0:i,:]
        #         break
        # print('tx_file')
        # print(tx_file)
        #

        test_file = pd.DataFrame(data=list(set(tx_file['to'])), columns=['address'])  # ,'nametag','label'
        test_file['name_tag'] = ''
        test_file['label'] = ''

        out_file = pd.DataFrame(columns=['address', 'name_tag', 'label'])

        for i in range(len(test_file)):
            # test_file['address'][i] = test_file['address'][i][:-2]
            # print(str(i) + " " + test_file['address'][i])

            tag1 = file_1[file_1['address'] == test_file['address'][i]]
            tag1 = tag1.reset_index(drop=True)
            if len(tag1) != 0:
                print('file_1, ok')
                test_file.loc[i, 'name_tag'] = tag1['name_tag'][0]
                test_file.loc[i, 'label'] = tag1['label'][0]
                new1 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag1['name_tag'][0], 'label': tag1['label'][0]})
                out_file = out_file.append(new1, ignore_index=True)
                continue

            tag2 = file_2[file_2['address'] == test_file['address'][i]]
            tag2 = tag2.reset_index(drop=True)
            if len(tag2) != 0:
                print('file_2, ok')
                test_file.loc[i, 'name_tag'] = tag2['name_tag'][0]
                test_file.loc[i, 'label'] = tag2['label'][0]
                new2 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag2['name_tag'][0], 'label': tag2['label'][0]})
                out_file = out_file.append(new2, ignore_index=True)
                continue

            tag3 = file_3[file_3['address'] == test_file['address'][i]]
            tag3 = tag3.reset_index(drop=True)
            if len(tag3) != 0:
                print('file_3, ok')
                test_file.loc[i, 'name_tag'] = tag3['name_tag'][0]
                test_file.loc[i, 'label'] = tag3['label'][0]
                new3 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag3['name_tag'][0], 'label': tag3['label'][0]})
                out_file = out_file.append(new3, ignore_index=True)
                continue

            tag4 = file_4[file_4['address'] == test_file['address'][i]]
            tag4 = tag4.reset_index(drop=True)
            if len(tag4) != 0:
                print('file_4, ok')
                test_file.loc[i, 'name_tag'] = tag4['name_tag'][0]
                test_file.loc[i, 'label'] = 'erc20'
                new4 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag4['name_tag'][0], 'label': 'erc20'})
                out_file = out_file.append(new4, ignore_index=True)
                continue

            tag5 = file_5[file_5['address'] == test_file['address'][i]]
            tag5 = tag5.reset_index(drop=True)
            if len(tag5) != 0:
                print('file_5, ok')
                test_file.loc[i, 'name_tag'] = tag5['name_tag'][0]
                test_file.loc[i, 'label'] = 'erc721'
                new5 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag5['name_tag'][0], 'label': 'erc721'})
                out_file = out_file.append(new5, ignore_index=True)
                continue

            tag6 = file_6[file_6['address'] == test_file['address'][i]]
            tag6 = tag6.reset_index(drop=True)
            if len(tag6) != 0:
                print('file_6, ok')
                test_file.loc[i, 'name_tag'] = tag6['name_tag'][0]
                test_file.loc[i, 'label'] = 'dex_defi'
                new6 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag6['name_tag'][0], 'label': 'dex_defi'})
                out_file = out_file.append(new6, ignore_index=True)
                continue

            tag7 = file_7[file_7['address'] == test_file['address'][i]]
            tag7 = tag7.reset_index(drop=True)
            if len(tag7) != 0:
                print('file_7, ok')
                test_file.loc[i, 'name_tag'] = tag7['name_tag'][0]
                test_file.loc[i, 'label'] = tag7['label'][0]
                new7 = pd.Series(
                    {'address': test_file['address'][i], 'name_tag': tag7['name_tag'][0], 'label': tag7['label'][0]})
                out_file = out_file.append(new7, ignore_index=True)
                continue

        # out_file.to_csv(filter_path + file_name + '_label.csv', index=False)
        test_file.to_csv(filter_path + file_name + '_address.csv', index=False)

        no_label_addr = test_file[test_file['label'] == '']['address']
        print('len(no_label_addr): ', len(no_label_addr))
        return no_label_addr


if __name__ == '__main__':
    print('Testing... ')
    # # test 1
    # discover_address_label('all-normal-tx.csv')

    #test 2 (单独一个文件夹)
    # for file_name in os.listdir(r'E:\OneDrive - 中山大学\Coding\AML-Defi\\'+raw_path):
    #     discover_address_label(file_name)

    # test 3 (有src文档的情况)
    df_src = pd.read_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.csv')
    #next_addr_file = pd.DataFrame(columns=['address'])
    next_addr_file = pd.DataFrame()
    for i in range(len(df_src)):
        addr = df_src.loc[i, 'address']
        print('---------------------------------------------------')
        print('num', i, ': ', addr, '.csv')
        next_addr = discover_address_label(addr + '.csv', large_addr=True)
        if (type(next_addr) != 'NoneType'):
            print('next_addr')
            print(next_addr)
            next_addr_file = pd.concat([next_addr_file, next_addr])
            # next_addr_file = pd.concat([next_addr_file, next_addr], axis=0, ignore_index=True)
            # next_addr_file = next_addr_file.append(next_addr, ignore_index=True)

    next_addr_file = next_addr_file.drop_duplicates()  # data中一行元素全部相同时才去除
    next_addr_file = next_addr_file.reset_index(drop=True)
    next_addr_file = next_addr_file.rename(columns={0:'address'})

    print('len(next_addr_file)', len(next_addr_file))
    if len(next_addr_file) == 0:
        print('Congratulation! Finished!')
    else:
        next_addr_file.to_csv(src_addr_path + eventName + '_source_addr' + str(depth + 1) + '.csv', index=False)

