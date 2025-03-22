import ctypes
import random
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WATCHLIST_PATH = os.path.join(SCRIPT_DIR, 'watchlist.txt')

# Global variable to store last picked item
last_picked = None

# Function to minimize the command prompt window (works on Windows)
def minimize_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd != 0:
        ctypes.windll.user32.ShowWindow(hwnd, 6)  # 6 = SW_MINIMIZE

# Function to load the list of movies and TV shows from the watchlist file
def load_list(filename, choice):
    try:
        with open(WATCHLIST_PATH, 'r') as file:
            lines = file.readlines()
        
        items = []
        section_found = False
        for line in lines:
            line = line.strip()
            # Handle the Kids section specially since it doesn't have an 's'
            if choice == 'Kids' and line == '# Kids':
                section_found = True
            elif line == f"# {choice}s":
                section_found = True
            elif section_found and line and not line.startswith('#'):
                items.append(line)
            elif section_found and line.startswith('#'):
                break
        
        return items
    except FileNotFoundError:
        messagebox.showerror("Error", f"Could not find {filename}. Please make sure the file exists in the same directory as the program.")
        return []
    except Exception as e:
        messagebox.showerror("Error", f"Error reading {filename}: {str(e)}")
        return []

# Function to save item to watchlist
def save_item(new_item, item_type):
    try:
        with open(WATCHLIST_PATH, 'r') as file:
            lines = file.readlines()
        
        section_found = False
        for i, line in enumerate(lines):
            if line.strip() == f"# {item_type}s":
                lines.insert(i + 1, new_item + '\n')
                section_found = True
                break
        
        if not section_found:
            lines.append(f"\n# {item_type}s\n")
            lines.append(new_item + '\n')
        
        with open(WATCHLIST_PATH, 'w') as file:
            file.writelines(lines)
        
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save item: {str(e)}")
        return False

# Function to remove item from watchlist
def remove_item_from_list(item, choice):
    try:
        with open(WATCHLIST_PATH, 'r') as file:
            lines = file.readlines()
        
        # Find and remove the item
        new_lines = []
        skip_next = False
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
            if line.strip() == item:
                skip_next = True
                continue
            new_lines.append(line)
        
        with open(WATCHLIST_PATH, 'w') as file:
            file.writelines(new_lines)
        
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to remove item: {str(e)}")
        return False

