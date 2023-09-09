# Путь к файлу с заметками
import json
import os
from datetime import datetime

NOTES_FILE = "notes.json"


def get_next_id(notes):
    if not notes:
        return 1
    else:
        ids = [int(note["id"]) for note in notes]
        return max(ids) + 1


def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as file:
            try:
                notes = json.load(file)
            except json.JSONDecodeError:
                notes = []
    else:
        notes = []
    return notes


def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)


def create_note():
    notes = load_notes()
    note_title = input("Введите заголовок заметки:")
    note_body = input("Введите текст заметки:")
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note_id = get_next_id(notes)

    new_note = {
        "id": note_id,
        "title": note_title,
        "body": note_body,
        "created_time": created_time,
        "last_modified_time": created_time
    }
    notes.append(new_note)
    save_notes(notes)
    print("Заметка успешно создана")


def list_notes():
    notes = load_notes()
    if not notes:
        print("Список заметок пуст.")
    else:
        print("Список заметок:")
        for note in notes:
            print(f"Идентификатор: {note['id']}, \nЗаголовок: {note['title']}, \nДата создания: {note['created_time']}")


def delete_note():
    note_id = input("Введите идентификатор заметки для удаления:")
    notes = load_notes()
    for note in notes:
        if note["id"] == int(note_id):
            notes.remove(note)
            save_notes(notes)
            print("Заметка успешно удалена.")
            break
    else:
        print(f"Заметка с идентификатором '{note_id}' не найдена")


def edit_note():
    note_id = input("Введите идентификатор заметки для просмотра:")
    notes = load_notes()
    for note in notes:
        if note["id"] == int(note_id):
            new_title = input("Введите новый заголовок (оставьте пустым для сохранения текущего): ")
            new_body = input("Введите новый текст заметки (оставьте пустым для сохранения текущего): ")
            if new_title:
                note['title'] = new_title
            if new_body:
                note['body'] = new_body
            note['last_modified_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_notes(notes)
            print("Заметка успешно отредактирована")
            break
    else:
        print(f"Заметка с идентификатором '{note_id}' не найдена")


def read_note():
    note_id = input("Введите идентификатор заметки для просмотра:")
    notes = load_notes()
    for note in notes:
        if note["id"] == int(note_id):
            print(f"Идентификатор: {note['id']}")
            print(f"Заголовок: {note['title']}")
            print(f"Текст заметки: {note['body']}")
            print(f"Дата создания: {note['created_time']}")
            print(f"Последнее изменение: {note['last_modified_time']}")
            break
    else:
        print(f"Заметка с идентификатором '{note_id}' не найдена")


def filter_notes_by_date():
    notes = load_notes()
    date_str = input("Введите дату для выборки (в формате ГГГГ-ММ-ДД): ")
    try:
        date_to_filter = datetime.strptime(date_str, "%Y-%m-%d")
        filtered_notes = [note for note in notes if
                          datetime.strptime(note['created_time'], "%Y-%m-%d %H:%M:%S").date() == date_to_filter.date()]
        if filtered_notes:
            print("Результаты выборки:")
            for note in filtered_notes:
                print(f"Идентификатор: {note['id']}")
                print(f"Заголовок: {note['title']}")
                print(f"Дата создания: {note['created_time']}")
        else:
            print("Заметки не найдены для указанной даты.")
    except ValueError:
        print("Неверный формат даты. Используйте формат 'ГГГГ-ММ-ДД'.")
        return []


while True:
    print("Выберите действие:")
    print("1. Создать новую заметку")
    print("2. Показать список заметок")
    print("3. Удалить заметку")
    print("4. Прочитать заметку")
    print("5. Редактировать заметку")
    print("6. Выборка по дате")
    print("7. Выйти")

    choice = input("Введите номер действия:")

    if choice == "1":
        create_note()
    elif choice == "2":
        list_notes()
    elif choice == "3":
        delete_note()
    elif choice == "4":
        read_note()
    elif choice == "5":
        edit_note()
    elif choice == "6":
        filter_notes_by_date()
    elif choice == "7":
        print("Выход из программы")
        break
    else:
        print("Неверный выбор. Пожалуйста, введите номер действия от 1 до 6")
