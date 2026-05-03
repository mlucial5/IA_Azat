import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
import os

# Файл для сохранения истории
HISTORY_FILE = "quote_history.json"

# Список предопределённых цитат
quotes = [
    {"text": "Жизнь — это то, что происходит с тобой, пока ты строишь другие планы.", "author": "Джон Леннон", "topic": "Философия"},
    {"text": "Единственный способ сделать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс", "topic": "Мотивация"},
    {"text": "В середине трудности лежит возможность.", "author": "Альберт Эйнштейн", "topic": "Преодоление"},
    {"text": "Будь изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "topic": "Саморазвитие"},
    {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль", "topic": "Успех"}
]

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Quote Generator")
        self.root.geometry("600x500")

        # Загрузка истории
        self.history = self.load_history()

        self.setup_ui()

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Кнопка генерации
        generate_btn = ttk.Button(main_frame, text="Сгенерировать цитату", command=self.generate_quote)
        generate_btn.grid(row=0, column=0, pady=10, sticky=tk.W)

        # Отображение цитаты
        self.quote_text = tk.StringVar()
        self.author_text = tk.StringVar()
        self.topic_text = tk.StringVar()

        ttk.Label(main_frame, textvariable=self.quote_text, wraplength=500, font=("Arial", 12)).grid(row=1, column=0, pady=5)
        ttk.Label(main_frame, textvariable=self.author_text, font=("Arial", 10, "italic")).grid(row=2, column=0, pady=2)
        ttk.Label(main_frame, textvariable=self.topic_text, font=("Arial", 9)).grid(row=3, column=0, pady=2)

        # Фильтры
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтры", padding="5")
        filter_frame.grid(row=4, column=0, pady=10, sticky=(tk.W, tk.E), columnspan=2)

        ttk.Label(filter_frame, text="Автор:").grid(row=0, column=0, padx=5)
        self.author_filter = ttk.Combobox(filter_frame, state="readonly")
        self.author_filter.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Тема:").grid(row=0, column=2, padx=5)
        self.topic_filter = ttk.Combobox(filter_frame, state="readonly")
        self.topic_filter.grid(row=0, column=3, padx=5)

        filter_btn = ttk.Button(filter_frame, text="Применить фильтры", command=self.apply_filters)
        filter_btn.grid(row=0, column=4, padx=5)

        # История
        history_frame = ttk.LabelFrame(main_frame, text="История цитат", padding="5")
        history_frame.grid(row=5, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S), columnspan=2)

        self.history_list = tk.Listbox(history_frame, height=8)
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_list.yview)
        self.history_list.configure(yscrollcommand=scrollbar.set)

        self.history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Обновление фильтров
        self.update_filters()

    def generate_quote(self):
        filtered_quotes = self.get_filtered_quotes()
        if not filtered_quotes:
            messagebox.showwarning("Предупреждение", "По заданным фильтрам нет цитат!")
            return

        quote = random.choice(filtered_quotes)
        self.display_quote(quote)
        self.add_to_history(quote)

    def display_quote(self, quote):
        self.quote_text.set(quote["text"])
        self.author_text.set(f"— {quote['author']}")
        self.topic_text.set(f"Тема: {quote['topic']}")

    def add_to_history(self, quote):
        history_entry = f"{quote['text']} — {quote['author']}"
        self.history.append(quote)
        self.history_list.insert(tk.END, history_entry)
        self.save_history()

    def get_filtered_quotes(self):
        author = self.author_filter.get()
        topic = self.topic_filter.get()

        filtered = quotes
        if author:
            filtered = [q for q in filtered if q["author"] == author
        if topic:
            filtered = [q for q in filtered if q["topic"] == topic
        return filtered

    def apply_filters(self):
        self.history_list.delete(0, tk.END)
        for quote in self.history:
            if self.matches_filters(quote):
                self.history_list.insert(tk.END, f"{quote['text']} — {quote['author']}")

    def matches_filters(self, quote):
        author = self.author_filter.get()
        topic = self.topic_filter.get()
        if author and quote["author"] != author:
            return False
        if topic and quote["topic"] != topic:
            return False
        return True

    def update_filters(self):
        authors = sorted(set(q["author"] for q in quotes))
        topics = sorted(set(q["topic"] for q in quotes))
        self.author_filter["values"] = [""] + authors
        self.topic_filter["values"] = [""] + topics

    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить историю: {e}")

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()
