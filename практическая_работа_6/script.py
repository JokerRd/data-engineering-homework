import pandas as pd
import model
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(path_to_csv_file: str, threshold_mb: int = 250, chunksize: int = 200000) -> pd.DataFrame:
    file_size = os.path.getsize(path_to_csv_file)
    file_size_in_mb = (file_size / 1024) / 1024
    if file_size_in_mb > threshold_mb:
        for chunk in pd.read_csv(path_to_csv_file, chunksize=chunksize):
            return chunk
    return pd.read_csv(path_to_csv_file)


def load_opt_data_by_chunk(path_to_csv_file: str, dtype: dict, names_columns: list[str]):
    return pd.read_csv(path_to_csv_file, dtype=dtype, usecols=names_columns, chunksize=10000)


def analyze_memory_usage(path_to_file: str, data: pd.DataFrame, label: str) -> model.DataAnalysis:
    total_disk = os.path.getsize(path_to_file)
    data_memory_usage = data.memory_usage(index=False, deep=True)
    total_ram = int(data_memory_usage.sum())
    columns_analysis = analyze_columns(data, data_memory_usage, total_ram)
    return model.DataAnalysis(total=model.MemoryUsage(disk=total_disk, ram=total_ram),
                              columns=columns_analysis, comment=label)


def analyze_columns(data: pd.DataFrame,
                    memory_usage: pd.Series,
                    total_ram: int) -> dict[str, model.ColumnAnalysis]:
    types = data.dtypes
    items = memory_usage.items()
    column_analysis_tuples = map(lambda item: analyze_column(item, types, total_ram), items)
    return dict(column_analysis_tuples)


def analyze_column(one_column_memory_usage: (str, int),
                   types: pd.Series,
                   total_ram: int) -> (str, model.ColumnAnalysis):
    name_column = one_column_memory_usage[0]
    type_column = str(types[name_column])
    ram_column = int(one_column_memory_usage[1])
    ram_percent_of_total_column = round(ram_column / total_ram, 4)
    return name_column, model.ColumnAnalysis(ram=ram_column,
                                             type=type_column,
                                             ram_fraction_of_total=ram_percent_of_total_column)


def sort_by_ram(data: model.DataAnalysis) -> model.DataAnalysis:
    data.columns = dict(sorted(data.columns.items(), key=lambda item: item[1].ram, reverse=True))
    return data


def save_to_file(data, encoder, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, cls=encoder, indent=4)


def transform_obj_to_category(data: pd.DataFrame) -> pd.DataFrame:
    names_columns_for_transform = get_name_columns_for_transform(data)
    columns_for_transform = data.loc[:, names_columns_for_transform].columns.tolist()
    for column in columns_for_transform:
        data[column] = data[column].astype('category')
    return data


def get_name_columns_for_transform(data: pd.DataFrame) -> list[str]:
    object_columns = data.select_dtypes(include='object')
    count_by_columns = object_columns.count(axis='rows')
    unique_by_columns = object_columns.nunique(axis='rows')
    unique_percent_of_total_by_columns = unique_by_columns / count_by_columns
    filtered_unique_value_by_columns = unique_percent_of_total_by_columns.loc[unique_percent_of_total_by_columns < 0.5]
    return list(filtered_unique_value_by_columns.index)


def downcast_int(data: pd.DataFrame) -> pd.DataFrame:
    int_types = data.select_dtypes(include=['int'])
    negative_column = int_types.lt(0, axis='rows').any(axis='rows')
    negative_column_names = set(negative_column.loc[negative_column].index)
    positive_column_names = set(int_types.columns.tolist()) - set(negative_column_names)
    if len(negative_column_names) == 0:
        downcast(data, positive_column_names, 'unsigned')
    else:
        downcast(data, negative_column_names, 'signed')
        downcast(data, positive_column_names, 'unsigned')
    return data


def downcast_float(data: pd.DataFrame) -> pd.DataFrame:
    float_types = data.select_dtypes(include=['float'])
    float_column_names = set(float_types.columns.tolist())
    downcast(data, float_column_names, 'float')
    return data


