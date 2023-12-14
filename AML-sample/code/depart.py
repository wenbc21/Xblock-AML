import pandas as pd

depth = 9   # 当前数据的层数
eventName = 'DragonExHacker'  # 改成事件的名称，自定义
src_addr_path = '../src_addr_token/'
df_src = pd.read_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.csv')

address_list = []
count = 0
num = 1
for add in df_src['address'] :
    address_list.append(add)
    count += 1
    if count == 8000 :
        file_temp = pd.DataFrame()
        file_temp['address'] = address_list
        file_temp.to_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.' + str(num) + '.csv', index = False)
        num += 1
        count = 0
        address_list = []
file_temp = pd.DataFrame()
file_temp['address'] = address_list
file_temp.to_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.' + str(num) + '.csv', index = False)
