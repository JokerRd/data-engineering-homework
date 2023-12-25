import json
import os


def load_file_as_str(file_path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return str(f.read())


def get_all_files_in_dir(dir_path: str) -> list[str]:
    return os.listdir(dir_path)


def load_files(dir_path: str) -> list[str]:
    files = get_all_files_in_dir(dir_path)
    return list(map(lambda file_name: load_file_as_str(os.path.join(dir_path, file_name)), files))


def save_to_json_file(data, encoder, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        json.dump(data, f, cls=encoder, indent=4, ensure_ascii=False)
