import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://faculty.uestc.edu.cn/jsjs.jsp?urltype=tree.TreeTempUrl&wbtreeid=1011'

# 发出HTTP请求
response = requests.get(url)
response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')

span_tag = soup.find('span', string='学院设置')
select_tag = span_tag.find_next('select', id="tsites_teacher_query_college_id")


college_data = []
# 提取学院ID和名称
for option in select_tag.find_all('option'):
    college_id = option.get('value').strip()  # 获取<option>标签的value属性
    college_name = option.text.strip().replace('|--', '').strip()  # 去掉前面的 "|--"

    # 过滤
    if college_id and college_id != " ":
        college_data.append({
            'college_id': college_id,
            'college': college_name
        })


df = pd.DataFrame(college_data)
df.to_csv('college_data.csv', index=False, encoding='utf-8')


