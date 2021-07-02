import pandas
from pathlib import Path

outputs_folder_path = Path('outputs/musescore_1')

merged_dataframe = pandas.DataFrame()

for group_folder in outputs_folder_path.iterdir():
    print(group_folder)
    for artist_file in group_folder.iterdir():
        data = pandas.read_csv(artist_file)

        merged_dataframe = merged_dataframe.append(data)


merged_dataframe.to_csv('outputs/full_data.csv', index=False)