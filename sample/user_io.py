import sys


def user_input(msg_to_user):
    user_string = input(msg_to_user + "\n")
    return user_string.strip()


def print_error(err_msg):
    print(err_msg, file=sys.stderr)
