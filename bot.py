import json
import os
from datetime import datetime, timedelta

# Назва файлу для зберігання даних
DATA_FILE = "events.json"

def load_events():
    """Завантажує події з файлу JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_events(events):
    """Зберігає список подій у файл JSON."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=4, ensure_ascii=False)

def check_conflict(events, new_date, new_start_time, duration_min=60):
    """Перевіряє, чи не перетинається нова подія з існуючими (стандартно 60 хв)."""
    new_start = datetime.strptime(f"{new_date} {new_start_time}", "%Y-%m-%d %H:%M")
    new_end = new_start + timedelta(minutes=int(duration_min))
    
    for event in events:
        if event['date'] == new_date:
            exist_start = datetime.strptime(f"{event['date']} {event['time']}", "%Y-%m-%d %H:%M")
            # Припустимо, що кожна подія триває 1 годину, якщо не вказано інше
            exist_end = exist_start + timedelta(minutes=60) 
            
            if (new_start < exist_end) and (new_end > exist_start):
                return True, event['name']
    return False, None

def add_event(events):
    """Функція для додавання нової події."""
    print("\n--- Додавання нової події ---")
    name = input("Введіть назву події: ")
    date_str = input("Введіть дату (РРРР-ММ-ДД): ")
    time_str = input("Введіть час початку (ГГ:ХХ): ")
    category = input("Категорія (лекція, зустріч, іспит тощо): ")
    
    try:
        # Перевірка формату дати
        datetime.strptime(date_str, "%Y-%m-%d")
        datetime.strptime(time_str, "%H:%M")
        
        conflict, conflict_name = check_conflict(events, date_str, time_str)
        if conflict:
            print(f"⚠️ УВАГА: Конфлікт! У цей час вже заплановано: {conflict_name}")
            confirm = input("Все одно додати? (так/ні): ")
            if confirm.lower() != 'так':
                return

        new_event = {
            "name": name,
            "date": date_str,
            "time": time_str,
            "category": category
        }
        events.append(new_event)
        save_events(events)
        print("✅ Подію успішно додано!")
    except ValueError:
        print("❌ Помилка: Неправильний формат дати або часу.")

def show_events(events_list, title="Список усіх подій"):
    """Виводить список подій у зручному форматі."""
    if not events_list:
        print("\nСписок порожній.")
        return
    
    print(f"\n--- {title} ---")
    # Сортування за датою та часом перед виводом
    sorted_events = sorted(events_list, key=lambda x: (x['date'], x['time']))
    for i, ev in enumerate(sorted_events, 1):
        print(f"{i}. [{ev['date']} {ev['time']}] {ev['name']} ({ev['category']})")

def show_weekly_events(events):
    """Показує події на найближчі 7 днів."""
    today = datetime.now().date()
    week_later = today + timedelta(days=7)
    
    weekly = [e for e in events if today <= datetime.strptime(e['date'], "%Y-%m-%d").date() <= week_later]
    show_events(weekly, "Події на тиждень")

def main():
    events = load_events()
    print("👋 Вітаємо у боті 'Організатор подій'!")
    
    while True:
        print("\nДоступні команди: додати, показати, тиждень, фільтр, видалити, редагувати, сьогодні, вийти, допомога")
        choice = input("Введіть команду: ").lower().strip()
        
        if choice == "додати":
            add_event(events)
        elif choice == "показати":
            show_events(events)
        elif choice == "тиждень":
            show_weekly_events(events)
        elif choice == "допомога":
            print("\nДопомога: Використовуйте 'додати' для створення події, 'показати' для списку, 'тиждень' для розкладу на 7 днів.")
        elif choice == "сьогодні":
            today_str = datetime.now().strftime("%Y-%m-%d")
            today_events = [e for e in events if e['date'] == today_str]
            show_events(today_events, "Події на сьогодні")
        elif choice == "видалити":
            show_events(events)
            try:
                idx = int(input("Введіть номер події для видалення: ")) - 1
                removed = events.pop(idx)
                save_events(events)
                print(f"🗑️ Видалено: {removed['name']}")
            except:
                print("❌ Помилка видалення.")
        elif choice == "вийти":
            print("Дякуємо за використання! До зустрічі.")
            break
        else:
            print("🤔 Невідома команда. Спробуйте ще раз або введіть 'допомога'.")

if __name__ == "__main__":
    main()
