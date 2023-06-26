import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from lxml import etree
import time


def comment_out_tags(xml_file, target_string):
    try:
        # Parse the XML file
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        root = tree.getroot()

        # Convert target string to lowercase
        target_string = target_string.lower()

        # Flag to check if the file was modified
        modified = False

        # Set of elements to be commented out
        elements_to_comment_out = set()

        # Iterate through all elements in the XML tree
        for elem in root.xpath("//*"):
            if elem.text and target_string in elem.text.lower():
                # If element is a child, add parent to the set
                if elem.getparent() is not None:
                    elements_to_comment_out.add(elem.getparent())
                # If element has no children, add element itself to the set
                elif len(elem) == 0:
                    elements_to_comment_out.add(elem)

        # Comment out the elements
        for elem in elements_to_comment_out:
            comment = etree.Comment(etree.tostring(elem, method='xml', encoding='unicode', with_tail=False))
            parent = elem.getparent()
            if parent is not None:
                parent.replace(elem, comment)
                modified = True

        # Save the modified XML back to the file
        if modified:
            tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return True
    except Exception as e:
        return str(e)


def process_files():
    target_string = target_string_entry.get()
    file_paths = filedialog.askopenfilenames(filetypes=[("XML files", "*.xml")])

    # Set progress bar maximum value
    progress_bar["maximum"] = len(file_paths)

    # Process the files sequentially
    results = []
    for file_path in file_paths:
        result = comment_out_tags(file_path, target_string)
        progress_bar.step(1)
        root.update_idletasks()
        time.sleep(0.1)  # Give the GUI some time to render updates
        if result is not True:
            results.append(f"Error processing {file_path}: {result}")
        else:
            results.append(f"Processed {file_path}")

    # Display the results in a messagebox
    messagebox.showinfo("Results", "\n".join(results))


# Create the GUI window
root = tk.Tk()
root.title("XML Helper")

# Set window size
root.geometry("400x200")

# Target string entry
target_string_label = tk.Label(root, text="Target String:")
target_string_label.pack()
target_string_entry = tk.Entry(root)
target_string_entry.pack()

# Process files button
process_files_button = tk.Button(root, text="Select and Process Files", command=process_files)
process_files_button.pack()

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack()

# Run the GUI
root.mainloop()
