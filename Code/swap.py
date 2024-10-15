# 替换学院id为学院名称
import pandas as pd

college_df = pd.read_csv('college_data.csv')
teachers_df = pd.read_csv('teachers_data.csv')

merged_df = pd.merge(teachers_df, college_df, left_on='collegeid', right_on='college_id', how='left')
final_df = merged_df[['name', 'college', 'sex', 'prorank', 'gtutor', 'doctorTutor', 'url', 'picUrl']]


final_df.to_csv('teachers_data.csv', index=False, encoding='utf-8')
print("teachers_data.csv successfully processed")
