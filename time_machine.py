#!/bin/env python3
'''Time machine program main file.'''

import tkinter as tk
from lxml import etree
from tkinter import scrolledtext

# Global variable initialization.
TIME_MACHINE_FILE = ".time_machine.xml"
INPUT_LIST = list()
NAME_BOXES = list()
DESCRIPTION_BOXES = list()

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
    out_root = etree.Element("root")
    n = 0 #count
    for i in range(len(NAME_BOXES)):
        ntext = NAME_BOXES[i].get().strip()
        dtext = DESCRIPTION_BOXES[i].get(1.0, tk.END).strip()

        # Only write if some entry.
        if len(ntext) + len(dtext) > 0:
            n = n + 1
            pers = etree.SubElement(out_root, "pers")
            name = etree.SubElement(pers, "name")
            name.text = ntext

            description = etree.SubElement(pers, "description")
            description.text = dtext

    out_tree = etree.ElementTree(out_root)
    out_tree.write(TIME_MACHINE_FILE, pretty_print=True)
    print("Done saving data to {}, {} entries.".format(TIME_MACHINE_FILE, n))

# GUI init and buttons.
WINDOW = tk.Tk()
WINDOW.title("Time machine")
save_btn = tk.Button(WINDOW, text="Save", command=save_xml)
add_btn = tk.Button(WINDOW, text="Add Entry", command=add_empty_entry)
save_btn.grid(column=1, row=0)
add_btn.grid(column=0, row=0)

# Parse xml input.
XML_IN = etree.parse(TIME_MACHINE_FILE).getroot()

# Read list of person content from xml elements.
for pers in XML_IN:
    INPUT_LIST.append({'name': pers[0].text,
                        'description': pers[1].text})
print("Done reading data from {}, {} entries.".format(TIME_MACHINE_FILE,
                                                len(INPUT_LIST)))

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
