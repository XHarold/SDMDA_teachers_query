import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import json

teacher_data = []

college_ids = list(range(2017, 2039)) + [2063,2012]

# 遍历
for college_id in college_ids:
    url = (
    f"https://faculty.uestc.edu.cn/system/resource/tsites/advancesearch.jsp?"
    f"collegeid={college_id}&disciplineid=0&enrollid=0&pageindex=1&pagesize=16&"
    f"rankid=0&degreeid=0&honorid=0&pinyin=&profilelen=100&teacherName=&"
    f"searchDirection=&viewmode=8&viewid=225569&siteOwner=1362264394&"
    f"viewUniqueId=225569&showlang=zh_CN&ispreview=false&basenum=0&ellipsis=...&"
    f"alignright=false&productType=0&tutorType="
)
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找网页中的 JSON 格式的教师数据
    match = re.search(r'{"totalnum":\d+,"totalpage":\d+,"pageindex":\d+,"teacherData":\[\{.*\}\]}', soup.text, re.DOTALL)
    if match:
        json_text = match.group(0)
        teacher_json = json.loads(json_text)  # 将字符串转换为字典
        # 获取totalpage数量
        total_pages = teacher_json.get('totalpage', 1)
        
        # 遍历该学院的所有页面
        for page_index in range(1, total_pages + 1):
            page_url = (
            f"https://faculty.uestc.edu.cn/system/resource/tsites/advancesearch.jsp?"
            f"collegeid={college_id}&disciplineid=0&enrollid=0&pageindex={page_index}&"
            f"pagesize=16&rankid=0&degreeid=0&honorid=0&pinyin=&profilelen=100&"
            f"teacherName=&searchDirection=&viewmode=8&viewid=225569&siteOwner=1362264394&"
            f"viewUniqueId=225569&showlang=zh_CN&ispreview=false&basenum=0&ellipsis=...&"
            f"alignright=false&productType=0&tutorType=")
            page_response = requests.get(page_url)
            page_response.encoding = 'utf-8'
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            
            page_match = re.search(r'{"totalnum":\d+,"totalpage":\d+,"pageindex":\d+,"teacherData":\[\{.*\}\]}', page_soup.text, re.DOTALL)
            if page_match:
                page_json_text = page_match.group(0)
                page_teacher_json = json.loads(page_json_text)
                
                # 遍历当前页面中的教师数据
                for teacher in page_teacher_json['teacherData']:
                    name = teacher.get('name', '')
                    sex = teacher.get('sex', '')
                    prorank = teacher.get('prorank', '')
                    gtutor = teacher.get('gtutor', '')
                    doctorTutor = teacher.get('doctorTutor', '')
                    teacher_url = teacher.get('url', '')
                    picUrl = 'https://faculty.uestc.edu.cn' + teacher.get('picUrl', '')

                    teacher_data.append({
                        'name': name,
                        'collegeid': college_id,
                        'sex': sex,
                        'prorank': prorank,
                        'gtutor': gtutor,
                        'doctorTutor': doctorTutor,
                        'url': teacher_url,
                        'picUrl': picUrl
                    })
                
                print(f"College {college_id}, Page {page_index} processed.")

df = pd.DataFrame(teacher_data)

# 检查数据是否提取成功
print(df.head())

# 将数据保存为CSV文件
df.to_csv('teachers_data.csv', index=False, encoding='utf-8')
print("CSV file 'teachers_data.csv' created successfully.")
