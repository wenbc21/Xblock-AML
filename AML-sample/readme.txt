准备：
- 确保中有code文件夹，reference_list文件夹和src_addr_token文件夹
- code文件夹代码中，涉及到BlockchainSpider的路径修改为自己的路径

step 0. 找到案件的新闻，在文档里面找到起始的账户，手敲到src_addr_token文件夹中的eventName_source_addr0.1.csv，这里的eventName是可以自己取的，例如'DEGOandCocosExploiter'

step 1. 运行1_csv2json.py
# 输入：该层待爬取的可疑的洗钱账户列表csv
# 参数：当前案件名称eventName，当前案件层数depth
# 输出：该层待爬取的可疑的洗钱账户列表json给BlockchainSpider
    # 接下来可以用cmd敲入命令行爬数据：
    # scrapy crawl txs.eth.bfs -a file=json/DEGOandCocosExploiter_source_addr0.json

step 2. 运行2_classify_accounts.py
# 输入：BlockchainSpider爬取的该层账户交易记录，以及账户列表csv
# 参数：当前案件名称eventName，当前案件层数depth
# 输出：大量交易的账户分到all_data_large文件夹后续处理，其他普通的洗钱账户分到all_data_token文件夹继续找下游洗钱账户
# 输出：补充普通的洗钱账户信息到当前的accounts-hacker.csv，大量交易账户存到large_addr_info.csv

step 3. 运行3_discover_address_token-0714.py
# 输入：该层的可疑洗钱账户列表和交易记录，已知标签文件
# 参数：当前案件名称eventName，当前案件层数depth
# 输出：下一层待爬取的可疑的洗钱账户列表

重新执行step 1-3，注意修改depth参数，直到没有下一层，跳出循环，爬虫结束

step 4. 运行4_filter_large_account.py
# 输入：大量交易的账户的all_data_large文件夹，大量交易账户列表large_addr_info.csv
# 输出：只保留和上游洗钱账户一周的交易记录addr_filter.csv，放到all_data_token文件夹

step 5. 运行5_merge_csv.py
# 输入：all_data_token文件夹，包括了所有可疑账户的交易记录
# 输出：合并为all-tx.csv，同时划分为all-normal-tx.csv和all-erc20-tx.csv

step 6. 运行6_filter_label_final.py
# 输入：分别输入all-tx.csv，all-normal-tx.csv和all-erc20-tx.csv
# 输出：分别输出三个输入交易记录对应的-address.csv

备注：如果爬虫过程发现漏了账户的交易，可以用check_file.py检查漏了哪些

