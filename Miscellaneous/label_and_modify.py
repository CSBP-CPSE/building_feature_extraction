import piexif
from PIL import Image
import os
from zipfile import ZipFile
import json


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

    with open("building_cat/annotations.json") as data_file:
        d = json.load(data_file)

        with open("building_cat/classes.json") as class_file:
            _d = json.load(class_file)

            for key, val in d.items():

                if key == "___sa_version___":
                    continue

                classId = d[key]["instances"][0]["classId"]
                data[key] = _d[classId - 1]["name"]

                set_exif_title("building_apartments_sample_50/" + key, data[key])

        class_file.close()
    data_file.close()

    # for filename in os.listdir(input_dir):
    #     if filename.endswith(".csv"):
    #         return


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
