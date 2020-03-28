
import requests
from bs4 import BeautifulSoup
import io
import sys
import pandas as pd
from matplotlib import pyplot as plt


def get_urldata(url):
    # 目标URL
    #url = 'http://www.tianqihoubao.com/lishi/guangzhou/month/201901.html'
    # 获取网页源代码
    resp = requests.get(url)
    # 返回状态码200
    print(resp)
    html = resp.content.decode('gbk')
    # 数据提取
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    tr_list = soup.find_all('tr')
    # print(tr_list)
    dates, conditions, temp = [], [], []
    for data in tr_list[1:]:
        sub_data = data.text.split()
        # print(sub_data)
        dates.append(sub_data[0])
        conditions.append(''.join(sub_data[1:3]))
        temp.append(''.join(sub_data[3:6]))
    # print(temp)
    # 数据保存
    _data = pd.DataFrame()
    _data['日期'] = dates
    _data['天气情况'] = conditions
    _data['气温'] = temp
    return _data


data_month_1 = get_urldata('http://www.tianqihoubao.com/lishi/guangzhou/month/201901.html')
data_month_2 = get_urldata('http://www.tianqihoubao.com/lishi/guangzhou/month/201902.html')
data_month_3 = get_urldata('http://www.tianqihoubao.com/lishi/guangzhou/month/201903.html')

data = pd.concat([data_month_1, data_month_2, data_month_3]).reset_index(drop=True)
print(data)
data.to_csv('guangzhou_data.csv', index=False, encoding='utf-8')

# 数据可视化

# 解决中文问题
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号显示问题
plt.rcParams['axes.unicode_minus'] = False

data = pd.read_csv('guangzhou_data.csv')

# 数据处理

data['最高气温'] = data['气温'].str.split('/', expand=True)[0]
data['最低气温'] = data['气温'].str.split('/', expand=True)[1]

data['最高气温'] = data['最高气温'].map(lambda x:int(x.replace('℃', '')))
data['最低气温'] = data['最低气温'].map(lambda x:int(x.replace('℃', '')))

dates = data['日期']
highs = data['最高气温']
lows = data['最低气温']

# 画图
fig = plt.figure(dpi=128, figsize=(10, 6))

plt.plot(dates, highs, c='red', alpha=0.5)
plt.plot(dates, lows, c='blue', alpha=0.5)

plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.2)

# 图表格式
# 设置图形的格式
plt.title('2019第一季度天气', fontsize=24)
plt.xlabel('', fontsize=6)
fig.autofmt_xdate() # 绘制斜的日期标签，以免重叠
plt.ylabel('气温', fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=10)

# 修改刻度
plt.xticks(dates[::20])

# 显示每日最高气温折线图
plt.show()





