# process-visual
Python-based graphical tool designed for visualizing and managing progress ranges in large numeric intervals

Description
proc.visual.py is a Python-based graphical tool designed for visualizing and managing progress ranges in large numeric intervals. The application allows users to input custom ranges and processes, calculate covered and free ranges, and visually display progress on a canvas.

Key features include:

Support for extremely large numbers (up to 316 digits).
Add and delete multiple process ranges dynamically.
Automatic recalculation and visualization upon each update.
A clear distinction between occupied and free ranges.
Support for HEX and DEC number systems.
Copyable list of free ranges for further use.
This tool is particularly useful for tasks involving huge numeric datasets, such as cryptographic calculations or big integer simulations.

Screenshots

![image](https://github.com/user-attachments/assets/98e83ba8-d486-469a-88c3-71ed27637fc7)
![image](https://github.com/user-attachments/assets/15d8c7bf-cc8b-4971-ae5a-44c244f4e4ab)



Usage
Range Input: Specify the start and end of the range you want to analyze.
Process Input: Add multiple processes (sub-ranges) dynamically using the "Add Process" button, or delete unwanted rows with "Del Process."
Calculation: Click "Calculate" to visualize the covered ranges and list the free ranges.
Free Ranges: View and copy free ranges for further use.
Switch Number Systems: Toggle between HEX and DEC for input and output.
Requirements
Python 3.10 or newer
Libraries listed in the requirements.txt

How to Run
Clone the repository:

`git clone https://github.com/franklin-lol/process_-visual.git
cd process_-visual.py`

Install dependencies:

`pip install -r requirements.txt`

Run the script:

`python process_-visual.py`

