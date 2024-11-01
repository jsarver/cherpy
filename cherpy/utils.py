import tkinter as tk
from tkinter import filedialog
import attr
import csv
from loguru import logger


def get_save_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=(("csv file", "*.csv"), ("All Files", "*.*")))
    return file_path


def get_open_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


@attr.s
class NameValueExtractor(object):
    """takes a response object and returns a data dict"""
    response = attr.ib()

    def create_dict(self):
        dict_list = []
        data = self.response.json()
        for obj in data["businessObjects"]:
            dict_list.append({field["name"]: field["value"] for field in obj["fields"]})
        return dict_list


def dict_to_csv(my_dict, columns, filename, **kwargs):
    mode = kwargs.get("filemode", 'w')
    logger.debug(f"writing to file {filename}")
    with open(filename, mode, newline='') as out_file:
        w = csv.DictWriter(out_file, columns)
        w.writeheader()
        for d in my_dict:
            w.writerow(d)


def create_temp_file(value_pairs, file_name):
    columns = value_pairs[::2]
    values = value_pairs[1::2]

    with open(file_name, 'w') as outf:
        outf.write(",".join(columns) + "\n")
        outf.write(",".join(values) + "\n")
