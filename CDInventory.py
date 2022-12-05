#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Harshita Singh, 2022-Nov-11, Modified File for Assignment 06
# Harshita Singh, 2022-Dec-03, Modified File for Assignment 07
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

import pickle
# -- PROCESSING -- #
class DataProcessor:
    """Processing the data to and from the list of dicts"""
    @staticmethod
    def create_row():
        """Function to create a dictionary row from user input


        Args:
            None

        Returns:
            None.
        """
        
        try:
            intId, strTitle, strArtist = IO.ask_user()
        except ValueError:
            return
        dicRow = {'ID': intId, 'Title': strTitle, 'Artist': strArtist}
        lstTbl.append(dicRow)
        
        
    @staticmethod
    def search_cd_to_delete(cd_to_delete):
        """Function to search for the CD user wants to delete from the list of dicts.
        If the matching CD is found, delete from the list.


        Args:
            CD user wants to delete

        Returns:
            None.
        """
        
        index = -1
        for idx, line in enumerate(lstTbl):
            # if the ley matches with the user key, then delete the data from list of dict
            if cd_to_delete == line['ID']:
                index = idx
                break
        if index != -1:
            lstTbl.pop(index)
        
        
        
    @staticmethod
    def save_inventory_to_file():
        """Function to save the CD inventory from the list of dicts to the file.

        Args:
            CD user wants to save

        Returns:
            None.
        """
        try:
            objFile = open(strFileName, 'wb')
            for row in lstTbl:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                pickle.dump(','.join(lstValues) + '\n', objFile)
            objFile.close()
        except FileNotFoundError as e:
            print("file does not exist!")
            print('Build in error info!')
            print(type(e), e, e.__doc__, sep = '\n')



class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        lstTbl.clear()  # this clears existing data and allows to load data from file
        try:
            with open(file_name, 'rb') as f:
                line = pickle.load(f)
                data = line.strip().split(',')
                dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(dicRow)
        except FileNotFoundError as e:
            print("file does not exist!")
            print('Build in error info!')
            print(type(e), e, e.__doc__, sep = '\n')           
        
            
    @staticmethod
    def write_file(file_name, table):
        
        """Function to wrute data from a list of dictionaries into a file

        Reads the data from 2D table (list of dicts) row by row
        and write a line into the flile

        Args:
            file_name (string): name of file used to write the data into
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            with open(file_name, 'w') as f:
                for row in table:
                    val = ''
                    for item in row.values():
                        val += str(item) + ','
                    val = val[:-1] + '\n'
                f.write(val)
        except FileNotFoundError as e:
            print("file does not exist!")
            print('Build in error info!')
            print(type(e), e, e.__doc__, sep = '\n')         

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        try:
            choice = ' '
            while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        except ValueError as e:
            print('Not a valid option')
            print('Build in error info!')
            print(type(e), e, e.__doc__, sep = '\n')         
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    staticmethod
    def ask_user():
        """Asks user input for ID, CD Title and Artist
        

        Args:
            None

        Returns:
            user inputs(ID, Title and Artist Name).

        """
        try:
            CD_id = int(input('Enter ID: '))
        except ValueError as e:
            print('\n\n\n\t\t\t\tNot a valid integer!\n\n\n\n\n') 
            raise e
            
        Title = input('What is the CD\'s title? ').strip()
        Artist = input('What is the Artist\'s name? ').strip()
            
        return CD_id, Title, Artist
        
        
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        #IO.ask_user()
        # 3.3.2 Add item to the table
        DataProcessor.create_row()
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('Not a valid integer!')
            print('Build in error info!')
            print(type(e), e, e.__doc__, sep = '\n')   
        # 3.5.2 search thru table and delete CD
        DataProcessor().search_cd_to_delete(intIDDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            DataProcessor().save_inventory_to_file()
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




