# coding=utf-8
import os


def get_full_path_test_file(filename):
    path = os.getcwd()
    return os.path.join(path, "test_file", filename)


def get_full_path_input_file(filename):
    path = os.getcwd()
    return os.path.join(path, "input_file", filename)


def get_full_path_output_file(filename):
    path = os.getcwd()
    return os.path.join(path, "output_file", filename)

