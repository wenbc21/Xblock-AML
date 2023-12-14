import pandas as pd
import requests

depth = 4   # 当前数据的层数
eventName = 'FakeMetadiumPresale'  # 改成事件的名称，自定义
src_addr_path = '../src_addr_token/'
df_src = pd.read_csv(src_addr_path + eventName + '_source_addr' + str(depth) + '.csv')

# 登录后改成自己的
headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.63"}
cookies={'cookie': '_pk_id.10.1f5c=2723c1d71d050b41.1657985498.; cf_clearance=foq8S_3MPSjo7dEhACXQ78mVzGl25CSbEbstOdzpcKw-1661222353-0-250; ASP.NET_SessionId=gheijdq45qf0fjosravvt5g4; _pk_ses.10.1f5c=1; __cf_bm=F6PtoIfigXx8XvosBw19_7_1uI9hmY.cB6Fev2306BQ-1661222358-0-ASVSCvjMoIDhfagvWij+epHZ1HrVxon6CwJhpp7QzCebsIyQEIzkBmAI9QL367Jd+g+Jk4vZswosy/9k12FXCzGSyNvxK4zjBTIAeDeuB8wNXkTC4Frv3ChQAL23b5RWTg=='}

title_list = ''
notitle_list = ''
count = 0
for add in df_src['address'] :
    url = 'https://cn.etherscan.com/address/' + add
    try :
        r = requests.post(url, headers=headers, cookies=cookies)
    except :
        print(f"breakpoint: {count}")
        break
    if r.status_code == 200 :
        r.encoding = 'UTF-8'
        begin = r.text.index('<title>')
        end = r.text.index(add)
        title = r.text[begin+10:end-1].split(' |')[0]
        print(title)
        if title != 'Address' and len(title) < 100:
            title_list += (add + ',' + title + '\n')
        else :
            notitle_list += (add + '\n')
        count += 1
    else :
        print(f"breakpoint: {count}")
        break
    # if count == 10 :
    #     break

f1 = open(src_addr_path + "title.csv", "a", encoding='utf-8')
f1.write(title_list)
f1.close()
f2 = open(src_addr_path + "notitle.csv", "a", encoding='utf-8')
f2.write(notitle_list)
f2.close()