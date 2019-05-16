import pathlib
import json
import pickle


def join_to_full_path(dir_path, filename, suffix):
    path = pathlib.Path(dir_path).joinpath(filename + suffix)
    return path


def store_dict_to_json(dict_data, filename, default_dir_path="./data"):
    json_data = json.dumps(dict_data)
    full_path = join_to_full_path(default_dir_path, filename, ".json")
    with open(full_path, "w", encoding="utf8") as f:
        f.write(json_data)
    print("Store to json file successful...")


def store_dict_to_serialization(dict_data, filename, default_dir_path="./data"):
    pickle_data = pickle.dumps(dict_data, protocol=pickle.HIGHEST_PROTOCOL)
    full_path = join_to_full_path(default_dir_path, filename, ".txt")
    with open(full_path, "wb") as f:
        f.write(pickle_data)
    print("Store to pickle file successful...")


def read_dict_from_json(filename, default_dir_path="./data"):
    full_path = join_to_full_path(default_dir_path, filename, ".json")
    with open(full_path, "r", encoding="utf8") as f:
        dict_data = f.read()
    print("Read data from json successful...")
    return json.loads(dict_data)


def read_dict_from_serialization(filename, default_dir_path="./data"):
    full_path = join_to_full_path(default_dir_path, filename, ".txt")
    with open(full_path, "rb") as f:
        dict_data = f.read()
    print("Read data from json successful...")
    return pickle.loads(dict_data)


if __name__ == '__main__':
    a = {"a": "好"}
    store_dict_to_json(a, "aa")
    print(read_dict_from_json("aa"))
    store_dict_to_serialization(a, "aa")
    print(read_dict_from_serialization("aa"))
