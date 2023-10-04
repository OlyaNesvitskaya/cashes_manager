
## Manual Build

👉 Download the code

$ git clone https://github.com/OlyaNesvitskaya/cashes_manager.git  
$ cd cashes_manager

👉 Install modules via VENV

$ virtualenv venv  
$ source venv/bin/activate  
$ pip install -r requirements.txt  

👉 Set Up Database

$ python manage.py makemigrations  
$ python manage.py migrate  

👉 Start the app

$ python manage.py runserver  
At this point, the app runs at http://127.0.0.1:8000/manager.

## Description

When the main page loads, a list of cashbox profiles will be displayed; the table is generated
by re-reading the physical directory profiles (path 'checkbox.kasa.manager\profiles'). 
Each folder name corresponds to the name field, the path field is filled in with the full path to the profile. 
Getting the value for the port field - open the config.json file (it is stored in each profile folder).
The remaining fields are optional and filled in by user. If the profile is not in the database, add it,
if it is mysite\in the database but not in the catalog, delete it.

Pressing on profile name we can direct to edit profile. Fields is available to edit: name, port, enabled, note.

Each cashbox prolfile has button *On/Off*. Pressing on this button we can run or stop .exe file 
(it is stored in coresponding profile folder). 
File .exe runs in new process and process data writes in process table.

There is a search field on the main page.Search is carried out by partially coincidence by such fields: port, enabled, name and serial.

There is an opportunity to sort in ascending order by such fields: port, enabled, shift, name and serial.
