import piexif
from PIL import Image
import os
from zipfile import ZipFile
import json
import pandas as pd
import pathlib


def unzip_folder(path):
    with ZipFile(path, "r") as zipObj:
        zipObj.extractall()


def create_folder(name):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r"".format(name))
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)


def add_to_folder(input_dir, output_dir):

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
                    pathlib.Path("building_apartments_sample_50/" + key),
                    data[key],
                )

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            df = pd.read_csv(input_dir + "/" + filename)
            file_name = filename[:-4]
            df.at[0, "File_Name"] = file_name[0:-10] + data[file_name + ".jpg"]
            df.at[0, "Class"] = data[file_name + ".jpg"]
            df.to_csv(input_dir + "/" + filename, index=False)


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


# unzip_folder("building_cat.zip")
# unzip_folder("building_apartments_sample.zip")
# create_folder("output")

add_to_folder("building_apartments_sample_50", "output")