def downcast(data: pd.DataFrame, names: set[str], downcast):
    for column in names:
        data[column] = pd.to_numeric(data[column], downcast=downcast, errors='coerce')


def get_filtered_column_types_by_name_column(data: pd.DataFrame, need_names_columns: list[str]) -> dict:
    return data[need_names_columns].dtypes.to_dict()


def load_and_save_optimize_data(path_to_csv_file: str, path_save_file: str,
                                data: pd.DataFrame, select_opt_columns: list[str]):
    filtered_columns_types = get_filtered_column_types_by_name_column(data, select_opt_columns)
    header = True
    for chunk in load_opt_data_by_chunk(path_to_csv_file, filtered_columns_types, select_opt_columns):
        chunk.to_csv(path_save_file, mode='a', header=header, index=False)
        header = False


def build_line_chart(data: pd.DataFrame, group_name_column: str, name_column: str, name_file: str):
    plt.figure(figsize=(20, 7))
    data.groupby(group_name_column)[name_column].mean().plot(legend=True)
    plt.savefig(f'{name_file}_line_chart.png')
    plt.clf()


def build_bar_chart(data: pd.DataFrame, name_column: str, name_file: str):
    plt.figure(figsize=(20, 7))
    (data[name_column].value_counts()
     .sort_values(ascending=False)
     .head(20)
     .plot(kind='bar', title='Most 20 high count value', legend=True))
    plt.savefig(f'{name_file}_bar_chart.png')
    plt.clf()


def build_pie_chart(data: pd.DataFrame, name_column: str, name_file: str):
    plt.figure(figsize=(10, 10))
    (data[name_column].value_counts()
     .sort_values(ascending=False)
     .head(10)
     .plot(kind='pie', title=name_column, autopct='%.2f%%'))
    plt.savefig(f'{name_file}_pie_chart.png')
    plt.clf()


def build_box_chart(data: pd.DataFrame, name_column_x: str, name_column_y: str, name_file: str):
    sns.boxplot(data=data, x=name_column_x, y=name_column_y)
    plt.savefig(f'{name_file}_box_chart.png')
    plt.clf()


def build_heatmap_chart(data: pd.DataFrame, name_file: str):
    plt.figure(figsize=(10, 10))
    sns.heatmap(data.corr(numeric_only=True))
    plt.savefig(f'{name_file}_heatmap.png')
    plt.clf()


def build_graphics(data: pd.DataFrame, name_file: str, parameters: model.ChartParameters):
    build_line_chart(data, parameters.line_chart_group_name_column, parameters.line_chart_name_column, name_file)
    build_bar_chart(data, name_column=parameters.bar_chart_name_column, name_file=name_file)
    build_box_chart(data, name_column_x=parameters.box_chart_x_name_column,
                    name_column_y=parameters.box_chart_y_name_column, name_file=name_file)
    build_pie_chart(data, name_column=parameters.pie_chart_name_column, name_file=name_file)
    build_heatmap_chart(data, name_file=name_file)


def start(path_to_csv_file, select_opt_columns, parameters):
    # step 1
    basename, extension = os.path.splitext(path_to_csv_file)
    data = load_data(path_to_csv_file)

    # step 2
    memory_analysis = analyze_memory_usage(path_to_csv_file, data, 'Not optimized data')

    # step 3
    sorted_memory_analysis = sort_by_ram(memory_analysis)
    save_to_file(sorted_memory_analysis, model.DataAnalysisEncoder, f'{basename}_stat_for_not_optimized_data.json')

    # step 4
    transformed_data = transform_obj_to_category(data)

    # step 5+
    downcast_int_data = downcast_int(transformed_data)

    # step 6
    downcast_float_data = downcast_float(downcast_int_data)

    # step 7
    memory_analysis_optimized_data = analyze_memory_usage(path_to_csv_file, downcast_float_data, 'Optimized data')
    sorted_memory_analysis_optimized_data = sort_by_ram(memory_analysis_optimized_data)
    save_to_file(sorted_memory_analysis_optimized_data,
                 model.DataAnalysisEncoder,
                 f'{basename}_stat_for_optimized_data.json')

    # step 8
    path_opt_data = f'{basename}_optimized_data.csv'
    load_and_save_optimize_data(path_to_csv_file, path_opt_data, downcast_float_data, select_opt_columns)

    # step 9
    opt_data = load_data(path_opt_data)
    build_graphics(opt_data, basename, parameters)


