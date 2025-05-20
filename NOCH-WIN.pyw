#!/usr/bin/python3
"""
author: Eytan Dagry
mail: eytan@silicom.co.il
Update by: Eytan Dagry
update date 04.05.2025
"""

ver = 1.72

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
        relevant_sub_indices = []
        relevant_main_line_indices = []
        single_line_china = 0

        sons_and_main_with_china = 0
        # Identify relevant indices of lines with sons that includes Made in chain in the main or in the sons
        for i in range(len(df)):
            empty_line_exist = False
            num_of_empty_lines = 0
            num_with_no_china = 0
            num_with_china = 0

            at_list_one_china = False
            if pd.notna(df.at[i, 'Item Number']):
                if 'China' in str(df.at[i, 'Country of Origin (MP)']):
                    at_list_one_china = True
                relevant_main_line_indices.append(i)
                j = i + 1

                while j < (len(df)) and pd.isna(df.at[j, 'Item Number']):
                    relevant_sub_indices.append(j)
                    empty_line_exist = True
                    num_of_empty_lines += 1


                    if 'China' not in str(df.at[j, 'Country of Origin (MP)']):
                        num_with_no_china += 1
                        #print("num_with_no_china =", num_with_no_china)
                    else:
                        at_list_one_china = True
                        num_with_china += 1
                    j += 1


                if not empty_line_exist:
                #print(i)
                    if at_list_one_china: single_line_china += 1
                    relevant_main_line_indices.pop()




                elif not at_list_one_china:
                    if len(relevant_main_line_indices) >= 1:
                        relevant_main_line_indices.pop()

                    for empty_line in range (num_of_empty_lines):
                        relevant_sub_indices.pop()

                # check if main and sons are all with Made in China
                elif num_with_china == num_of_empty_lines and 'China' in str(df.at[i, 'Country of Origin (MP)']):
                    sons_and_main_with_china += 1
                    #print(sons_and_main_with_china)
                    relevant_main_line_indices.pop()
                    for p in range (num_with_china):
                        relevant_sub_indices.pop()

        #print("****************************************************")
        #print("relevant_sub_indices=", relevant_sub_indices)
        #print("relevant_main_line_indices=", relevant_main_line_indices )
        self.log(f"Number of PN that were modified: {len(relevant_main_line_indices)}", "magenta")
        self.log(f"Number of sons' lines (with made in China) that were deleted: {len(relevant_sub_indices)}", "magenta")
        self.log(f"Number of main line and sons lines that are all with Made in China: {sons_and_main_with_china}", "red")
        self.log(f"Number of main line (single with no sons) with Made in China: {single_line_china}", "red")




        # update the main lines (relevant_main_line_indices)  with -NCN
        for idx in relevant_main_line_indices:
            if len(df.at[int(idx), 'Item Number']) > 18:

                df.at[int(idx), 'Item Number'] = df.at[int(idx), 'Item Number'] + '-NCN-LONG'
            else:
                df.at[int(idx), 'Item Number'] = df.at[int(idx), 'Item Number'] + '-NCN'

        # Clean up lines without Item Number but with 'China' in relevant_sub_indices
        for idx in sorted(relevant_sub_indices, reverse=True):
            if pd.isna(df.at[idx, 'Item Number']) and 'China' in str(df.at[idx, 'Country of Origin (MP)']):
                df.drop(idx, inplace=True)
        df = df.reset_index(drop=True)

        # Check if main line includes China and copy info from bottom line
        for idx in range(len(df)-1):
            if '-NCN' in str(df.at[idx, 'Item Number']) and 'China' in str(df.at[idx, 'Country of Origin (MP)']):
                df.loc[idx, 'Manufacture Part Has Redline':'Reference Notes'] = df.loc[idx + 1,
                                                                                'Manufacture Part Has Redline':'Reference Notes']
                df.loc[idx + 1, 'Manufacture Part Has Redline':'Reference Notes'] = pd.NA
                #
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