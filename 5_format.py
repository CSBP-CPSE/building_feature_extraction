#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import csv
import matplotlib.pyplot as plt


def get_city():
    # this method currently only returns Ottawa but in future implimentations might get the city based off the address
    return "Ottawa"


def get_province():
    # this method currently only returns Ottawa but in future implimentations might get the city based off the address
    return "Ontario"


def concatenate_address(in_file):

    data = dict()
    with open(in_file) as input:
        in_reader = csv.DictReader(input)
        for row in in_reader:
            data.setdefault(
                str(
                    [
                        row["addr:unit"],
                        row["addr:housenumber"],
                        row["addr:street"],
                        row["osm_obj_type"],
                        row["latitude"],
                        row["longitude"],
                    ]
                ),
                [],
            ).append(row["building"])

    with open("dict1.csv", "w") as out:
        writer = csv.writer(out)
        writer.writerow(
            [
                "building_address",
                "building_type",
                "osm_obj_type",
                "latitude",
                "longitude",
            ]
        )
        for key, val in data.items():
            key = eval(key)
            addr = (
                key[0]
                + " "
                + key[1]
                + " "
                + key[2]
                + ", "
                + get_city()
                + ", "
                + get_province()
                if key[0]
                else key[1] + " " + key[2] + ", " + get_city() + ", " + get_province()
            )
            writer.writerow(
                [addr, ", ".join([elem for elem in val]), key[3], key[4], key[5]]
            )


def create_type_files(in_file):
    with open(in_file) as fin:
        csvin = csv.DictReader(fin)
        # Category -> open file lookup
        outputs = {}
        for row in csvin:
            cat = row["building_type"]
            # Open a new file and write the header
            if "," in cat:
                cat = "unknown"

            if cat not in outputs:
                fout = open("{}.csv".format(cat), "w", newline="")
                dw = csv.DictWriter(fout, fieldnames=csvin.fieldnames)
                dw.writeheader()
                outputs[cat] = fout, dw
            # Always write the row
            outputs[cat][1].writerow(row)
        # Close all the files
        for fout, _ in outputs.values():
            fout.close()
        fin.close()


def type_histogram(in_file):
    df = pd.read_csv(in_file)
    # data.plot(kind='bar')
    # plt.ylabel('Amount in the Ottawa Region')
    # plt.xlabel('Residential Building Types')
    # plt.title('Residential Buildings in the Ottawa Region per type')

    df.loc[df["building_type"].str.contains(","), "building_type"] = "unknown"
    df["building_type"].hist()
    plt.show()


def count_duplicates(in_file):
    count = 0
    with open(in_file, "r") as input:
        reader = csv.reader(input)
        next(reader)
        for idx, row in enumerate(reader):
            count += len(row[1].split(","))
    return count


def get_duplicate_file(in_file):
    with open(in_file, "r") as input:
        reader = csv.reader(input)
        with open("unknown_separated.csv", "w") as out:
            writer = csv.writer(out)
            for idx, row in enumerate(reader):
                types = row[1].split(",")
                for _type in types:
                    writer.writerow([row[0], _type.strip(), row[2], row[3], row[4]])
            out.close()
        input.close()


concatenate_address("sample-input.csv")
create_type_files("dict.csv")
type_histogram("dict.csv")
count_duplicates("unknown.csv")
get_duplicate_file("unknown.csv")
