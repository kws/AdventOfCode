import os
from distutils.dir_util import copy_tree
import requests
from decouple import config
from markdownify import markdownify

AOC_COOKIE = config("AOC_COOKIE")


class FileParser:
    def __init__(self, dir_path: str, file_name: str) -> None:
        self.dir_path = dir_path
        self.file_name = file_name

    def load(self) -> list:
        with open(self.file_path) as f:
            data = [d.strip("\n") for d in f.readlines()]
        return data

    def read(self) -> list[str]:
        self.file_path = os.path.join(self.dir_path, self.file_name)
        return self.load()


def find_html_block(text: str, tag: str):
    start = text.find(f"<{tag}>")
    end = text.find(f"</{tag}>")
    return text[start + len(f"<{tag}>") : end]


def get_inputs(day: int):
    res = requests.get(
        f"https://adventofcode.com/2022/day/{day}", cookies={"session": AOC_COOKIE}
    )
    test_input = find_html_block(res.text, "code")
    statement = find_html_block(res.text, "main")
    input_res = requests.get(
        f"https://adventofcode.com/2022/day/{day}/input",
        cookies={"session": AOC_COOKIE},
    )
    final_input = input_res.text
    return statement, test_input, final_input


def new_day(day: int):
    day_dir = str(day).zfill(2)
    copy_tree("day_template", f"{day_dir}")
    statement, test_input, final_input = get_inputs(day)

    with open(f"{day_dir}/test.txt", "w") as f:
        f.write(test_input)

    with open(f"{day_dir}/final.txt", "w") as f:
        f.write(final_input)

    with open(f"{day_dir}/STATEMENT.md", "w") as f:
        f.write(markdownify(statement))

def submit_answer(day: int, answer: int | str, part: int = 1) -> bool:
    res = requests.post(
        f"https://adventofcode.com/2022/day/{day}/answer",
        cookies={"session": AOC_COOKIE},
        data={"level": part, "answer": answer},
    )
    print(find_html_block(res.text, "main"))
    if "That's not the right answer" in res.text:
        print("Wrong answer.. Try again")

    elif "You gave an answer too recently" in res.text:
        start = res.text.find("You gave an answer too recently;")
        end = res.text.find("left to wait")
        print("To many attempts...", res.text[start:end], "left to wait")
    else:
        print("Great success! Your answer is correct")
