from tkinter import *
import sqlite3


root = Tk()
root.title("GUI Database")
screen_x = root.winfo_screenwidth()
screen_y = root.winfo_screenheight()
window_x = 356
window_y = 600
pos_X = int((screen_x - window_x) / 2)
pos_Y = int((screen_y - window_y) / 2)
root.geometry(f"{window_x}x{window_y}+{pos_X}+{pos_Y}")


# Create Function to delete a record

def delete():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect("../Projects1/ProjetInfo/database.db")
    # Create a cursor
    c = conn.cursor()

    # Delete a record
    c.execute(f"DELETE from addresses WHERE oid={select_box.get()}")

    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()


# Create Submit Function for database
# Create Submit button

def submit():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect("../Projects1/ProjetInfo/database.db")
    # Create a cursor
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS addresses 
    (f_name text,
    l_name text,
    address text,
    city text,
    state text,
    zipcode text)""")

    # Insert into table
    c.execute("INSERT INTO addresses VALUES (:f_name, :l_name, :address, :city, :state, :zipcode)",
                   {
                       'f_name': str(f_name.get()),
                       'l_name': str(l_name.get()),
                       'address': str(address.get()),
                       'city': str(city.get()),
                       'state': str(state.get()),
                       'zipcode': str(zipcode.get())
                   })

    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()

    # Clear the Text Boxes
    f_name.delete(0, END)
    l_name.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    address.delete(0, END)
    zipcode.delete(0, END)


# Create Query Function

def query():
    # Create a cursor inside the function
    # Create a database or connect to one
    conn = sqlite3.connect("../Projects1/ProjetInfo/database.db")
    # Create a cursor
    c = conn.cursor()

    # Query The database
    c.execute("SELECT *, oid FROM addresses")
    records = c.fetchall()

    print_records = ""
    for record in records:
        for item in record:
            print_records += str(item) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=11, column=0, columnspan=2)

    # Commit changes
    conn.commit()
    # Close Connection
    conn.close()


# Create an Update function to update the new stuff that was input inside the Entry boxes

def update():
    conn = sqlite3.connect("../Projects1/ProjetInfo/database.db")
    c = conn.cursor()

    record_id = select_box.get()
    c.execute(f"""UPDATE addresses SET
    f_name = :first_name,
    l_name = :last_name,
    address = :address,
    city = :city,
    state = :state,
    zipcode = :zipcode 
    
    WHERE oid = :oid""",
              {
                  "first_name": f_name_editor.get(),
                  "last_name": l_name_editor.get(),
                  "address": address_editor.get(),
                  "city": city_editor.get(),
                  "state": state_editor.get(),
                  "zipcode": zipcode_editor.get(),

                  "oid": record_id})
    conn.commit()
    conn.close()
    editor.destroy()


# Create Edit function to update a record

def edit():
    global editor
    editor = Toplevel()
    editor.title("Update a Record")
    screen_x_2 = editor.winfo_screenwidth()
    screen_y_2 = editor.winfo_screenheight()
    window_x_2 = 356
    window_y_2 = 250
    pos_x_2 = int((screen_x_2 - window_x_2) / 2)
    pos_y_2 = int((screen_y_2 - window_y_2) / 2)
    editor.geometry(f"{window_x_2}x{window_y_2}+{pos_x_2}+{pos_y_2}")

    # Create Global Variables for text box names

    global f_name_editor, l_name_editor, address_editor, city_editor, state_editor, zipcode_editor

    # Create Text Boxes

    f_name_editor = Entry(editor, width=30)
    f_name_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

    l_name_editor = Entry(editor, width=30)
    l_name_editor.grid(row=1, column=1, padx=20)

    address_editor = Entry(editor, width=30)
    address_editor.grid(row=2, column=1, padx=20)

    city_editor = Entry(editor, width=30)
    city_editor.grid(row=3, column=1, padx=20)

    state_editor = Entry(editor, width=30)
    state_editor.grid(row=4, column=1, padx=20)

    zipcode_editor = Entry(editor, width=30)
    zipcode_editor.grid(row=5, column=1, padx=20)

    delete_box_editor = Entry(editor, width=30)
    delete_box_editor.grid(row=8, column=1, padx=20)

    # Create Text Box Labels

    f_name_label_editor = Label(editor, text="First Name")
    f_name_label_editor.grid(row=0, column=0, pady=(10, 0))

    l_name_label_editor = Label(editor, text="Last Name")
    l_name_label_editor.grid(row=1, column=0)

    address_label_editor = Label(editor, text="Address")
    address_label_editor.grid(row=2, column=0)

    city_label_editor = Label(editor, text="City")
    city_label_editor.grid(row=3, column=0)

    state_label_editor = Label(editor, text="State")
    state_label_editor.grid(row=4, column=0)

    zip_code_label_editor = Label(editor, text="Zip Code")
    zip_code_label_editor.grid(row=5, column=0)

    delete_box_label_editor = Label(editor, text="Select ID")
    delete_box_label_editor.grid(row=8, column=0)

    # Create a save Button to save an edited record
    save_btn = Button(editor, text="Save Record", command=update)
    save_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=131)

    # Connection start
    conn = sqlite3.connect("../Projects1/ProjetInfo/database.db")
    c = conn.cursor()

    record_id = select_box.get()

    c.execute(f"SELECT * FROM addresses WHERE oid={record_id}")
    records = c.fetchall()

    # Loop through the results
    for record in records:
        f_name_editor.insert(0, record[0])
        l_name_editor.insert(0, record[1])
        address_editor.insert(0, record[2])
        city_editor.insert(0, record[3])
        state_editor.insert(0, record[4])
        zipcode_editor.insert(0, record[5])

    conn.commit()
    conn.close()

    editor.mainloop()


# Create Text Boxes

f_name = Entry(root, width=30)
f_name.grid(row=0, column=1, padx=20, pady=(10, 0))

l_name = Entry(root, width=30)
l_name.grid(row=1, column=1, padx=20)

address = Entry(root, width=30)
address.grid(row=2, column=1, padx=20)

city = Entry(root, width=30)
city.grid(row=3, column=1, padx=20)

state = Entry(root, width=30)
state.grid(row=4, column=1, padx=20)

zipcode = Entry(root, width=30)
zipcode.grid(row=5, column=1, padx=20)

select_box = Entry(root, width=30)
select_box.grid(row=8, column=1, padx=20)

# Create Text Box Labels

f_name_label = Label(root, text="First Name")
f_name_label.grid(row=0, column=0, pady=(10, 0))

l_name_label = Label(root, text="Last Name")
l_name_label.grid(row=1, column=0)

address_label = Label(root, text="Address")
address_label.grid(row=2, column=0)

city_label = Label(root, text="City")
city_label.grid(row=3, column=0)

state_label = Label(root, text="State")
state_label.grid(row=4, column=0)

zip_code_label = Label(root, text="Zip Code")
zip_code_label.grid(row=5, column=0)

delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=8, column=0)

# Create Submit Button
submit_button = Button(root, text="Add record to database", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Create a Query Button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=124)

# Create a delete button
query_btn = Button(root, text="Delete Record", command=delete)
query_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=125)

# Create an update button
edit_btn = Button(root, text="Edit Record", command=edit)
edit_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=131)

root.mainloop()
