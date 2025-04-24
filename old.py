import json
import os
import tkinter as tk
from tkinter import messagebox
import webbrowser
import re

PASSWORD = "admin"
users_file = "users.json"
LOGIN = "admin"

if os.path.exists(users_file) and os.path.getsize(users_file) > 0:
    with open(users_file, "r", encoding="utf-8") as file:
        all_people = json.load(file)
else:
    all_people = []

root = tk.Tk()
root.title("User Info Base")
root.geometry("1000x700")
root.config(bg="white")
root.iconbitmap("db.ico")
# -------------------- ЛОГИН ЭКРАН --------------------
login_frame = tk.Frame(root, bg="#1e272e")
login_frame.place(relwidth=1, relheight=1)

tk.Label(login_frame, text="🔒 Login", font=("Arial", 28, "bold"), bg="#1e272e", fg="white").pack(pady=60)
tk.Label(login_frame, text="Username", font=("Arial", 20), bg="#1e272e", fg="white").pack(pady=0)
entry_login = tk.Entry(login_frame, font=("Arial", 18), width=25, justify='center')
entry_login.pack(pady=10)
tk.Label(login_frame, text="Password", font=("Arial", 20), bg="#1e272e", fg="white").pack(pady=0)
entry_password = tk.Entry(login_frame, font=("Arial", 18), show="*", width=25, justify='center')
entry_password.pack(pady=10)

def check_details():
    if not entry_login.get() or not entry_password.get():
        messagebox.showerror("Error", "Username and Password are required")
        return
    if entry_login.get() != LOGIN:
        return
    if entry_password.get() == PASSWORD:
        login_frame.destroy()
        show_main_app()
    else:
        messagebox.showerror("Error", "Username or Password is incorrect")

tk.Button(login_frame, text="LOGIN", font=("Arial", 16), bg="#20bf6b", fg="white", width=15, command=check_details).pack(pady=20)

