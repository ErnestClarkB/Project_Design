import serial.tools.list_ports
import tkinter as tk

def show_ports():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        listbox.insert(tk.END, p)

root = tk.Tk()
root.title("Arduino Ports")

frame = tk.Frame(root)
frame.pack()

listbox = tk.Listbox(frame)
listbox.pack()

button = tk.Button(frame, text="Show Ports", command=show_ports)
button.pack()

root.mainloop()
