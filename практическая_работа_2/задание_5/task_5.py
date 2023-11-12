import pandas as pnd
import json
import msgpack
import pickle
import os


def transform_number_type_data_to_json(columns, item):
    index = item[0]
    element = item[1]
    return {columns[index]: {
        'min': element[0],
        'max': element[1],
        'avr': element[2],
        'sum': element[3],
        'std': element[4]}
    }


def calculate_frequency_category_type_and_transform_to_json(column, data_frame):
    frequency_occurrence = data_frame.loc[:, [column]].value_counts(normalize=True)
    return {column: frequency_occurrence.to_json()}


df = pnd.read_csv("Nutrition__Physical_Activity__and_Obesity_-_Behavioral_Risk_Factor_Surveillance_System.csv")

df = df.drop(columns=[
    'LocationAbbr',
    'LocationDesc',
    'Datasource',
    'Class',
    'StratificationID1',
    'StratificationCategoryId1',
    'Stratification1',
    'StratificationCategory1',
    'LocationID',
    'DataValueTypeID',
    'QuestionID',
    'TopicID',
    'ClassID',
    'GeoLocation',
    'Data_Value_Footnote',
    'Data_Value_Footnote_Symbol',
    'Data_Value_Alt',
    'Data_Value',
    'Data_Value_Type',
    'Data_Value_Unit',
    'Total',
    'Age(years)'
])

print(df.info())

number_type_columns = ['YearStart', 'YearEnd', 'Low_Confidence_Limit', 'High_Confidence_Limit ', 'Sample_Size']
category_type_columns = ['Topic', 'Question', 'Education', 'Gender', 'Income', 'Race/Ethnicity']

min_number_type = df.loc[:, number_type_columns].min(axis='index')
max_number_type = df.loc[:, number_type_columns].max(axis='index')
mean_number_type = df.loc[:, number_type_columns].mean(axis='index')
sum_number_type = df.loc[:, number_type_columns].sum(axis='index')
std_number_type = df.loc[:, number_type_columns].std(axis='index')

zipped_data = zip(min_number_type, max_number_type, mean_number_type, sum_number_type, std_number_type)
number_type_json_data = list(map(lambda item: transform_number_type_data_to_json(number_type_columns, item),
                                 enumerate(zipped_data)))


category_type_json_data = list(map(lambda item: calculate_frequency_category_type_and_transform_to_json(item, df),
                                   category_type_columns))

result_json_data = {'number_characteristic': number_type_json_data, 'category_characteristic': category_type_json_data}

with open("answer.json", 'w') as file:
    json.dump(result_json_data, file)

df.to_csv('answer_data.csv', index=False)

answer_json_data = df.to_json()
with open("answer_data.json", 'w') as file:
    json.dump(answer_json_data, file)

with open("answer_data.msgpack", 'wb') as file:
    msgpack.dump(answer_json_data, file)

with open("answer_data.pkl", "wb") as file:
    pickle.dump(answer_json_data, file)

answer_csv_size = os.path.getsize('answer_data.csv')
answer_json_size = os.path.getsize('answer_data.json')
answer_msgpack_size = os.path.getsize('answer_data.msgpack')
answer_pickle_size = os.path.getsize('answer_data.pkl')

print('csv: ' + str(answer_csv_size))
print('json: ' + str(answer_json_size))
print('msgpack: ' + str(answer_msgpack_size))
print('pickle: ' + str(answer_pickle_size))
