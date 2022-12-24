#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import click
import os
import sys


@click.group()
def cli():
    pass


# Добавление нового студента
@cli.command("add")
@click.option("-n", "--name")
@click.option("-g", "--groop")
@click.option("-gr", "--marks")
def add(name, groop, marks):
    """
    Добавить данные о студенте
    """
    # Запросить данные о студенте.
    students = load_students()
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


# Отобразить студентов
@cli.command("display")
@click.option("--select", "-s", is_flag=True)
def display(select):
    # Заголовок таблицы.
    students = load_students()
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


# Выбор студентов с оценкой не ниже 4
def selected(students):
    result = []
    for idx, student in enumerate(students, 1):
        res = all(int(x) > 3 for x in student["marks"])
        if res:
            result.append(student)
    return result


# Загрузка из файла
def load_students():
    filename = os.environ.get("STUDENTS_DATA1")
    with open(filename, "r", encoding="utf-8") as fin:
        return json.load(fin)


if __name__ == "__main__":
    cli()
