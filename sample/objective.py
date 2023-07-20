from datetime import date, datetime, timedelta
from textwrap import wrap
import json

STD_TIME = "00:00"
ROW_LEN = 78
VAL_COL_LEN = 68
FIELD_COL_LEN = 8


class Objective:
    class ObjectiveEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Objective):
                return {
                    "creation_datetime": obj.creation_datetime,
                    "deadline_date": obj.deadline_date,
                    "deadline_time": obj.deadline_time,
                    "obj_theme": obj.obj_theme,
                    "obj_task": obj.obj_task
                }
            return json.JSONEncoder.default(self, obj)

    def __init__(
            self,
            creation_datetime: str = None,
            deadline_date: str = None,
            deadline_time: str = None,
            obj_theme: str = None,
            obj_task: str = None
    ):
        self._creation_datetime = None
        self._deadline_date = None
        self._deadline_time = None
        self._obj_theme = obj_theme
        self._obj_task = obj_task
        self._obj_complete = False
        if creation_datetime:
            self.creation_datetime = creation_datetime
        if deadline_date:
            self.deadline_date = deadline_date
        if deadline_time:
            self.deadline_time = deadline_time

    @property
    def creation_datetime(self):
        if self._creation_datetime is None or self._creation_datetime == "":
            self._creation_datetime = datetime.today()
        return self._creation_datetime.strftime("%d-%m-%Y %H:%M")

    @creation_datetime.setter
    def creation_datetime(self, creation_datetime_str):
        self._creation_datetime = datetime.strptime(creation_datetime_str,
                                                    "%d-%m-%Y %H:%M")

    @property
    def deadline_time(self):
        if self._deadline_time is None or self._deadline_time == "":
            self._deadline_time = datetime.strptime(STD_TIME, "%H:%M")
        return self._deadline_time.strftime("%H:%M")

    @deadline_time.setter
    def deadline_time(self, deadline_time_str):
        self._deadline_time = datetime.strptime(deadline_time_str,
                                                "%H:%M").time()

    @property
    def deadline_date(self):
        if self._deadline_date is None or self._deadline_date == "":
            self._deadline_date = date.today() + timedelta(1)
        return self._deadline_date.strftime("%d-%m-%Y")

    @deadline_date.setter
    def deadline_date(self, deadline_date_str):
        self._deadline_date = datetime.strptime(deadline_date_str,
                                                "%d-%m-%Y").date()

    @property
    def obj_task(self):
        return self._obj_task

    @obj_task.setter
    def obj_task(self, obj_task_str):
        self._obj_task = obj_task_str

    @property
    def obj_theme(self):
        return self._obj_theme

    @obj_theme.setter
    def obj_theme(self, obj_theme_str):
        self._obj_theme = obj_theme_str

    def __object_completed(self):
        self._obj_complete = True

    def __str__(self):

        # redundant code - found, how to align text with str.format()
        #
        # def __pad_line(line_str, length):
        #     pad = (length - len(line_str))/2
        #     return " " * floor(pad) + line_str + " " * ceil(pad)

        def __wrap_str(text, length):
            wrapped_text = ''
            for line in wrap(text, length):
                line += " " * (length - len(line)) + "|\n"
                line = "|" + line
                wrapped_text += line
            return wrapped_text

        deadline = self.deadline_date + " " + self.deadline_time
        dash_gridline = '-' * ROW_LEN
        esign_gridline = '=' * ROW_LEN
        return (
                '|{esign_gridline}|\n'
                '|{:<{field_col_len}}||{:^{val_col_len}}|\n'
                '|{dash_gridline}|\n'
                '|{:<{field_col_len}}||{:^{val_col_len}}|\n'
                '|{dash_gridline}|\n'
                '|{:<{field_col_len}}||{:^{val_col_len}}|\n'
                '|{esign_gridline}|\n'
                '|{:^{row_len}}|\n'
                '|{esign_gridline}|\n'
                '{}'
                '|{esign_gridline}|\n'
                ).format("THEME", self.obj_theme,
                         "CREATED", self.creation_datetime,
                         "DEADLINE", deadline,
                         "TASK", __wrap_str(self.obj_task, ROW_LEN),
                         field_col_len=FIELD_COL_LEN,
                         val_col_len=VAL_COL_LEN,
                         row_len=ROW_LEN,
                         esign_gridline=esign_gridline,
                         dash_gridline=dash_gridline)

    def json_dump(self):
        return json.dumps(self, cls=Objective.ObjectiveEncoder)


# just for checking

if __name__ == "__main__":
    import time
    check_time = time.time()
    obj = Objective()
    obj.obj_theme = "NEW IDEA"
    obj.obj_task = ("Lib for creating tables with ascii "
                    "(like markup table in GitHub README).")
    print(obj)
    print(obj.json_dump())
    import file_manager
    file_manager.save_objs([obj, obj, obj], r"..\list_data")
    objs = []
    for obj_read in file_manager.read_objs(r"..\list_data"):
        objs.append(obj_read)
    print(objs)
    print(objs[0])
