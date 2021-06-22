from zipfile import ZipFile
import os
import shutil
import glob
import pandas as pd
import csv


def unzip_folder(zip_path, out_path=None):
    with ZipFile(zip_path, "r") as zipObj:
        zipObj.extractall(out_path)


def create_folder(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r"{0}".format(name))
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def fix_csv_name(dir_path):
    for file in os.listdir(dir_path):
        if file.endswith(".csv"):
            r = csv.reader(open(dir_path + "/" + file))
            lines = list(r)
            lines[1][0] = file[:-4]
            writer = csv.writer(open(dir_path + "/" + file, "w"))
            writer.writerows(lines)


def place_in_corresponding_folder(dir_path):

    create_folder(dir_path + "/csv")
    create_folder(dir_path + "/jpg")
    create_folder(dir_path + "/json")

    for file in os.listdir(dir_path):

        if file.endswith(".csv"):
            shutil.move(dir_path + "/" + file, dir_path + "/" + "csv/" + file)
        elif file.endswith(".jpg"):
            shutil.move(dir_path + "/" + file, dir_path + "/" + "jpg/" + file)
        elif file.endswith(".json"):
            shutil.move(dir_path + "/" + file, dir_path + "/" + "json/" + file)


def combine_all_csvs(dir_path, name):

    os.chdir(dir_path)
    file_extension = ".csv"
    all_filenames = [i for i in glob.glob(f"*{file_extension}")]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    files_in_directory = os.listdir(os.getcwd())
    filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
    for file in filtered_files:
        path_to_file = os.path.join(os.getcwd(), file)
        os.remove(path_to_file)

    combined_csv.to_csv(name + ".csv", index=False)


unzip_folder("...")
fix_csv_name("...")
place_in_corresponding_folder("...")
combine_all_csvs("...")
