from objective import Objective
import file_manager
from user_io import user_input


class UnknownCommand(Exception):
    pass


class InvalidArgumentsNum(Exception):
    pass


class CommandHandler:
    def __init__(self, obj_list_ref):
        self._command_list = {"help": self.HelpCommand(),
                              "add_obj": self.AddObjCommand(
                                  obj_list_ref),
                              "save_data": self.SaveDataCommand(obj_list_ref),
                              "del_obj": self.DeleteObjCommand(obj_list_ref),
                              "list_obj": self.ListObjCommand(obj_list_ref),
                              "history": self.HistoryCommand()}

    def execute_command(self, command, args):
        if command not in self._command_list:
            raise UnknownCommand(("Unknown command '{}'. "
                                  "Type 'help' to see available commands."
                                  ).format(command))
        command_return = self._command_list[command].execute(*args)
        return command_return

    class Command:
        def execute(self):
            raise NotImplementedError(("{} hasn't been implemented"
                                       " yet.").format(str(self)))

        def __str__(self):
            return "Command"

    class HelpCommand(Command):

        HELP_INFO_BRIEF = {
            "help": "help [command_name]\n",
            "add_obj": "add_obj [objective_data]\n",
            "save_data": "save_data [path]\n",
            "load_data": "load_data path\n",
            "del_obj": "del_obj option\n",
            "list_obj": "list_obj\n",
            "history": "history"
        }

        HELP_INFO_FULL = {
            "help": ("help [command_name]\n"
                     "Display information about built-in commands.\n"
                     "\n"
                     "If COMMAND_NAME specified, "
                     "gives detailed information about command.\n"),
            "add_obj": ("add_obj [objective_data]\n"
                        "add_obj "
                        "[deadline_date deadline_time "
                        "obj_theme obj_task]\n"
                        "Creates new objective in the TODO list.\n"
                        "\n"
                        "If OBJECTIVE_DATA specified, "
                        "instantly creates new objective.\n"
                        "Otherwise, you could type info one by one.\n"),
            "save_data": ("save_data [path]\n"
                          "Saves objectives to file.\n"
                          "\n"
                          "If PATH specified, save data into it "
                          "(rewrites file!).\n"
                          "\n"
                          "PATH could be file or directory path.\n"
                          "If PATH is a directory, "
                          "there will be created new file "
                          "named 'todo_list.txt'.\n"
                          "\n"
                          "If PATH didn't specified, "
                          "creates directory and file in the app directory."),
            "load_data": ("load_data path\n"
                          "Loads objectives from file PATH.\n"),
            "del_obj": ("del_obj option\n"
                        "Deletes certain loaded objective/es "
                        "(without ability to restore it!).\n"
                        "\n"
                        "Options:\n"
                        "\n"
                        "-a\n"
                        "\t fully clear objective list.\n"
                        "\n"
                        "-i = INDEX\n"
                        "\n"
                        "\t delete objective by its index "
                        "in objective list.\n"
                        "\n"
                        "-t = THEME"
                        "\t delete objectives by their theme.\n"),
            "list_obj": ("list_obj\n"
                         "Prints list of all loaded objectives.\n"),
            "history": ("history\n"
                        "Prints list of 20 previously used commands "
                        "with arguments.\n")
        }

        def execute(self, *args):
            if len(args) == 0:
                cmds_info = "".join(self.HELP_INFO_BRIEF.values()) + "\n"
                return (
                        "ToDo App, version 1.0 - release.\n"
                        "These commands are available. "
                        "Type 'help' to see this list.\n"
                        "Type 'help name' to find what command 'name' do.\n\n"
                        + cmds_info
                )
            elif len(args) == 1:
                try:
                    cmd_info = self.HELP_INFO_FULL[args[0]]
                except KeyError:
                    raise UnknownCommand(("Unknown command {} was passed. "
                                          "Type 'help' to list all available "
                                          "commands.").format(args[0]))
                return cmd_info
            else:
                raise InvalidArgumentsNum(("{} needed no more than "
                                           "one argument.").format(self))

        def __str__(self):
            return "Command 'help'"

    class AddObjCommand(Command):
        def __init__(self, obj_list_ref):
            self._obj_list_ref = obj_list_ref

        def execute(self, *args):
            def __create_new_obj():
                print("Creating new objective.")
                obj_theme = user_input("Type theme of the objective:")
                obj_deadline_date = user_input(("Type deadline date "
                                                "(dd-mm-yyyy) of "
                                                "the objective"
                                                "(if not specified, "
                                                "deadline date will be "
                                                "set tomorrow):"))
                obj_deadline_time = user_input(("Type deadline time "
                                                "(hh:mm) of "
                                                "the objective"
                                                "(if not specified, deadline "
                                                "time will be 00:00):"))
                obj_task = user_input("Type task of the objective:")
                return Objective(deadline_date=obj_deadline_date,
                                 deadline_time=obj_deadline_time,
                                 obj_theme=obj_theme,
                                 obj_task=obj_task)

            if len(args) == 0:
                new_obj = __create_new_obj()
                self._obj_list_ref.append(new_obj)
            elif len(args) == 4:
                new_obj = Objective(None, *args)
                self._obj_list_ref.append(new_obj)
            else:
                raise InvalidArgumentsNum(("{} needed four arguments for "
                                           "instant creation "
                                           "of objective.").format(self))
            return "Created new objective successfully."

        def __str__(self):
            return "Command 'add_obj'"

    class SaveDataCommand(Command):
        def __init__(self, obj_list_ref):
            self._obj_list_ref = obj_list_ref

        def execute(self, *args):
            if len(args) > 1:
                raise InvalidArgumentsNum(("{} needed no more "
                                           "than one argument").format(self))
            if args:
                path = args[0]
            else:
                path = None
            file_manager.save_objs(self._obj_list_ref, path)
            return "Saved successfully."

        def __str__(self):
            return "Command 'save_data'"

    class DeleteObjCommand(Command):
        def __init__(self, obj_list_ref):
            self._obj_list_ref = obj_list_ref

        def execute(self, *args):
            pass

        def __str__(self):
            return "Command 'del_obj'"

    class ListObjCommand(Command):
        def __init__(self, obj_list_ref):
            self._obj_list_ref = obj_list_ref

        def execute(self, *args):
            if len(args) > 0:
                raise InvalidArgumentsNum(("{} didn't need any "
                                           "arguments").format(self))
            return "".join((str(obj) for obj in self._obj_list_ref))

        def __str__(self):
            return "Command 'list_obj'"

    class HistoryCommand(Command):
        # def __init__(self, comm_list_ref):
        #     self._comm_list_ref = comm_list_ref

        # def execute(self, *args):
        #     return "\n".join(self._comm_list_ref)

        def __str__(self):
            return "Command 'history'"
    #   TODO:
    #    -refactor load command (in current state there is no sense)
    #    -implement history command (use history queue size 20? mb)
    #    -add implement execute() for delete command
    #    -add exit command (or just left ctrl+C exit?)

    # class LoadDataCommand(Command):
    #     def __init__(self, obj_list_ref):
    #         self._obj_list_ref = obj_list_ref
    #
    #     def execute(self, *args):
    #

# if __name__ == "__main__":
