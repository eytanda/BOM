#!/usr/bin/python3
"""
author: Eytan Dagry
mail: eytan@silicom.co.il
Update by: Eytan Dagry
update date 04.05.2025


"""

ver = 1.2
BLUE_COLOR = "\033[1;34;40m"
PURPLE_COLOR = "\033[1;35;40m"
YELLOW_COLOR = "\033[1;33;40m"
CYAN_COLOR = "\033[1;36;40m"
RED_COLOR = "\033[1;31;40m"
GREEN_COLOR = "\033[1;32;40m"
ALL_COLORS = [BLUE_COLOR, PURPLE_COLOR, YELLOW_COLOR, CYAN_COLOR, RED_COLOR, GREEN_COLOR]
RESET_STYLE_BLACK_BG = "\033[0;0;40m"
RESET_STYLE = "\033[0;0;0m"



import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import time





def select_file():
    # Create a root window (necessary for Tkinter)
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    time.sleep(0.1)
    print("Opening file dialog...")
    # Open the file dialog and store the selected file path in a variable
    file_path = filedialog.askopenfilename(title="Select a file")
    directory_path = os.path.dirname(file_path)

    # Now, you can use the file_path variable for your purposes
    if file_path:
        print(f"Selected file: {file_path}")
        return file_path , directory_path
    else:
        print("No file selected")
        exit(1)

# Load the CSV file


def main():
    file_path , directory_path = select_file()
    #file_path,  = 'BOM1.csv'  # original file
    df = pd.read_csv(file_path)

    # Initialize a list to keep track of relevant row indices
    relevant_indices = []
    # init indication for empty line
    empty_line_exist = False

    ## delete alll lines that do not have item number and chain in COT
    for i in range(len(df) - 1, -1, -1):
        if pd.isna(df.at[i, 'Item Number']) and 'China' in str(df.at[i, 'Country of Origin (MP)']):
            # df.loc[i, 'Item Description':'Reference Notes'] = pd.NA
            #print(df.loc[i])
            #print(i)
            df.drop(i, inplace=True)
        # Reset the index after dropping rows
        df.reset_index(drop=True, inplace=True)



    # Loop through the DataFrame to find rows 'Country of Origin (MP)' and a non-empty 'Item Number' and lines with empty item number below
    for i in range(len(df) - 1):
        if pd.notna(df.at[i, 'Item Number']): # and 'China' in str(df.at[i, 'Country of Origin (MP)']):
            relevant_indices.append(i)  # Include the current row


            # Add all subsequent rows where 'Item Number' is empty and update them
            j = i + 1
            empty_line_exist = False
            while j < len(df) and pd.isna(df.at[j, 'Item Number']):
                relevant_indices.append(j)
                #df.at[j, 'Item Number'] = last_item_number  # Assign the updated Item Number to empty cells
                j += 1
                empty_line_exist = True
            if empty_line_exist == False:
                relevant_indices.pop()


    #  make a list of the indices to be updated without modifying the DataFrame 
    rows_to_update = []

    for idx in relevant_indices:
        if pd.notna(df.at[int(idx), 'Item Number']):  # Ensure Item Number is not None or NaN
            df.at[int(idx), 'Item Number'] = df.at[int(idx), 'Item Number'] + '-NCN'  # Append '-NCN' to Item Number

        if 'China' in str(df.at[idx, 'Country of Origin (MP)']):
            # Save the rows that need to be copied
            rows_to_update.append(idx)

    # update the rows outside of the loop to avoid shifting
    for idx in rows_to_update:
        # Copy the values from the next row to the current row (above)
        df.loc[idx, 'Manufacture Part Has Redline':'Reference Notes'] = df.loc[idx + 1,
                                                                        'Manufacture Part Has Redline':'Reference Notes']

        # Set the next row (the source) to NaN
        df.loc[idx + 1, 'Manufacture Part Has Redline':'Reference Notes'] = pd.NA
    #delet empty lines
    df = df.dropna(how='all')

    # Save the updated DataFrame to a new CSV file
    x = len(directory_path)
    file_name=(file_path[x + 1:-4])
    output_path = directory_path + '/' + file_name + "-NCN.csv"  # Replace with your desired output path
    #filtered_df.to_csv(output_path, index=False)
    df.to_csv(output_path, index=False)


    print(GREEN_COLOR + f"Filtered data with '-NCN' added to Item Numbers has been saved to {output_path}" + RESET_STYLE)



if __name__ == '__main__':

    print(YELLOW_COLOR + f" Made In China BOM Conversion Utility Ver:{ver}" + RESET_STYLE )
    main()