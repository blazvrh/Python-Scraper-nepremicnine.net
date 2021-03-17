import pickle


def clear_file(file_path: str):
    open(file_path, 'w').close()


def append_to_file(file_path: str, text: str):
    with open(file_path, "ba+") as f:
        f.write(text.encode('UTF-16'))


def get_file_content(file_path: str):
    with open(file_path, "br") as f:
        content = f.read().decode('UTF-16')

    return content


def write_to_pickle(file_path: str, data):
    with open(file_path, 'wb') as handle:
        pickle.dump(data, handle)


def read_pickle(file_path: str):
    with open(file_path, 'rb') as handle:
        data = pickle.load(handle)

    return data
