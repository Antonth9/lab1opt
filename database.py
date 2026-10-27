import csv
import os

FILENAME = "database.csv"


def load_data(filename=FILENAME):
    """Загружает CSV в список словарей."""
    if not os.path.exists(filename):
        return [], []
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = [dict(row) for row in reader]
    return fieldnames, rows


def save_data(fieldnames, rows, filename=FILENAME):
    """Сохраняет список словарей в CSV."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def show_table(fieldnames, rows):
    """Красиво выводит таблицу."""
    if not rows:
        print("\n[!] Таблица пуста.")
        return

    widths = {f: len(f) for f in fieldnames}
    for row in rows:
        for f in fieldnames:
            widths[f] = max(widths[f], len(str(row.get(f, ""))))

    header = " | ".join(f"{f:<{widths[f]}}" for f in fieldnames)
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))
    for row in rows:
        print(" | ".join(f"{str(row.get(f, '')):<{widths[f]}}" for f in fieldnames))
    print("-" * len(header))
    print(f"Всего записей: {len(rows)}")


def init_database():
    """Создаёт пустую БД, если её нет."""
    if not os.path.exists(FILENAME):
        fieldnames = ["id", "name", "email", "age"]
        save_data(fieldnames, [])
        print(f"[+] Создана новая база: {FILENAME}")
        return fieldnames
    fieldnames, _ = load_data()
    return fieldnames


def add_record(fieldnames, rows):
    record = {}
    for f in fieldnames:
        val = input(f"  {f}: ").strip()
        if f == "id" and not val:
            val = str(max((int(r["id"]) for r in rows if r.get("id", "").isdigit()), default=0) + 1)
            print(f"    -> id автоматически: {val}")
        record[f] = val
    rows.append(record)
    save_data(fieldnames, rows)
    print("[+] Запись добавлена.")


def find_index(rows, fieldnames, record_id):
    for i, r in enumerate(rows):
        if r.get(fieldnames[0]) == str(record_id):
            return i
    return -1


def edit_record(fieldnames, rows):
    show_table(fieldnames, rows)
    rid = input(f"\nВведите {fieldnames[0]} для редактирования: ").strip()
    idx = find_index(rows, fieldnames, rid)
    if idx == -1:
        print("[!] Запись не найдена.")
        return

    print("Текущие значения (Enter — оставить как есть):")
    for f in fieldnames:
        cur = rows[idx].get(f, "")
        new = input(f"  {f} [{cur}]: ").strip()
        if new:
            rows[idx][f] = new
    save_data(fieldnames, rows)
    print("[+] Запись обновлена.")


def delete_record(fieldnames, rows):
    show_table(fieldnames, rows)
    rid = input(f"\nВведите {fieldnames[0]} для удаления: ").strip()
    idx = find_index(rows, fieldnames, rid)
    if idx == -1:
        print("[!] Запись не найдена.")
        return
    confirm = input(f"Удалить запись '{rid}'? (y/n): ").strip().lower()
    if confirm == "y":
        del rows[idx]
        save_data(fieldnames, rows)
        print("[+] Запись удалена.")


def search(fieldnames, rows):
    query = input("Введите строку для поиска: ").strip().lower()
    found = [r for r in rows if any(query in str(v).lower() for v in r.values())]
    if found:
        show_table(fieldnames, found)
    else:
        print("[!] Ничего не найдено.")


def main():
    fieldnames = init_database()
    _, rows = load_data()

    menu = """
===== CSV DATABASE =====
1. Показать все записи
2. Добавить запись
3. Редактировать запись
4. Удалить запись
5. Поиск
6. Перезагрузить из файла
7. Выход
========================
"""

    while True:
        print(menu)
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            show_table(fieldnames, rows)
        elif choice == "2":
            add_record(fieldnames, rows)
        elif choice == "3":
            edit_record(fieldnames, rows)
        elif choice == "4":
            delete_record(fieldnames, rows)
        elif choice == "5":
            search(fieldnames, rows)
        elif choice == "6":
            fieldnames, rows = load_data()
            print("[+] Данные перезагружены.")
        elif choice == "7":
            print("До свидания!")
            break
        else:
            print("[!] Неверный пункт меню.")


if __name__ == "__main__":
    main()