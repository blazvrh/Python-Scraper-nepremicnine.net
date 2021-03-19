""" File handling functions """
import pickle


def clear_file(file_path: str) -> None:
    """
    Clears content of a passed file
    :param file_path: str
    :return: none
    """
    open(file_path, 'w').close()


def append_to_file(file_path: str, text: str) -> None:
    """
    Appends text to file (UTF-16 format)
    :param file_path: str
    :param text: str
    :return: None
    """
    with open(file_path, "ba+") as f:
        f.write(text.encode('UTF-16'))


def get_file_content(file_path: str) -> str:
    """
    Returns content of text file (UTF-16 format)
    :param file_path: str
    :return: str
    """
    with open(file_path, "br") as f:
        content = f.read().decode('UTF-16')

    return content


def write_to_pickle(file_path: str, data: any) -> None:
    """
    Write object to pickle file
    :param file_path: str
    :param data: any
    :return: None
    """
    with open(file_path, 'wb') as handle:
        pickle.dump(data, handle)


def read_pickle(file_path: str) -> any:
    """
    Returns content of a pickle file
    :param file_path: str
    :return: any
    """
    with open(file_path, 'rb') as handle:
        data = pickle.load(handle)

    return data
