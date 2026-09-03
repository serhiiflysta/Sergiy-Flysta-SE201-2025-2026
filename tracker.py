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

def get_valid_date(prompt):
    while True:
        default_date = datetime.now().strftime("%Y-%m-%d")
        date_input = input(f"{prompt} [за замовчуванням {default_date}]: ").strip()
        
        if not date_input:
            return default_date
            
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Помилка: введіть дату у форматі РРРР-ММ-ДД (наприклад, 2026-06-06).")

def add_workout(workouts):
    print("\n--- Додавання вправи до тренування ---")
    date_str = get_valid_date("Дата (РРРР-ММ-ДД)")

    name = input("Назва вправи (наприклад, Біг / Прес): ").strip() or "Загальне тренування"
    duration = get_valid_float("Тривалість (хв): ")

    if name.lower() == "біг":
        sets = 0
        reps = 0
        calories = get_valid_float("Спалені калорії (ккал): ")
    else:
        sets = get_valid_int("Кількість підходів: ")
        reps = get_valid_int("Кількість повторень: ")
        calories = 0.0

    exercise_data = {
        "name": name,
        "duration": duration,
        "sets": sets,
        "reps": reps,
        "calories": calories
    }

    # Перевіряємо, чи вже є тренування на цю дату
    existing_day = None
    for day in workouts:
        if day["date"] == date_str:
            existing_day = day
            break

    if existing_day:
        existing_day["exercises"].append(exercise_data)
    else:
        workouts.append({
            "date": date_str,
            "exercises": [exercise_data]
        })

    save_data(workouts)
    print("Вправу успішно додано до тренування та збережено!")

def view_workouts(workouts):
    if not workouts:
        print("\nІсторія тренувань порожня.")
        return

    print("\n--- Список тренувань ---")
    for i, day in enumerate(workouts, 1):
        print(f"\n{i}. Дата: {day['date']}")
        for ex in day['exercises']:
            line = f"   - Вправа: {ex['name']} | Тривалість: {ex['duration']} хв"
            if ex['name'].lower() == "біг":
                line += f" | Калорії: {ex['calories']} ккал"
            else:
                line += f" | Підходи: {ex['sets']} | Повторення: {ex['reps']}"
            print(line)

def calculate_weekly_stats(workouts):
    if not workouts:
        print("\nНемає даних для аналізу.")
        return

    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    total_duration = 0
    total_calories = 0
    workout_days = 0

    for day in workouts:
        try:
            w_date = datetime.strptime(day['date'], "%Y-%m-%d").date()
            if week_ago <= w_date <= today:
                workout_days += 1
                for ex in day['exercises']:
                    total_duration += ex['duration']
                    total_calories += ex['calories']
        except ValueError:
            continue

    print(f"\n--- Статистика за тиждень ---")
    print(f"Днів з тренуваннями: {workout_days}")
    print(f"Сумарний час: {total_duration} хв")
    print(f"Сумарно спалено калорій: {total_calories} ккал")

def main():
    workouts = load_data()
    while True:
        print("\n=== ТРЕКЕР ТРЕНУВАНЬ ===")
        print("1. Додати тренування")
        print("2. Переглянути список тренувань")
        print("3. Статистика за тиждень")
        print("4. Вихід")
        
        choice = input("Виберіть пункт (1-4): ").strip()
        if choice == "1":
            add_workout(workouts)
        elif choice == "2":
            view_workouts(workouts)
        elif choice == "3":
            calculate_weekly_stats(workouts)
        elif choice == "4":
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")

if __name__ == "__main__":
    main()