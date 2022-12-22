#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import click


@click.group()
def cli():
    pass


@cli.command("add")
@click.argument("filename")
@click.option("-n", "--name")
@click.option("-g", "--groop")
@click.option("-gr", "--marks")
def add(filename, name, groop, marks):
    """
    Добавить данные о студенте
    """
    # Запросить данные о студенте.
    students = load_students(filename)
    students.append(
        {
            "name": name,
            "group": groop,
            "grade": [int(i) for i in marks.split()],
        }
    )
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)
    click.secho("Студент добавлен")


@cli.command("display")
@click.argument("filename")
@click.option("--select", "-s", is_flag=True)
def display(filename, select):
    # Заголовок таблицы.
    students = load_students(filename)
    if select:
        students = selected(students)

    # Заголовок таблицы.
    line = "+-{}-+-{}-+-{}-+".format("-" * 30, "-" * 20, "-" * 9)
    print(line)
    print("| {:^30} | {:^20} | {:^9} |".format("Ф.И.О.", "Группа", "Оценки"))
    print(line)

    # Вывести данные о всех студентах.
    for idx, student in enumerate(students, 1):
        print(
            "| {:<30} | {:<20} | {:>7} |".format(
                student.get("name", ""),
                student.get("groop", ""),
                ",".join(map(str, student["marks"])),
            )
        )
    print(line)


def selected(students):
    result = []
    for idx, student in enumerate(students, 1):
        res = all(int(x) > 3 for x in student["marks"])
        if res:
            result.append(student)
    return result


def load_students(filename):
    with open(filename, "r", encoding="utf-8") as fin:
        return json.load(fin)


if __name__ == "__main__":
    cli()
