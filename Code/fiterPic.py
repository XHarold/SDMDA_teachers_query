# 筛选图片
import pandas as pd

df = pd.read_csv('teachers_data.csv')

# 过滤掉空白的图片URL
filtered_df = df[df['picUrl'] != 'https://faculty.uestc.edu.cn/__local/1/21/08/AE9986A0EC249484A97EB5885D6_608FBC5C_58E8.jpg']


filtered_df.to_csv('filtered_teachers_data.csv', index=False, encoding='utf-8')
print("CSV file 'filtered_teachers_data.csv' created successfully.")
