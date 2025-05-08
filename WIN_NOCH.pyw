#!/usr/bin/python3
"""
author: Eytan Dagry
mail: eytan@silicom.co.il
Update by: Eytan Dagry
update date 04.05.2025
"""

ver = 1.31

import tkinter as tk
from tkinter import filedialog, scrolledtext
import os


class BOMConverterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Made In China BOM Conversion Utility Ver:{ver}")

        self.log_window = scrolledtext.ScrolledText(self.root, width=100, height=30)
        self.log_window.pack(padx=10, pady=10)

        self.run_button = tk.Button(self.root, text="Run Conversion", command=self.main)
        self.run_button.pack(pady=10)

        self.log("Made In China BOM Conversion Utility Ver:" + str(ver), "PURPLE")

    def log(self, message, color="green"):
        # Define a tag with color if not already defined
        if not color in self.log_window.tag_names():
            self.log_window.tag_configure(color, foreground=color)

        # Insert the message with the specified color
        self.log_window.insert(tk.END, f"{message}\n", color)
        self.log_window.see(tk.END)
        self.root.update_idletasks()

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        directory_path = os.path.dirname(file_path)

        if file_path:
            self.log(f"Selected file: {file_path}", "blue")
            return file_path, directory_path
        else:
            self.log("No file selected. Exiting...", "red")
            exit(1)

    def main(self):
        import pandas as pd

        file_path, directory_path = self.select_file()
        df = pd.read_csv(file_path)
        relevant_indices = []

        # Clean up lines without Item Number but with 'China' in Origin
        for i in range(len(df) - 1, -1, -1):  # start from the end to the start to overcome delete line issue
            if pd.isna(df.at[i, 'Item Number']) and 'China' in str(df.at[i, 'Country of Origin (MP)']):
                df.drop(i, inplace=True)
            df.reset_index(drop=True, inplace=True)

        # Identify relevant indices of lines with suns
        for i in range(len(df) - 1):
            if pd.notna(df.at[i, 'Item Number']):
                relevant_indices.append(i)
                j = i + 1
                empty_line_exist = False
                while j < len(df) and pd.isna(df.at[j, 'Item Number']):
                    relevant_indices.append(j)
                    j += 1
                    empty_line_exist = True
                if not empty_line_exist:
                    relevant_indices.pop()
        print(relevant_indices)



        rows_to_update = []

        for idx in relevant_indices:
            if pd.notna(df.at[int(idx), 'Item Number']):
                df.at[int(idx), 'Item Number'] = df.at[int(idx), 'Item Number'] + '-NCN'
            if 'China' in str(df.at[idx, 'Country of Origin (MP)']):
                rows_to_update.append(idx)

        # Update rows
        for idx in rows_to_update:
            df.loc[idx, 'Manufacture Part Has Redline':'Reference Notes'] = df.loc[idx + 1, 'Manufacture Part Has Redline':'Reference Notes']
            df.loc[idx + 1, 'Manufacture Part Has Redline':'Reference Notes'] = pd.NA

        # Remove fully empty rows
        df = df.dropna(how='all')

        # Save the file
        x = len(directory_path)
        file_name = file_path[x + 1:-4]
        output_path = directory_path + '/' + file_name + "-NCN.csv"
        df.to_csv(output_path, index=False)

        self.log(f"Filtered data with '-NCN' added to Item Numbers has been saved to {output_path}", "green")

if __name__ == '__main__':
    app = BOMConverterApp()
    app.root.mainloop()