#!/bin/env python3
'''Time machine program main file.'''

import os.path as path
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import scrolledtext

# Global variable initialization.
TM_FILE = path.expanduser("~/.time_machine.xml")
TM_FILE_HEADER = "<root>\n</root>\n"
INPUT_LIST = list()
NAME_BOXES = list()
DESCRIPTION_BOXES = list()

def init_tm_file():
    """Check existence of TM file and create it if not."""
    if not path.isfile(TM_FILE):
        with open(TM_FILE, 'w') as tm_file:
            tm_file.write(TM_FILE_HEADER)
        print("Initialized time_machine file in {}.".format(TM_FILE))

def add_empty_entry():
    """Adds a empty graphical container for a new entry."""
    NAME_BOXES.append(tk.Entry(WINDOW))
    NAME_BOXES[-1].grid(column=0, row=len(NAME_BOXES))
    NAME_BOXES[-1].insert(tk.END, "")

    DESCRIPTION_BOXES.append(scrolledtext.ScrolledText(WINDOW, height=10))
    DESCRIPTION_BOXES[-1].grid(column=1, row=len(DESCRIPTION_BOXES))
    DESCRIPTION_BOXES[-1].insert(tk.INSERT, "")
    print("New entry added.")

def save_xml():
    """Write current entry content to the xml config file."""
    out_root = ET.Element("root")
    n = 0 #count
    for i in range(len(NAME_BOXES)):
        ntext = NAME_BOXES[i].get().strip()
        dtext = DESCRIPTION_BOXES[i].get(1.0, tk.END).strip()

        # Only write if some entry.
        if len(ntext) + len(dtext) > 0:
            n = n + 1
            pers = ET.SubElement(out_root, "pers")
            name = ET.SubElement(pers, "name")
            name.text = ntext

            description = ET.SubElement(pers, "description")
            description.text = dtext

    out_tree = ET.ElementTree(out_root)
    out_tree.write(TM_FILE, xml_declaration=True)
    print("Done saving data to {}, {} entries.".format(TM_FILE, n))

def close_window():
    """Closes the window, terminating the program."""
    WINDOW.destroy()

# GUI window.
WINDOW = tk.Tk()
WINDOW.title("Time machine")

# Add button.
add_btn = tk.Button(WINDOW, text="Add Entry", command=add_empty_entry)
add_btn.grid(column=0, row=0)

# Save button.
save_btn = tk.Button(WINDOW, text="Save", command=save_xml)
save_btn.grid(column=1, row=0)

# Close button.
close_btn = tk.Button(WINDOW, text="Close", command=close_window)
close_btn.grid(column=2, row=0)

# Initialize XML file.
init_tm_file()

# Parse xml file and read initial list of person content from xml elements.
INPUT_LIST = [{'name': pers[0].text,
               'description': pers[1].text} for pers in ET.parse(TM_FILE).getroot()]
print("Done reading data from {}, {} entries.".format(TM_FILE, len(INPUT_LIST)))

# Render the data in the graphical window and populate list of widgets.
for i, pers in enumerate(INPUT_LIST):
    NAME_BOXES.append(tk.Entry(WINDOW))
    NAME_BOXES[-1].grid(column=0, row=i + 1)
    NAME_BOXES[-1].insert(tk.END, pers['name'])

    DESCRIPTION_BOXES.append(scrolledtext.ScrolledText(WINDOW, height=10))
    DESCRIPTION_BOXES[-1].grid(column=1, row=i + 1)
    DESCRIPTION_BOXES[-1].insert(tk.INSERT, pers['description'])

# Main sequence.
WINDOW.mainloop()
