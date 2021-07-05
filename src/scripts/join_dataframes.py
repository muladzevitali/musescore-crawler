import pandas
from pathlib import Path

outputs_folder_path = Path(r'C:\Users\vmuladze\Projects\musescore-crawler\outputs\tmp')

merged_dataframe = pandas.DataFrame()


for artist_file in outputs_folder_path.iterdir():
    data = pandas.read_csv(artist_file)

    merged_dataframe = merged_dataframe.append(data)


merged_dataframe.to_csv('outputs/full_data.csv', index=False)