# select_columns = ['number_of_game', 'day_of_week', 'v_name', 'v_score',
#                   'v_league', 'h_name', 'h_score', 'h_league', 'length_minutes', 'protest']
# start('[1]game_logs.csv', select_columns,
#       model.ChartParameters(line_chart_name_column='length_minutes',
#                             line_chart_group_name_column='day_of_week',
#                             bar_chart_name_column='v_name',
#                             pie_chart_name_column='day_of_week',
#                             box_chart_x_name_column='v_score',
#                             box_chart_y_name_column='day_of_week'))


# second_select_columns = ['msrp', 'askPrice', 'isNew', 'color',
#                          'brandName', 'modelName', 'stockNum', 'firstSeen', 'lastSeen',
#                          'vf_TransmissionStyle']
# start("[2]automotive.csv.zip", second_select_columns,
#       model.ChartParameters(line_chart_name_column='askPrice',
#                             line_chart_group_name_column='brandName',
#                             bar_chart_name_column='modelName',
#                             pie_chart_name_column='brandName',
#                             box_chart_x_name_column='askPrice',
#                             box_chart_y_name_column='vf_TransmissionStyle'))

# third_select_columns = ['YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK',
#                         'AIRLINE', 'DESTINATION_AIRPORT', 'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'AIR_TIME',
#                         'DISTANCE']
#
# start('[3]flights.csv', third_select_columns,
#       model.ChartParameters(line_chart_name_column='DISTANCE',
#                             line_chart_group_name_column='AIRLINE',
#                             bar_chart_name_column='AIRLINE',
#                             pie_chart_name_column='AIRLINE',
#                             box_chart_x_name_column='YEAR',
#                             box_chart_y_name_column='DAY_OF_WEEK'))

# fourth_select_columns = ['schedule_name', 'employer_name', 'type_name', 'salary_from',
#                         'salary_to', 'salary_currency', 'area_name', 'employment_name', 'name',
#                         'employer_trusted']
#
# start('[4]vacancies.csv.gz', fourth_select_columns,
#       model.ChartParameters(line_chart_name_column='salary_to',
#                             line_chart_group_name_column='type_name',
#                             bar_chart_name_column='area_name',
#                             pie_chart_name_column='area_name',
#                             box_chart_x_name_column='employment_name',
#                             box_chart_y_name_column='salary_to'))


# fifth_select_columns = ['name', 'H', 'diameter', 'albedo',
#                         'class', 'rms', 'prefix', 'pha', 'diameter_sigma',
#                         'epoch']
#
# start('[5]asteroid.zip', fifth_select_columns,
#       model.ChartParameters(line_chart_name_column='diameter',
#                             line_chart_group_name_column='class',
#                             bar_chart_name_column='class',
#                             pie_chart_name_column='class',
#                             box_chart_x_name_column='class',
#                             box_chart_y_name_column='albedo'))

sixth_select_columns = ['Brew_Date', 'Beer_Style', 'SKU', 'Fermentation_Time',
                        'Temperature', 'Alcohol_Content', 'Color', 'Total_Sales', 'Quality_Score',
                        'Brewhouse_Efficiency']

start('[6]Brewery_Operations.zip', sixth_select_columns,
      model.ChartParameters(line_chart_name_column='Total_Sales',
                            line_chart_group_name_column='Beer_Style',
                            bar_chart_name_column='Beer_Style',
                            pie_chart_name_column='Beer_Style',
                            box_chart_x_name_column='SKU',
                            box_chart_y_name_column='Alcohol_Content'))
