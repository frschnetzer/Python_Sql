import pyodbc
import customtkinter
from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
import os

win = Tk()

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

try:
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=(localdb)\MSSQLLocalDB;DATABASE=SampleDB;Trusted_Connection=yes')

    cursor = connection.cursor()

except pyodbc.Error as ex:
    print("Failed to connect to Database: {}".format(ex))

table_li = []


def select():
    try:
        cursor.execute("SELECT * FROM Person ORDER BY FirstName")
        result = cursor.fetchall()

        for entry in result:
            table_li.insert(entry)
            print(entry)
    except Exception as ex:
        print("An error occurred while selecting from database: ".format(ex))


def insert(person_id, first_name, last_name, address, city):
    sql = f"INSERT INTO Person (PersonID, FirstName, LastName, Address, City) VALUES ({person_id}, {first_name}," \
          f"{last_name}, {address}, {city})"
    cursor.execute(sql)

    connection.commit()

    print(cursor.rowcount, "record inserted...")


def select_one(person_id):
    try:
        cursor.execute(f"SELECT * FROM Person WHERE PersonID = {person_id}")
        result = cursor.fetchall()

        for entry in result:
            print(entry)
        return True
    except Exception as ex:
        return False


def delete(person_id):
    try:
        if select_one(person_id):
            sql = f"DELETE FROM Person WHERE PersonID = {person_id}"
            cursor.execute(sql)

            connection.commit()

            print(cursor.rowcount, "record(s) deleted")
        else:
            print("Person Id is not correct. Enter a valid Id Number!")
    except Exception as ex:
        print("Some error occured while deleting an element from database: ".format(ex))


def update(column, new_value, person_id):
    if column == "" or new_value == "" or person_id == "":
        print("string is empty")
    else:
        try:
            sql = f"UPDATE Person SET {column} = '{new_value}' WHERE PersonID = {person_id}"
            cursor.execute(sql)

            connection.commit()
            print(cursor.rowcount, "record(s) affected")
        except Exception as ex:
            print("Some error occurred while updating database: ".format(ex))


def select_top(count):
    if count > 0:
        try:
            sql = f"SELECT TOP {count} * FROM Person"
            cursor.execute(sql)

            result = cursor.fetchall()

            for entry in result:
                print(entry)
        except Exception as ex:
            print("Some error occured while selecting from database: ".format(ex))
    else:
        print("Number must be greater than 0!")


# select()
# select_top(10)
# update('FirstName', 'Lisa', '5')
# insert(5, 'Helen', 'Doe', 'Beachalley 62', 'Beachcity')
# delete(5)


cursor.close()
connection.close()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("450x260")
        self.title("CustomTkinter example_button_images.py")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, minsize=200)

        self.frame_1 = customtkinter.CTkFrame(master=self, width=250, height=240, corner_radius=15)
        self.frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_1.grid_columnconfigure(0, weight=1)
        self.frame_1.grid_columnconfigure(1, weight=1)
        # self.frame_1.configure(image=self.load_image(r"\test_images\bg_gradient.jpg", 20))

        self.add_user_image = self.load_image(r"\test_images\add-user.png", 20)

        self.button_5 = customtkinter.CTkButton(master=self, image=self.add_user_image, text="Add User", width=130,
                                                height=60, border_width=2,
                                                corner_radius=10, compound="bottom", border_color="#D35B58",
                                                fg_color=("gray84", "gray25"),
                                                hover_color="#C77C78", command=self.button_function)
        self.button_5.grid(row=0, column=1, padx=20, pady=20)

        tree = ttk.Treeview(win, column=("PersonId", "FirstName", "LastName", "Address", "City"), show='headings',
                            height=5)
        tree.column("# 1", anchor=CENTER)
        tree.heading("# 1", text="FirstName")
        tree.column("# 2", anchor=CENTER)
        tree.heading("# 2", text="LastName")
        tree.column("# 3", anchor=CENTER)
        tree.heading("# 3", text="Address")
        tree.column("# 4", anchor=CENTER)
        tree.heading("# 4", text="City")

        for item in table_li:
            tree.insert(item)

    def load_image(self, path, image_size):
        """ load rectangular image with path relative to PATH """
        return ImageTk.PhotoImage(Image.open(PATH + path).resize((image_size, image_size)))

    def button_function(self):
        print("button pressed")


if __name__ == "__main__":
    app = App()
    app.mainloop()

    cursor.close()
    connection.close()
