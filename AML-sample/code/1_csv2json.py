
import json
import pandas as pd
import os

###
# 输入：该层待爬取的可疑的洗钱账户列表csv
# 参数：当前案件名称eventName，当前案件层数depth
# 输出：该层待爬取的可疑的洗钱账户列表json给BlockchainSpider


depth = 1   # 当前数据的层数
eventName = 'DEGOandCocosExploiter'  # 改成事件的名称，自定义

types = "erc20,external,internal"  # 包含代币交易、外部和内部交易
src_addr_path = '../src_addr_token/'  # 存有起始地址集合的路径
spider_path = '../../BlockchainSpider/json/'  #改成自己BlockchainSpider的相关路径
if not os.path.exists(spider_path):
    os.makedirs(spider_path)

def csv_to_json(csv_file_name, types):
    csv_file = pd.read_csv(src_addr_path + csv_file_name + '.csv')
    addr_list = []
    for addr in csv_file['address']:
        print(addr)
        addr_dict = {}

        addr_dict["source"] = addr
        addr_dict["types"] = types
        addr_dict["fields"] = "hash,from,to,value,timeStamp,blockNumber,tokenSymbol,contractAddress,isError," \
                              "gasPrice,gasUsed"
        addr_dict["depth"] = 1

        addr_list.append(addr_dict)

    print("len(addr_list): ", len(addr_list))
    # return json.dumps(addr_list)
    with open(spider_path + csv_file_name + '.json', 'w+') as f:
        f.write(json.dumps(addr_list))


if __name__ == '__main__':
    csv_to_json(eventName + '_source_addr'+str(depth), types=types)
    # 接下来可以用cmd敲入命令行爬数据：
    # scrapy crawl txs.eth.bfs -a file=json/DEGOandCocosExploiter_source_addr0.json

