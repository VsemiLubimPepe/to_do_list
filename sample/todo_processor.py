from user_io import user_input, print_error
from file_manager import read_objs
from commands import CommandHandler, UnknownCommand, \
    InvalidArgumentsNum


def load_objs(obj_list_ref):
    for obj in read_objs(None):
        obj_list_ref.append(obj)


if __name__ == "__main__":
    print("Greetings. Starting TODO app.")
    objective_list = []
    print("Loading data.")
    load_objs(objective_list)
    print("Data loaded.")
    command_handler = CommandHandler(objective_list)
    while True:
        try:
            command_line = user_input("Type command:")
            command = command_line.split()[0]
            command_args = command_line.split()[1:]
            result = command_handler.execute_command(command, command_args)
            print(result)
        except FileNotFoundError as e:
            print_error(e)
        except UnknownCommand as e:
            print_error(e)
        except InvalidArgumentsNum as e:
            print_error(e)
        except NotImplementedError as e:
            print_error(e)
        except EOFError:
            exit()
        except KeyboardInterrupt:
            exit()
