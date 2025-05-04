#!/usr/bin/python3
"""
author: Eytan Dagry
mail: eytan@silicom.co.il
Update by: Eytan Dagry
update date 04.05.2025
ver:1.1

"""


import pandas as pd
#from numpy.matlib import empty

# Load the CSV file
file_path = 'BOM1.csv'  # original file
df = pd.read_csv(file_path)

# Initialize a list to keep track of relevant row indices
relevant_indices = []
# init indication for empty line
empty_line_exist = False

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

#print("relevant_indices=", relevant_indices)

for idx in relevant_indices:
    #print("idx=", idx)
    #print(type(idx))
    if pd.notna(df.at[int(idx), 'Item Number']):  # Ensure Item Number is not None or NaN
        df.at[int(idx), 'Item Number'] = df.at[int(idx), 'Item Number'] + '-NCN'  # Append '-NCN' to Item Number
    if 'China' in str(df.at[idx, 'Country of Origin (MP)']):
        df.loc[idx, 'Item Description':'Reference Notes'] = pd.NA

for i in range(len(df) - 1):
    if pd.isna(df.at[i, 'Item Number']) and 'China' in str(df.at[i, 'Country of Origin (MP)']):
        df.loc[i, 'Item Description':'Reference Notes'] = pd.NA



# Save the updated DataFrame to a new CSV file
output_path = 'filtered_BOM_updated_with_ncn.csv'  # Replace with your desired output path
#filtered_df.to_csv(output_path, index=False)
df.to_csv(output_path, index=False)


print(f"Filtered data with '-ncn' added to Item Numbers has been saved to {output_path}")