# -------------------- ГЛАВНОЕ ПРИЛОЖЕНИЕ --------------------
def show_main_app():
    def open_support_link():
        webbrowser.open("https://tonviewer.com/EQA93O3YlQleajDjdOuaygtJ_U1bX_TOko9AZ7pJzyRSpsqX?section=tokens")
    def show_notification(message):
        notification_frame = tk.Frame(root, bg="#2ecc71")
        notification_frame.pack(side="bottom", fill="x")
        tk.Label(notification_frame, text=message, font=("Arial", 14), bg="#2ecc71", fg="white").pack()
        notification_frame.after(1500, notification_frame.destroy)  
    def show_notification_delete(message):
        notification_frame = tk.Frame(root, bg="red")
        notification_frame.pack(fill="x")
        tk.Label(notification_frame, text=message, font=("Arial", 14), bg="red", fg="white").pack()
        notification_frame.after(1500, notification_frame.destroy)  
    
    def update_people_list():
        listbox_people.delete(0, tk.END)
        for person in all_people:
            listbox_people.insert(tk.END, f"{person['Name']}, {person['Age']} yo, {person['Country']}, {person['Phone Number']}")
        user_count_label.config(text=f"👥 Total Users: {len(all_people)}")

    def validate_name(name):
    
        if not re.match("^[A-Za-zА-Яа-яЁё ]+$", name):
            messagebox.showerror("Error", "Name must contain only letters and spaces.")
            return False
        show_notification("User added successfully!")
        return True
        
    def validate_age(age):
        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a valid number.")
            return False
        age = int(age)
        if age < 1 or age > 100:
            messagebox.showerror("Error", "Age must be between 1 and 100.")
            return False
        return True

    def validate_country(country):
        if not country.strip():
            messagebox.showerror("Error", "Country cannot be empty.")
            return False
        return True

    def validate_phone_number(phone_number):
        if not phone_number.startswith("+") or not phone_number[1:].isdigit():
            messagebox.showerror("Error", "Phone number must start with '+' and contain only numbers.")
            return False
        return True

    def add_person():
        name = entry_name.get()
        age = entry_age.get()
        country = entry_country.get()
        number = entry_number.get()

      
        if not name or not age or not country or not number:
            messagebox.showerror("Error", "Fill all fields")
            return

        if not validate_name(name):
            return
        if not validate_age(age):
            return
        if not validate_country(country):
            return
        if not validate_phone_number(number):
            return


        person_data = {
            "Name": name,
            "Age": int(age),
            "Country": country,
            "Phone Number": number,
            "IsAdult": int(age) >= 18
        }

        all_people.append(person_data)
        with open(users_file, "w", encoding="utf-8") as file:
            json.dump(all_people, file, ensure_ascii=False, indent=2)
        
        update_people_list()
        clear_fields()

    def clear_fields():
        entry_name.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        entry_country.delete(0, tk.END)
        entry_number.delete(0, tk.END)

    def delete_person():
        selected = listbox_people.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a user to delete")
            return
        person = all_people[selected[0]]
        if messagebox.askyesno("Confirm", f"Delete {person['Name']}?"):
            show_notification_delete("User deleted successfully!")
            del all_people[selected[0]]
            with open(users_file, "w", encoding="utf-8") as file:
                json.dump(all_people, file, ensure_ascii=False, indent=2)
            update_people_list()

    def start_edit():
        nonlocal edit_mode, edit_index
        selected = listbox_people.curselection()
        if not selected:
            messagebox.showerror("Error", "Select a user to edit")
            return

        edit_index = selected[0]
        person = all_people[edit_index]

        entry_name.delete(0, tk.END)
        entry_name.insert(0, person["Name"])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, str(person["Age"]))
        entry_country.delete(0, tk.END)
        entry_country.insert(0, person["Country"])
        entry_number.delete(0, tk.END)
        entry_number.insert(0, person["Phone Number"])

        btn_add.config(text="Save Changes", bg="#3498db", command=save_edit)
        btn_edit.config(state="disabled")
        edit_mode = True

    def save_edit():
        nonlocal edit_mode, edit_index

        name = entry_name.get()
        age = entry_age.get()
        country = entry_country.get()
        number = entry_number.get()

        if not name or not age or not country or not number:
            messagebox.showerror("Error", "Fill all fields")
            return

        if not validate_name(name):
            return
        if not validate_age(age):
            return
        if not validate_country(country):
            return
        if not validate_phone_number(number):
            return

        all_people[edit_index] = {
            "Name": name,
            "Age": int(age),
            "Country": country,
            "Phone Number": number,
            "IsAdult": int(age) >= 18
        }

        with open(users_file, "w", encoding="utf-8") as file:
            json.dump(all_people, file, ensure_ascii=False, indent=2)

        update_people_list()
        clear_fields()
        btn_add.config(text="Add User", bg="#2ecc71", command=add_person)
        btn_edit.config(state="normal")
        edit_mode = False
        edit_index = None

   
    top_bar = tk.Frame(root, bg="#ffffff")
    top_bar.pack(fill="x", pady=10, padx=10)

    support_button = tk.Button(top_bar, text="❤️ Support Creator", font=("Arial", 12), bg="#ffdddd", command=open_support_link)
    support_button.pack(side="left", padx=5)

    user_count_label = tk.Label(top_bar, text="", font=("Arial", 14), bg="#ffffff")
    user_count_label.pack(side="right", padx=10)

    form_frame = tk.Frame(root, bg="#f0f0f0")
    form_frame.pack(pady=10, padx=10)

    tk.Label(form_frame, text="Name:", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, sticky="w")
    entry_name = tk.Entry(form_frame, font=("Arial", 14), width=30)
    entry_name.grid(row=0, column=1)

    tk.Label(form_frame, text="Age:", font=("Arial", 14), bg="#f0f0f0").grid(row=1, column=0, sticky="w")
    entry_age = tk.Entry(form_frame, font=("Arial", 14), width=30)
    entry_age.grid(row=1, column=1)

    tk.Label(form_frame, text="Country:", font=("Arial", 14), bg="#f0f0f0").grid(row=2, column=0, sticky="w")
    entry_country = tk.Entry(form_frame, font=("Arial", 14), width=30)
    entry_country.grid(row=2, column=1)

    tk.Label(form_frame, text="Phone Number:", font=("Arial", 14), bg="#f0f0f0").grid(row=3, column=0, sticky="w")
    entry_number = tk.Entry(form_frame, font=("Arial", 14), width=30)
    entry_number.grid(row=3, column=1)

    btn_frame = tk.Frame(root, bg="white")
    btn_frame.pack(pady=10)

    btn_add = tk.Button(btn_frame, text="Add User", font=("Arial", 14), bg="#2ecc71", fg="white", width=20, command=add_person)
    btn_add.pack(side="left", padx=5)

    btn_edit = tk.Button(btn_frame, text="Edit Selected", font=("Arial", 14), bg="#e67e22", fg="white", width=20, command=start_edit)
    btn_edit.pack(side="left", padx=5)

    btn_delete = tk.Button(btn_frame, text="Delete Selected", font=("Arial", 14), bg="#e74c3c", fg="white", width=20, command=delete_person)
    btn_delete.pack(side="left", padx=5)

    listbox_frame = tk.Frame(root)
    listbox_frame.pack(padx=10, pady=10, fill="both", expand=True)

    listbox_people = tk.Listbox(listbox_frame, font=("Courier", 14), width=80, height=10, bg="#ecf0f1")
    listbox_people.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox_people.yview)
    scrollbar.pack(side="right", fill="y")

    listbox_people.config(yscrollcommand=scrollbar.set)

    edit_mode = False
    edit_index = None

    update_people_list()

root.mainloop()
