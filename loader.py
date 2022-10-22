#!python3
import argparse
import os
import subprocess
import sys


def run_parsers():
    """Run main loop of program"""
    comics_path = choice_folder()
    os.makedirs(comics_path, exist_ok=True)

    comix_parsers = {
        "buttersafe": "buttersafe.py",  # <--comic_name, base_folder
        "exocomics": "exocomics.py",
        "left_handed": "left_handed.py",
        "lunarbaboon": "lunarbaboon.py",
        "savage_chickens": "chickens.py",
        "wonderella": "wonderella.py",
        # "moonbeard": "moonbeard.py",  # <-- not worked
    }

    for name, comix_parser in comix_parsers.items():
        path = f"{comics_path}\\{name}"
        subprocess.run([sys.executable, comix_parser, '--outdir', path])


def choice_folder() -> str:
    """Change the default download folder"""

    parser = argparse.ArgumentParser(prog='loader', description='loader comics')
    parser.add_argument('--outdir', type=str, default=None, help='Output absolut path')
    args = parser.parse_args()

    default_path = r'E:\GitHub\Autoloader-comics-schedule\comics_folder'
    outdir = args.outdir
    if outdir is None:
        return default_path
    elif os.path.isabs(outdir):
        return outdir
    else:
        raise ValueError('Path is not absolute')


def check_new_comix() -> list[str]:
    pass
    # TODO: check new comix and return list of new chapters(images)
    return ["comix name1 - chapters 100, 99"]


def notify_user(new_comix: list[str]):
    pass
    # TODO: add file new_comix.txt with details of new comix in user desktop


def main():
    print("start program")
    try:
        run_parsers()
        # new_comix = check_new_comix()
        # if new_comix:
        #     notify_user(new_comix)
        print("end program")
    except KeyboardInterrupt:
        print('Forced program termination!')
        return


if __name__ == '__main__':
    main()
