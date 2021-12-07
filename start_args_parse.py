import os
import json
import typing as tp
from argparse import ArgumentParser
from db_settings import label_desc
from textwrap import dedent


class GuineaPigs():

    def __init__(self, fname: str = "subjects.json"):
        self.fname = fname
        self._data, self._last_id = self._get_subjects()

    def _get_subjects(
        self
    ) -> tp.Tuple[tp.Dict[str, str], int]:
        """
        return: dict {id:subject} and last id as integer
        """
        if self.fname not in os.listdir():
            return dict(), -1
        else:
            with open(self.fname, 'r') as subj_datafile:
                data = json.load(subj_datafile)

        last_id = list(data.keys())[-1]
        return data, int(last_id)

    def _rewrite_file(self):
        with open(self.fname, 'w') as subj_datafile:
            json.dump(self._data, subj_datafile)

    def _add_subject(self, name):
        new_id = self._last_id + 1
        self._data[str(new_id)] = name
        self._rewrite_file()
        return new_id

    def checking_the_existence(self, h_id: tp.Union[str, int]):
        check = False
        human_id = str(h_id)
        while not check:
            name = self._data.get(human_id, None)
            if name is None:
                msg = (f"""
                    Sorry, your id {human_id} not in list of test subjects.
                    Here are all available IDs:
                    {self._data}
                    Choose another id or enter you name:
                """)
                print(dedent(msg))
                id_or_name = input()

                if id_or_name.isdigit():
                    human_id = id_or_name
                    continue
                else:
                    name = id_or_name
                    human_id = self._add_subject(name)
                    check = True
            else:
                check = True
        return name, human_id

    @property
    def data(self):
        return self._data


def check_label(label):
    desc = label_desc.get(label, None)
    while desc is None:
        msg = f"""
            Please, choose correct label.
            Here are all available:
            {label_desc}
        """
        print(dedent(msg))
        label = input()
        desc = label_desc.get(label, None)
    return desc, label


def args_parser():
    argparser = ArgumentParser()
    argparser.add_argument("--id", help="Human id")
    argparser.add_argument(
        "--label", help="Label for data sample. Coded action name.")
    args = argparser.parse_args()
    human_id = args.id
    label = args.label

    humans = GuineaPigs()
    name, human_id = humans.checking_the_existence(human_id)
    print(f"Hi, {name}. You id is {human_id}.")

    desc, label = check_label(label)
    msg = f"""
        Fine, {name}! Let's start motor imagery task.
        Your task is to imagine \x1b[6;30;42m{desc.upper()}\x1b[0m.
        You can start after signal.
    """

    print(dedent(msg))
    return human_id, label
