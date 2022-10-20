import subprocess
import sys


def run_parsers():
    i = {
        "buttersafe": "buttersafe.py" # <--comic_name, base_folder
    }

    comix_parsers = [
        "buttersafe.py",
        "exocomics.py",
        "left_handed_toons.py",
    ]
    for comix_parser in comix_parsers:
        subprocess.run([sys.executable, comix_parser])


def check_new_comix() -> list[str]:
    pass
    # TODO: check new comix and return list of new chapters(images)
    return ["comix name1 - chapters 100, 99"]


def notify_user(new_comix: list[str]):
    pass
    # TODO: add file new_comix.txt with details of new comix in user desktop


if __name__ == '__main__':
    print("start program")
    run_parsers()
    new_comix = check_new_comix()
    if new_comix:
        notify_user(new_comix)
    print("end program")