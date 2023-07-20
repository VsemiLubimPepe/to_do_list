import ijson
import os
from objective import Objective

STD_FILE_NAME = r"\todo_list.txt"
STD_DIR_PATH = r"..\todo_list_data"


def save_objs(obj_list, file_path):
    if file_path is None:
        file_path = STD_DIR_PATH

    if os.path.isdir(file_path):
        file_path += STD_FILE_NAME
    with open(file_path, "w") as save_file:
        save_file.write('[\n')
        for obj in obj_list[:-1]:
            save_file.write(obj.json_dump() + ",\n")
        save_file.write(obj_list[-1].json_dump() + "\n")
        save_file.write("]")


def read_objs(file_path):
    if file_path is None:
        file_path = STD_DIR_PATH

    if os.path.isdir(file_path):
        file_path += STD_FILE_NAME
    with open(file_path, "r") as read_file:
        for obj_data in ijson.items(read_file, "item"):
            obj = Objective(obj_data["creation_datetime"],
                            obj_data["deadline_date"],
                            obj_data["deadline_time"],
                            obj_data["obj_theme"],
                            obj_data["obj_task"])
            yield obj
