#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import argparse
import json
import os.path


# Добавить студента
def show_add(students, name, groop, marks):
    """
    Добавить данные о студенте
    """
    students.append(
        {"name": name, "groop": groop, "marks": [int(i) for i in marks.split()]}
    )
    return students


# Вывести справку о работе с программой.
def help():
    print("Список команд:\n")
    print("add - добавить работника;")
    print("list - вывод студентов с оценками 4 и 5;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")


# Отобразить студентов
def show_display(students):
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
def show_select(students):
    result = []
    for idx, student in enumerate(students, 1):
        res = all(int(x) > 3 for x in student["marks"])
        if res:
            result.append(student)
    return result


# Сохранение в файл
def save_students(file_name, students):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


# Загрузка из файла
def load_students(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument("filename", action="store", help="The data file name")

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version", action="version", help="The main parser", version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser("add", parents=[file_parser], help="Add a new student")
    add.add_argument(
        "-n", "--name", action="store", required=True, help="The student's name"
    )
    add.add_argument("-g", "--groop", action="store", help="The student's group")
    add.add_argument(
        "-m", "--marks", action="store", required=True, help="The student's marks"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    _ = subparsers.add_parser(
        "select", parents=[file_parser], help="Select the students"
    )
    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        students = load_students(args.filename)
    else:
        students = []

    # Добавить студента.

    if args.command == "add":
        students = show_add(students, args.name, args.groop, args.marks)
        if len(students) > 1:
            students.sort(key=lambda item: sum(item["marks"]) / len(item["marks"]))
        print(students)
        is_dirty = True
    # Отобразить всех студентов.
    elif args.command == "display":
        show_display(students)
    # Выбрать требуемых студентов.
    elif args.command == "select":
        print(students)
        selected = show_select(students)
        show_display(selected)
    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(args.filename, students)


if __name__ == "__main__":
    main()
