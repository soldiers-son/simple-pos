# simple-pos

Author: soldiers-son

POS.py Version: 1.0

Python: 3.11+

Platform: Windows / Linux / Mac

Dependencies: tkinter, customtkinter, sqlite3, sys, json, webbrowser, datetime, os

----------------------------------------------------
0. Acknowledgments
----------------------------------------------------
Thank you to the open source community, whose 
work makes this project possible.

----------------------------------------------------
1. Introduction
----------------------------------------------------
This is simple lightweight Point Of Sale application designed for small business owners.

<img src="demo_main.png" />

----------------------------------------------------
2. Features
----------------------------------------------------

- Toolbar menu with:
  • Sales & Inv → Easily view sales and input items into current stock 
  • Help → Help / About / Source Code
  • Source Code
  
- Clean Tkinter-based interface.

----------------------------------------------------
3. Requirements
----------------------------------------------------
- Python 3.11 or higher
- customtkinter

----------------------------------------------------
4. Installation
----------------------------------------------------
1. Clone or download this repository.
2. Place the project folder on your desktop or 
   desired directory.
3. Install Python and required dependencies.
4. Run the application:

   Windows:
   > python POS.py

   Linux/Mac:
   $ python3 POS.py

----------------------------------------------------
5. Dependencies
----------------------------------------------------
Install required packages via pip:

   pip install customtkinter

----------------------------------------------------
6. Usage
----------------------------------------------------
- Run `POS.py` to start the application.
- Click "Inv" in menubar to input current stock.
  <img src="demo_inv.png" />
- Select the desired item on the main menu you wish to add to order, enter quantity, and press submit.
- View the current order by clickling the "Cart".
- Once the order is finished, press "Finalize" to confirm and complete the order.
- View sales data by selecting "Sales' in menubar.
  <img src="demo_sales.png" />
  
----------------------------------------------------
7. Future Goals
----------------------------------------------------
Planned expansions include:

- Extended data visualization
- Search & Filter data
- Stripe payment integration
- Web Api
- Reciept options and processing (email, text, print)
- Better cart management
- Edit currently listed in stock items
- Ability to save current order for later retrieval
- Kiosk for customer display

----------------------------------------------------
8. Contributing
----------------------------------------------------
Suggestions and improvements are welcome. 
Fork the repo, make your changes, and submit a PR.

----------------------------------------------------
9. License
----------------------------------------------------
This project is open source under the MIT License.

----------------------------------------------------
10. Contact
----------------------------------------------------
Author: soldiers-son

GitHub: (https://github.com/soldiers-son?tab=repositories)

Email: (soldiers.son1618@gmail.com)