# Function to choose a random movie or TV show from the list
def choose_item(choice):
    global last_picked
    item_list = load_list(WATCHLIST_PATH, choice)
    if not item_list:
        return f"Error: No {choice} content found in the watchlist. Please check the watchlist.txt file."
    selected_item = random.choice(item_list)
    last_picked = (choice, selected_item, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    update_result()
    return f"How about watching: {selected_item} ({choice})"

# Function to update the result label based on the user's choice
def update_choice(choice):
    result = choose_item(choice)
    result_label.config(
        text=f"How about watching:\n{result.split(': ')[1]}",
        fg='#000080',
        justify='center'  # Center alignment
    )

# Function to update the result display
def update_result():
    if last_picked:
        result_label.config(
            text=f"How about watching:\n{last_picked[1]} ({last_picked[0]})\n{last_picked[2]}",
            fg='#000080',  # Windows 95 navy blue
            justify='center'  # Center alignment
        )
    else:
        result_label.config(
            text="Choose whether to watch a Movie, TV Show, or Kids content",
            fg='black',
            justify='center'
        )

# Function to show the view list dialog
def view_list(choice=None):
    if not choice:
        # Create category selection dialog
        dialog = tk.Toplevel(root)
        dialog.title("Select Category")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.configure(bg='#c0c0c0')
        
        dialog.transient(root)
        dialog.grab_set()
        
        # Create frame for buttons
        button_frame = tk.Frame(dialog, bg='#c0c0c0')
        button_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        def show_category(category):
            dialog.destroy()
            show_list_dialog(category)
        
        # Create category buttons
        tk.Button(button_frame, text="Movies", 
                 command=lambda: show_category('Movie'),
                 font=("MS Sans Serif", 10),
                 relief='raised',
                 bd=2,
                 bg='#c0c0c0').pack(pady=5)
        
        tk.Button(button_frame, text="TV Shows", 
                 command=lambda: show_category('TV Show'),
                 font=("MS Sans Serif", 10),
                 relief='raised',
                 bd=2,
                 bg='#c0c0c0').pack(pady=5)
        
        tk.Button(button_frame, text="Kids", 
                 command=lambda: show_category('Kids'),
                 font=("MS Sans Serif", 10),
                 relief='raised',
                 bd=2,
                 bg='#c0c0c0').pack(pady=5)
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')
        return
    
    show_list_dialog(choice)

def show_list_dialog(choice):
    dialog = tk.Toplevel(root)
    dialog.title(f"View {choice} List")
    dialog.geometry("400x500")
    dialog.resizable(False, False)
    dialog.configure(bg='#c0c0c0')
    
    # Make dialog modal
    dialog.transient(root)
    dialog.grab_set()
    
    # Create title bar frame with gradient effect
    title_frame = tk.Frame(dialog, height=25, bg='#000080')
    title_frame.pack(fill='x', side='top')
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(title_frame, 
                          text=f"View {choice} List",
                          font=("MS Sans Serif", 10, "bold"),
                          fg='white',
                          bg='#000080')
    title_label.pack(expand=True, fill='both', padx=5, pady=2)
    
    # Create frame for list with 3D border
    list_frame = tk.Frame(dialog, bg='#c0c0c0', relief='sunken', bd=2)
    list_frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Create listbox with Windows 95 style
    listbox = tk.Listbox(list_frame, 
                        font=("MS Sans Serif", 10), 
                        bg='#ffffff',
                        selectmode='single',
                        relief='sunken',
                        bd=2,
                        selectbackground='#000080',
                        selectforeground='white',
                        highlightthickness=1,
                        highlightcolor='#c0c0c0',
                        highlightbackground='#c0c0c0')
    listbox.pack(fill='both', expand=True, padx=2, pady=2)
    
    # Add scrollbar with Windows 95 style
    scrollbar = tk.Scrollbar(listbox, 
                            bg='#c0c0c0',
                            activebackground='#a0a0a0',
                            troughcolor='#c0c0c0',
                            width=16,
                            relief='sunken',
                            bd=2)
    scrollbar.pack(side='right', fill='y')
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    # Populate list
    items = load_list(WATCHLIST_PATH, choice)
    for item in items:
        listbox.insert('end', item)
    
    # Create frame for buttons with 3D border
    button_frame = tk.Frame(dialog, bg='#c0c0c0', relief='sunken', bd=2)
    button_frame.pack(fill='x', padx=10, pady=5)
    
    def remove_selected():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
            
        item = listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Remove '{item}' from {choice}s?"):
            try:
                with open(WATCHLIST_PATH, 'r') as file:
                    lines = file.readlines()
                
                # Find and remove the item
                new_lines = []
                skip_next = False
                for i, line in enumerate(lines):
                    if skip_next:
                        skip_next = False
                        continue
                    if line.strip() == item:
                        skip_next = True
                        continue
                    new_lines.append(line)
                
                with open(WATCHLIST_PATH, 'w') as file:
                    file.writelines(new_lines)
                
                # Update the listbox
                listbox.delete(selection[0])
                messagebox.showinfo("Success", f"Removed '{item}' from {choice}s")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove item: {str(e)}")
    
    def add_new_item():
        dialog.destroy()  # Close the list view dialog
        add_new_item_dialog(choice)  # Open the add new item dialog with the current category
    
    def go_back():
        dialog.destroy()  # Close the list view dialog
        view_list()  # Reopen the category selection dialog
    
    # Add buttons with Windows 95 style
    back_button = tk.Button(button_frame, 
                          text="Back",
                          command=go_back,
                          font=("MS Sans Serif", 10),
                          relief='raised',
                          bd=2,
                          bg='#c0c0c0',
                          activebackground='#a0a0a0',
                          activeforeground='black',
                          cursor='hand2')
    back_button.pack(side='right', padx=5)
    
    add_button = tk.Button(button_frame, 
                         text="Add New Item",
                         command=add_new_item,
                         font=("MS Sans Serif", 10),
                         relief='raised',
                         bd=2,
                         bg='#c0c0c0',
                         activebackground='#a0a0a0',
                         activeforeground='black',
                         cursor='hand2')
    add_button.pack(side='left', padx=5)
    
    remove_button = tk.Button(button_frame, 
                            text="Remove Selected",
                            command=remove_selected,
                            font=("MS Sans Serif", 10),
                            relief='raised',
                            bd=2,
                            bg='#c0c0c0',
                            activebackground='#a0a0a0',
                            activeforeground='black',
                            cursor='hand2')
    remove_button.pack(side='left', padx=5)
    
    # Center the dialog
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')

def add_new_item_dialog(choice=None):
    dialog = tk.Toplevel(root)
    dialog.title("Add New Item")
    dialog.geometry("300x200")
    dialog.resizable(False, False)
    dialog.configure(bg='#c0c0c0')
    
    dialog.transient(root)
    dialog.grab_set()
    
    type_frame = tk.Frame(dialog, bg='#c0c0c0')
    type_frame.pack(fill='x', padx=20, pady=10)
    
    input_frame = tk.Frame(dialog, bg='#c0c0c0')
    input_frame.pack(fill='x', padx=20, pady=10)
    
    item_type = tk.StringVar(value=choice if choice else "Movie")
    
    tk.Radiobutton(type_frame, text="Movie", variable=item_type, value="Movie",
                   bg='#c0c0c0', font=("MS Sans Serif", 10)).pack(side='left', padx=10)
    tk.Radiobutton(type_frame, text="TV Show", variable=item_type, value="TV Show",
                   bg='#c0c0c0', font=("MS Sans Serif", 10)).pack(side='left', padx=10)
    tk.Radiobutton(type_frame, text="Kids", variable=item_type, value="Kids",
                   bg='#c0c0c0', font=("MS Sans Serif", 10)).pack(side='left', padx=10)
    
    entry = tk.Entry(input_frame, font=("MS Sans Serif", 10))
    entry.pack(fill='x', pady=5)
    
    def save_item():
        new_item = entry.get().strip()
        if not new_item:
            messagebox.showerror("Error", "Please enter a title")
            return
            
        try:
            with open(WATCHLIST_PATH, 'r') as file:
                lines = file.readlines()
            
            section_found = False
            for i, line in enumerate(lines):
                if line.strip() == f"# {item_type.get()}s":
                    lines.insert(i + 1, new_item + '\n')
                    section_found = True
                    break
            
            if not section_found:
                lines.append(f"\n# {item_type.get()}s\n")
                lines.append(new_item + '\n')
            
            with open(WATCHLIST_PATH, 'w') as file:
                file.writelines(lines)
            
            messagebox.showinfo("Success", f"{item_type.get()} content added successfully!")
            dialog.destroy()
            
            # If we came from the list view, reopen it
            if choice:
                view_list(choice)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add item: {str(e)}")
    
    save_button = tk.Button(dialog, text="Save", command=save_item,
                          font=("MS Sans Serif", 10), relief='raised', bd=2, bg='#c0c0c0')
    save_button.pack(pady=10)
    
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')

# Function to handle button hover effects
def on_enter(e):
    e.widget['relief'] = 'sunken'

def on_leave(e):
    e.widget['relief'] = 'raised'

# Function to pick random from all categories
def pick_random_all():
    categories = ['Movie', 'TV Show', 'Kids']
    category = random.choice(categories)
    update_choice(category)

# Function to add new item to watchlist
def add_new_item():
    add_new_item_dialog()

# Minimize the console window when the GUI starts
minimize_console()

# Create the main window (root) for the GUI
root = tk.Tk()
root.title("WatchWizard - Movie & TV Show Picker")
root.geometry("400x450")  # Increased height to show all buttons
root.resizable(False, False)

# Configure the root window style
root.configure(bg='#c0c0c0')

# Create title bar frame with gradient effect
title_frame = tk.Frame(root, height=25, bg='#000080')
title_frame.pack(fill='x', side='top')
title_frame.pack_propagate(False)

title_label = tk.Label(title_frame, 
                      text="WatchWizard",
                      font=("MS Sans Serif", 10, "bold"),
                      fg='white',
                      bg='#000080')
title_label.pack(expand=True, fill='both', padx=5, pady=2)

# Create main container frame with 3D border
main_frame = tk.Frame(root, bg='#c0c0c0', relief='sunken', bd=2)
main_frame.pack(expand=True, fill='both', padx=10, pady=10)

# Create a frame for the result label with 3D border
result_frame = tk.Frame(main_frame, height=120, bg='#c0c0c0', relief='sunken', bd=2)
result_frame.pack(fill='x', pady=(0, 20))
result_frame.pack_propagate(False)

result_label = tk.Label(result_frame, 
                       text="Choose whether to watch a Movie, TV Show, or Kids content", 
                       font=("MS Sans Serif", 10),
                       wraplength=380,  # Increased wraplength
                       justify="center",
                       bg='#ffffff',
                       padx=10,  # Added horizontal padding
                       pady=5)   # Added vertical padding
result_label.pack(expand=True, fill='both', padx=2, pady=2)

# Create a frame for the buttons with 3D border
button_frame = tk.Frame(main_frame, bg='#c0c0c0', relief='sunken', bd=2)
button_frame.pack(fill='x', pady=20)

# Create buttons with hover effects and tooltips
def create_button(parent, text, command, tooltip):
    button = tk.Button(parent, 
                      text=text,
                      font=("MS Sans Serif", 10),
                      command=command,
                      relief='raised',
                      bd=2,
                      bg='#c0c0c0',
                      activebackground='#a0a0a0',  # Darker shade when clicked
                      activeforeground='black',
                      cursor='hand2')  # Hand cursor on hover
    button.pack(pady=3, fill='x', padx=10)  # Reduced vertical padding between buttons
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)
    
    # Create tooltip
    def show_tooltip(event):
        tooltip_window = tk.Toplevel()
        tooltip_window.wm_overrideredirect(True)
        tooltip_window.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        label = tk.Label(tooltip_window, text=tooltip, 
                        bg='#ffffe0', relief='solid', borderwidth=1,
                        font=("MS Sans Serif", 9))
        label.pack()
        
        def hide_tooltip(event):
            tooltip_window.destroy()
        
        button.bind('<Leave>', hide_tooltip)
        tooltip_window.bind('<Leave>', hide_tooltip)
    
    button.bind('<Enter>', show_tooltip)
    return button

# Create all buttons with tooltips
movie_button = create_button(button_frame, "Pick a Movie (M)", 
                           lambda: update_choice('Movie'),
                           "Pick a random movie from the list")

tv_button = create_button(button_frame, "Pick a TV Show (T)", 
                         lambda: update_choice('TV Show'),
                         "Pick a random TV show from the list")

kids_button = create_button(button_frame, "Pick Kids Content (K)",
                          lambda: update_choice('Kids'),
                          "Pick random kids content from the list")

random_all_button = create_button(button_frame, "Pick Random from All (R)",
                                pick_random_all,
                                "Pick random content from any category")

view_list_button = create_button(button_frame, "View List (V)",
                               lambda: view_list(),
                               "View all items in any category")

# Update keyboard shortcuts
root.bind('<m>', lambda e: update_choice('Movie'))
root.bind('<t>', lambda e: update_choice('TV Show'))
root.bind('<k>', lambda e: update_choice('Kids'))
root.bind('<r>', lambda e: pick_random_all())
root.bind('<v>', lambda e: view_list())

# Run the GUI application
root.mainloop()
