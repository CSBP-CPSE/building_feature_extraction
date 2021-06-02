import piexif
from PIL import Image
import os
from zipfile import ZipFile
import json
import pandas as pd
import pathlib
import shutil


def unzip_folder(path):
    with ZipFile(path, "r") as zipObj:
        zipObj.extractall()


def create_folder(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r"{0}".format(name))
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def classify_and_rename(input_dir):

    data = dict()

    with open("building_cat/annotations.json", encoding="utf-8") as data_file:
        data_dict = json.load(data_file)
        with open("building_cat/classes.json", encoding="utf-8") as class_file:
            class_dict = json.load(class_file)
            for key, val in data_dict.items():
                if key == "___sa_version___":
                    continue
                classId = data_dict[key]["instances"][0]["classId"]
                data[key] = class_dict[classId - 1]["name"]
            for key, val in data.items():
                set_exif_title(
                    pathlib.Path("{0}}/".format(input_dir) + key),
                    data[key],
                )

    for file in os.listdir(input_dir):

        if file.endswith(".csv"):
            file_name = file[:-4]
            _type = data[file_name + ".jpg"]
            df = pd.read_csv(input_dir + "/" + file)
            df.at[0, "File_Name"] = file_name[0:-10] + _type
            df.at[0, "Class"] = _type
            df.to_csv(input_dir + "/" + file, index=False)

        if file.endswith(".csv") or file.endswith(".jpg"):
            filename = file.replace("apartments", data[file[:-4] + ".jpg"])
        elif file.endswith(".json"):
            filename = file.replace("apartments", data[file[:-5] + ".jpg"])
        else:
            continue

        current_directory = os.getcwd()
        os.rename(
            r"{0}/{1}}/{2}".format(current_directory, input_dir, file),
            r"{0}/{1}}/{2}".format(current_directory, input_dir, filename),
        )


def organize_files(input_dir):
    input_dir = input_dir + "/"

    for filename in os.listdir(input_dir):

        if "condominium_apartment" in os.path.basename(filename):
            if not os.path.exists("condominium_apartment"):
                os.mkdir("condominium_apartment")
            shutil.move(input_dir + filename, "condominium_apartment/" + filename)

        elif "single_detached" in os.path.basename(filename):
            if not os.path.exists("single_detached"):
                os.mkdir("single_detached")
            shutil.move(input_dir + filename, "single_detached/" + filename)

        elif "prop_with_multiple_res_units" in os.path.basename(filename):
            if not os.path.exists("prop_with_multiple_res_units"):
                os.mkdir("prop_with_multiple_res_units")
            shutil.move(
                input_dir + filename, "prop_with_multiple_res_units/" + filename
            )

        elif "row_house" in os.path.basename(filename):
            if not os.path.exists("row_house"):
                os.mkdir("row_house")
            shutil.move(input_dir + filename, "row_house/" + filename)

        elif "semi_detached" in os.path.basename(filename):
            if not os.path.exists("semi_detached"):
                os.mkdir("semi_detached")
            shutil.move(input_dir + filename, "semi_detached/" + filename)

        elif "undetermined" in os.path.basename(filename):
            if not os.path.exists("undetermined"):
                os.mkdir("undetermined")
            shutil.move(input_dir + filename, "undetermined/" + filename)


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


unzip_folder("building_cat.zip")
unzip_folder("building_apartments_sample_100_v1.zip")

classify_and_rename("building_apartments_sample_100_v1")
organize_files("building_apartments_sample_100_v1")
