import json
import os
import re
from datetime import datetime

# 1. ÖZEL DEKORATÖR (Custom Decorator - 3 Puan): Fonksiyonların ne zaman çalıştığını loglar
def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[SYSTEM LOG] '{func.__name__}' is running...")
        return func(*args, **kwargs)
    return wrapper

# Özel Hata Sınıfımız
class InvalidHabitError(Exception):
    pass

class Habit:
    def __init__(self, name, description, creation_date=None, is_completed=False):
        self.name = name
        self.description = description
        self.creation_date = creation_date if creation_date else datetime.now().strftime("%Y-%m-%d")
        self.is_completed = is_completed

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "creation_date": self.creation_date,
            "is_completed": self.is_completed
        }

    def __str__(self):
        status = "Done" if self.is_completed else "Pending"
        return f"[{status}] {self.name} - {self.description} (Added: {self.creation_date})"


class HabitTracker:
    def __init__(self):
        self.habits = []
        self.filename = "data.json"
        self.load_data()

    # Dekoratörümüzü burada kullanıyoruz! Her alışkanlık eklendiğinde arka planda log tutacak
    @log_action
    def add_habit(self, name, description):
        if not re.match(r"^[a-zA-Z0-9\s]{3,}$", name):
            raise InvalidHabitError("Habit name must be at least 3 characters long and contain only letters/numbers.")

        new_habit = Habit(name, description)
        self.habits.append(new_habit)
        self.save_data()
        print(f"-> Success: '{name}' added successfully!")

    def display_habits(self):
        if not self.habits:
            print("-> No habits found. Let's add some!")
        else:
            print("\n--- YOUR HABITS (Sorted A-Z) ---")
            # 2. LAMBDA FONKSİYONU (3 Puan): Listeyi alışkanlık ismine göre alfabetik sıralar
            sorted_habits = sorted(self.habits, key=lambda h: h.name.lower())
            for habit in sorted_habits:
                print(habit)

    # 3. GENERATOR (2 Puan): Alışkanlıkları belleği yormadan tek tek üreten gelişmiş bir döngü yapısı
    def get_pending_habits_generator(self):
        for habit in self.habits:
            if not habit.is_completed:
                # "yield" kelimesi bu fonksiyonu bir generator yapar
                yield habit

    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as file:
            json_data = [habit.to_dict() for habit in self.habits]
            json.dump(json_data, file, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as file:
                try:
                    json_data = json.load(file)
                    for item in json_data:
                        loaded_habit = Habit(
                            name=item["name"],
                            description=item["description"],
                            creation_date=item["creation_date"],
                            is_completed=item["is_completed"]
                        )
                        self.habits.append(loaded_habit)
                except json.JSONDecodeError:
                    pass