import pandas as pd
import os

###
# 输入：分别输入all-tx.csv，all-normal-tx.csv和all-erc20-tx.csv
# 输出：分别输出三个输入交易记录对应的-address.csv

ref_path = '../reference_list/'
file_1 = pd.read_csv(ref_path + 'exchange-list.csv', encoding='utf-8')
file_2 = pd.read_csv(ref_path + 'wallet-list.csv')
file_3 = pd.read_csv(ref_path + 'accounts-hacker.csv')   # 事件的名称，即文件夹名称
file_4 = pd.read_csv(ref_path + 'ERC20TokenInfo.csv', encoding='ansi')
file_5 = pd.read_csv(ref_path + 'ERC721TokenInfo.csv', encoding='ansi')
file_6 = pd.read_csv(ref_path + 'dex_defi_labels.labelcloud.csv', encoding='utf-8')
file_7 = pd.read_csv(ref_path + 'addr_labels.csv', encoding='utf-8')


def discover_address_label(file_name, type_name):
    if os.path.exists(file_name) == False:
        print(file_name, 'Not exist!!!')
        return
    else:
        tx_file = pd.read_csv(file_name)

        tx_file = tx_file[tx_file['value'] != '0']

        #同时考虑from和to
        addr_from = tx_file['from']
        addr_to = tx_file['to']
        addr_join = pd.concat([addr_from,addr_to],axis=0, ignore_index=True)
        addr_join = addr_join.drop_duplicates() #data中一行元素全部相同时才去除
        addr_join = addr_join.reset_index(drop=True)
        test_file = pd.DataFrame(data=addr_join, columns=['address']) #,'nametag','label'

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

        # out_file.to_csv(eventName + 'dataset/all' + type_name + '-label.csv', index=None)
        test_file.to_csv('../dataset/all' + type_name + '-address.csv', index=None)

        no_label_addr = test_file[test_file['label'] == '']['address']
        print('len(no_label_addr): ', len(no_label_addr))
        return no_label_addr


if __name__ == '__main__':
    print('Testing... ')
    for type_name in ['-normal', '-erc20','']:
        discover_address_label(file_name='../dataset/all'+type_name+'-tx.csv', type_name=type_name)
