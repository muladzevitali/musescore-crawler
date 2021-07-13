from pathlib import Path

import pandas


def drop_duplicates_from_dataframe(dataframe: pandas.DataFrame, column: str) -> pandas.DataFrame:
    dataframe = dataframe.drop_duplicates(subset=column)

    return dataframe


def drop_duplicates_in_folder(folder_path: Path, column: str) -> None:
    for file_path in folder_path.iterdir():
        dataframe = pandas.read_csv(file_path)
        dataframe = dataframe.drop_duplicates(subset=column)
        dataframe.to_csv(file_path, index=True)


def drop_duplicates_in_sub_folders(input_path: Path, column: str) -> None:
    if input_path.is_dir():
        for file_path in input_path.iterdir():
            drop_duplicates_in_sub_folders(file_path, column)
        return

    dataframe = pandas.read_csv(input_path)
    dataframe = dataframe.drop_duplicates(subset=column)
    dataframe.to_csv(input_path, index=True)


def merge_files_in_folder(folder_path: Path, output_file_path: Path) -> None:
    overall_dataframe = pandas.DataFrame()
    for file_path in folder_path.iterdir():
        if not file_path.name.endswith('csv'):
            continue
        dataframe = pandas.read_csv(file_path)

        overall_dataframe = overall_dataframe.append(dataframe)

    if output_file_path.is_dir():
        output_file_path = output_file_path.joinpath('overall.csv')

    overall_dataframe.to_csv(output_file_path, index=False)
