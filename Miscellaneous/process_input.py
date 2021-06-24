from datetime import datetime
import shutil
import os
import piexif
from PIL import Image
import json
import pandas as pd
import pathlib
import glob
from zipfile import ZipFile

# global variable for home directory
home = os.getcwd()

# Simple method to check if the input string contains a digit
def check_for_digit(str):
    return any(char.isdigit() for char in str)


def get_num_folder(path):
    folders = 0
    for _, dirnames, filenames in os.walk(path):
        folders += len(dirnames)
    return folders


def create_folder(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r"{0}".format(name))
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def unzip_file(zip_path, out_path=None):
    with open(zip_path, "rb") as fileobj:
        z = ZipFile(fileobj)
        z.extractall(out_path)
        z.close()
    os.remove(zip_path)


def create_workflow(input_dir):
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    shutil.copytree(input_dir, "main~" + date)

    for file in os.listdir("main~" + date):
        if file.endswith(".zip"):
            unzip_file("main~" + date + "/" + file, "main~" + date + "/" + file[:-4])
    return date


def classify_and_rename(input_dir):
    def modify_and_store(building_cat, output_accepted):
        data = dict()
        with open(building_cat + "/annotations.json", encoding="utf-8") as data_file:
            data_dict = json.load(data_file)
            with open(building_cat + "/classes.json", encoding="utf-8") as class_file:
                class_dict = json.load(class_file)
                for key, val in data_dict.items():
                    if key == "___sa_version___":
                        continue
                    classId = data_dict[key]["instances"][0]["classId"]
                    data[key] = class_dict[classId - 1]["name"]
                for key, val in data.items():
                    set_exif_title(
                        pathlib.Path("{0}/".format(output_accepted) + key), data[key]
                    )
        return data

    def rename(data, output_accepted):
        for file in os.listdir(output_accepted):

            if file.endswith(".csv"):
                file_name = file[:-4]
                _type = data[file_name + ".jpg"]
                df = pd.read_csv(output_accepted + "/" + file)
                df.at[0, "File_Name"] = file_name[: file_name.rfind("~") + 1] + _type
                df.at[0, "Class"] = _type
                df.to_csv(output_accepted + "/" + file, index=False)

            if file.endswith(".csv") or file.endswith(".jpg"):
                file_name = file[:-4]
                _type = data[file_name + ".jpg"]
                filename = file_name[: file_name.rfind("~") + 1] + _type + file[-4:]
            elif file.endswith(".json"):
                file_name = file[:-5]
                _type = data[file_name + ".jpg"]
                filename = file_name[: file_name.rfind("~") + 1] + _type + file[-5:]
            else:
                continue

            current_directory = os.getcwd()
            os.rename(
                r"{0}/{1}/{2}".format(current_directory, output_accepted, file),
                r"{0}/{1}/{2}".format(current_directory, output_accepted, filename),
            )

    os.chdir(input_dir)
    for i in range(get_num_folder(os.getcwd()) // 2):
        data = modify_and_store(
            "building_cat_" + str(i + 1), "output_accepted_" + str(i + 1)
        )
        rename(data, "output_accepted_" + str(i + 1))
    os.chdir(home)


def set_exif_title(image_file, exif_title):
    """
    Set an image's exif data title field to the given string
    Args:
        image_file (pathlib.Path): Path of image file
        exif_title (str): Exif data title will be set to this string
    Returns:
        None
    """
    im = Image.open(image_file)
    try:
        exif_dict = piexif.load(im.info["exif"])
    except Exception:
        zeroth_ifd = {piexif.ImageIFD.ImageDescription: exif_title}
        exif_dict = {"0th": zeroth_ifd}
        exif_bytes = piexif.dump(exif_dict)
    else:
        edit_entry = exif_dict["0th"]
        edit_entry[piexif.ImageIFD.ImageDescription] = exif_title
        exif_dict["0th"] = edit_entry
        exif_bytes = piexif.dump(exif_dict)
    finally:
        piexif.insert(exif_bytes, str(image_file))
        im.close()


def organize_files(input_dir):

    for foldername in os.listdir(input_dir):
        if "output_accepted" in foldername:

            for filename in os.listdir(input_dir + "/" + foldername):
                file = (
                    filename[:-4]
                    if filename.endswith(".csv") or filename.endswith(".jpg")
                    else filename[:-5]
                )
                _type = file[file.rfind("~") + 1 :]

                if not os.path.exists(input_dir + "/" + _type):
                    os.mkdir(input_dir + "/" + _type)

                shutil.move(
                    input_dir + "/" + foldername + "/" + filename,
                    input_dir + "/" + _type + "/" + filename,
                )


def place_in_corresponding_folder(date, dir_path):
    create_folder("output~" + date)
    create_folder("output~" + date + "/" + dir_path + "/csv")
    create_folder("output~" + date + "/" + dir_path + "/jpg")
    create_folder("output~" + date + "/" + dir_path + "/json")

    for file in os.listdir("main~" + date + "/" + dir_path):

        if file.endswith(".csv"):
            shutil.move(
                "main~" + date + "/" + dir_path + "/" + file,
                "output~" + date + "/" + dir_path + "/csv/" + file,
            )
        elif file.endswith(".jpg"):
            shutil.move(
                "main~" + date + "/" + dir_path + "/" + file,
                "output~" + date + "/" + dir_path + "/jpg/" + file,
            )
        elif file.endswith(".json"):
            shutil.move(
                "main~" + date + "/" + dir_path + "/" + file,
                "output~" + date + "/" + dir_path + "/json/" + file,
            )


def combine_all_csvs(dir_path, name, date):

    os.chdir("output~" + date + "/" + dir_path + "/csv/")
    file_extension = ".csv"
    all_filenames = [i for i in glob.glob(f"*{file_extension}")]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])

    files_in_directory = os.listdir(os.getcwd())
    filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
    for file in filtered_files:
        path_to_file = os.path.join(os.getcwd(), file)
        os.remove(path_to_file)

    combined_csv.to_csv(name + ".csv", index=False)
    os.chdir(home)


#######  MAIN  ##########

_date = create_workflow("input")
_main = "main~" + _date
classify_and_rename(_main)
organize_files(_main)

for folder in os.listdir(_main):
    if not (check_for_digit(folder)):
        place_in_corresponding_folder(_date, folder)
        combine_all_csvs(folder, folder[folder.rfind("~") + 1 :], _date)
