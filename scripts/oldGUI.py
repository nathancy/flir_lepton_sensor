import Tkinter as tk
from subprocess import call

KML_filename = "KML_generator.py"
menufont = 40

def generate_KML_file():
    resolution = KML_resolution.get()
    call(["python", KML_filename, resolution])

# Create GUI, set resolution/title
gui = tk.Tk()
gui.geometry('800x800')
gui.title('Flir')

# KML resolution input field
generate_KML_resolution_scale = tk.Label(gui, text='KML Resolution').grid(row=0)
KML_resolution = tk.Entry(gui)
KML_resolution.focus_set()
KML_resolution.grid(row=0, column=1)
generate_KML_button = tk.Button(gui, text='Generate KML File', width=25, font=20,command=generate_KML_file).grid(row=1)



# Menu
menu = tk.Menu(gui, font=menufont)
gui.config(menu=menu)
filemenu = tk.Menu(menu, font=menufont)
menu.add_cascade(label='File', menu=filemenu, font=menufont)
filemenu.add_command(label='New', font=menufont)
filemenu.add_command(label='Open', font=menufont)
filemenu.add_separator()
filemenu.add_command(label='Exit', font=menufont, command=gui.quit)
helpmenu = tk.Menu(menu)
menu.add_cascade(label='Help', font=menufont, menu=helpmenu)
helpmenu.add_command(label='About', font=menufont)













gui.mainloop()

