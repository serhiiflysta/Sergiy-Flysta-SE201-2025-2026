import json
import os
from datetime import datetime, timedelta

DATA_FILE = "workouts_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

def save_data(workouts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(workouts, file, ensure_ascii=False, indent=4)

def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Значення не може бути від'ємним.")
                continue
            return value
        except ValueError:
            print("Помилка: введіть число.")

def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Значення не може бути від'ємним.")
                continue
            return value
        except ValueError:
            print("Помилка: введіть ціле число.")

def add_workout(workouts):
    print("\n--- Додавання нового тренування ---")
    default_date = datetime.now().strftime("%Y-%m-%d")
    date_input = input(f"Дата (РРРР-ММ-ДД) [за замовчуванням {default_date}]: ").strip()
    date_str = date_input if date_input else default_date
    
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        date_str = default_date

    name = input("Назва вправи: ").strip() or "Загальне тренування"
    duration = get_valid_float("Тривалість (хв): ")
    sets = get_valid_int("Кількість підходів: ")
    reps = get_valid_int("Кількість повторень: ")
    calories = get_valid_float("Спалені калорії (ккал): ")

    workouts.append({
        "date": date_str,
        "name": name,
        "duration": duration,
        "sets": sets,
        "reps": reps,
        "calories": calories
    })
    save_data(workouts)
    print("Успішно збережено!")

def view_workouts(workouts):
    if not workouts:
        print("\nІсторія тренувань порожня.")
        return

    print("\n--- Список тренувань ---")
    for i, w in enumerate(workouts, 1):
        print(f"{i}. Дата: {w['date']} | Вправа: {w['name']} | "
              f"Тривалість: {w['duration']} хв | Підходи: {w['sets']} | "
              f"Повторення: {w['reps']} | Калорії: {w['calories']} ккал")

def main():
    workouts = load_data()
    while True:
        print("\n=== ТРЕКЕР ТРЕНУВАНЬ ===")
        print("1. Додати тренування")
        print("2. Переглянути список тренувань")
        print("3. Вихід")
        
        choice = input("Виберіть пункт (1-3): ").strip()
        if choice == "1":
            add_workout(workouts)
        elif choice == "2":
            view_workouts(workouts)
        elif choice == "3":
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    main()