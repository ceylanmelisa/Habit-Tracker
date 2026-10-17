from habit_manager import HabitTracker, InvalidHabitError


def main_menu():
    tracker = HabitTracker()

    while True:
        print("\n--- HABIT TRACKER ---")
        print("1. Add New Habit")
        print("2. List All Habits")
        print("3. List Pending Habits")  # Generator özelliğimiz için yeni menü seçeneği
        print("4. Exit")

        choice = input("Please select an option (1/2/3/4): ")

        if choice == '1':
            print("\n--- ADD NEW HABIT ---")
            name = input("Enter habit name (e.g., Reading): ")
            description = input("Enter habit description (e.g., 20 pages a day): ")

            try:
                # İsim ve açıklama alındıktan sonra doğrulama burada yapılıyor
                tracker.add_habit(name, description)
            except InvalidHabitError as e:
                # \033[91m kodu yazıyı kırmızı yapar, \033[0m kodu ise rengi tekrar normale çevirir
                print(f"\033[91m-> Error: {e}\033[0m")

        elif choice == '2':
            tracker.display_habits()

        elif choice == '3':
            print("\n--- PENDING HABITS ---")
            # Generator yapısını burada çağırıyoruz
            pending_generator = tracker.get_pending_habits_generator()
            has_pending = False

            for habit in pending_generator:
                print(habit)
                has_pending = True

            if not has_pending:
                print("-> No pending habits. Great job!")

        elif choice == '4':
            print("Exiting program. Goodbye!")
            break

        else:
            print("-> Invalid choice! Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main_menu()