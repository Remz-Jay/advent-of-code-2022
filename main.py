import os

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("."),
    autoescape=select_autoescape()
)


@click.command()
@click.option('--day', prompt='Which day do I generate?')
@click.option('--delete', default=False)
def cli(delete, day):
    files = [
        (f"src/input/day{day}.txt", False),
        (f"test/input/day{day}.txt", False),
        (f"src/day{day}.py", "templates/day_class.pyi"),
        (f"test/test_day{day}.py", "templates/day_test.pyi")
    ]

    if delete:
        delete_files_for_day(day, files)
    else:
        generate_day_from_template(day, files)


def delete_files_for_day(day, files):
    for f in files:
        if os.path.exists(f[0]):
            os.remove(f[0])


def generate_day_from_template(day, files):
    for file in files:
        if not file[1]:
            f = open(file[0], "w")
            f.close()
        else:
            t = env.get_template(file[1])
            render = t.render(id=f"day{day}")
            with open(file[0], "w") as f:
                f.write(render)
            f.close()


if __name__ == '__main__':
    cli()
