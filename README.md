# Made In China BOM Conversion Utility 

The Utility convert the BOM based on the below rules 


Explanation of file format: lines that ITEM NUMBER exist: the first vendor listed in the same line. In case that ITEM NUMBER cell is empty it means that this line related to the ITEM NUMBER above, it is another vendor that listed. there could be one or more vendors for each ITEM NUMBER, column COUNTRY OF ORIGION (MP) list where the component that defined in ITEM NUMBER produced.

1.	Copy the original CSV file, name it A8 + ”-NCN”.CSV
2.	For ITEM NUMBER that list vendors that their COUNTRY OF ORIGION (MP) is not “China” or not include “China”- skip these ITEM NUMBERs.
3.	For ITEM NUMBER that list only one vendor that its COUNTRY OF ORIGION (MP) is “China” or include “China”- skip these ITEM NUMBERs.
4.	For ITEM NUMBER that list vendors that their COUNTRY OF ORIGION (MP) is “China” or include “China” and have one or more vendors - need to:
a.	If ITEM NUMBER is not null- delete columns I- AZ.
b.	If ITEM NUMBER is empty, remove the lines (vendors) that has “China” or include “China”. Delete the entire line.
c.	Repeat 4.a to 4.b till the ITEM NUMBER is not Null.
d.	If ITEM NUMBER is not Null- go to 2.
e.	Rename the original ITEM NUMBER to be “ITEM NUMBER-NCN”, adding “-NCN” suffix for such ITEM NUMBERs.
5.	If ITEM NUMBER and the ITEM NUMBER below it are both Null- you reached to end of file.