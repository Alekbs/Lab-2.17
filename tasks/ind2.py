#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import click
import os


@click.group()
@click.argument("filename")
@click.pass_context
def cli(ctx, filename):
    ctx.obj = filename


@cli.command("add")
@click.pass_obj
@click.option("-n", "--name")
@click.option("-g", "--groop")
@click.option("-m", "--marks")
def add(filename, name, groop, marks):
    """
    Добавить данные о студенте
    """
    students = load_students(filename)
    students.append(
        {
            "name": name,
            "groop": groop,
            "marks": [int(i) for i in marks.split()],
        }
    )
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)
    click.secho("Студент добавлен")


@cli.command("display")
@click.pass_obj
@click.option("--select", "-s", is_flag=True)
def display(filename, select):
    """
    Вывести данные о студентах.
    """
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
    for student in students:
        print(
            "| {:<30} | {:<20} | {:>7} |".format(
                student.get("name", ""),
                student.get("groop", ""),
                ",".join(map(str, student["marks"])),
            )
        )
    print(line)


def selected(students):
    """
    Выбрать студентов со средним баллом не ниже 4.
    """

    result = []
    for student in students:
        res = all(int(x) > 3 for x in student["marks"])
        if res:
            result.append(student)
    return result


def load_students(filename):
    """
    Загрузить всех студентов из файла JSON.
    """
    result = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as fin:
            result = json.load(fin)
    return result


if __name__ == "__main__":
    cli()
