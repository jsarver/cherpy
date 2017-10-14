import tkinter as tk
from tkinter import filedialog

import attr


def get_save_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(("csv file", "*.csv"),("All Files", "*.*")))
    return file_path

def get_open_file_path():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


@attr.s
class NameValueExtractor(object):
    response = attr.ib()

    def create_dict(self):
        dict_list = []
        data = self.response.json()
        for obj in data["businessObjects"]:
            dict_list.append({field["name"]: field["value"] for field in obj["fields"]})
        return dict_list