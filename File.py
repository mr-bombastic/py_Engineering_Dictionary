# Author: Spyros Leonard Lian Krinis
# Last updated: 29-8-2019
# Version: 2.0
# This class is used for various functions that pertain to the files of JAMES
# This includes creating files, manipulating the location of files, deleting files, adding data to files,
#       getting data from files, and converting one data format to another.


import os
import shutil


# ===========================================================
# These functions are used to check if something exists/is a type of value
# ===========================================================
# used to check if a given value is a float
# True = value is a float, False = value is not a float
def is_it_a_float(f_value):
    try:                # if the value is a float
        float(f_value)
        return True
    except ValueError:  # if its not a float
        return False


# checks if a given value is in a given list
# True = Value is in the list, False = Value is not in the list
def is_value_in_list(value_list, value):
    # looks for the value in the list
    if value in value_list:     # if the value is in the list
        return True
    else:                       # if it is not
        return False


# used to check if a file with a specific name exists
# True = file exists, False = files does not exist
def does_file_exist(s_name):
    # checks to see if file exists
    if os.path.exists(str(s_name)):     # if it does exist
        return True
    else:                               # if it doesn't exist
        return False


# ===========================================================
# These functions are used to copy/delete files
# ===========================================================
# used to move and rename files. The file can only start in the root directory of the program
# also includes logic to check if a file of the same name already exists. If it does the version number will change
# A file name string = successfully moved, '' = File did not exist
def move_file(s_initial_name, s_final_name, s_final_folder):
    # check to see if the file to be changed exists
    if does_file_exist(s_initial_name):     # when it exists
        i_count = 1  # sets the value of i_count to be used to make sure no overwriting of files occurs
        # create the final file directory name including the extension name
        s_final = os.getcwd() + '\\' + str(s_final_folder) + '\\' + str(s_final_name) + ' Ver 1.txt'

        # loop to check the final destination for files with the same name
        while True:
            if does_file_exist(s_final):  # if the file does exist in the final directory
                i_count += 1  # increment count

                # alter file name to increment the version number
                s_final = s_final.replace(' Ver ' + str(i_count - 1) + '.txt', ' Ver ' + str(i_count) + '.txt')
            else:  # if it doesn't exist then the name is fine and it can be moved/renamed
                os.rename(s_initial_name, s_final)                          # actually rename and move the file
                return str(s_final_name) + ' Ver ' + str(i_count) + '.txt'  # return the file name
    else:                                       # if the file to be changed doesn't exist
        print('\n===File did not exist.===\n')  # inform about non-existent file [help with debugging]
        return ''                               # return nothing as a file was not named


# used to copy of a file (s_old) to a new location (s_new). Checks if the initial file exists to prevent errors
# mainly used when copying the various versions of mdat and polarx
# =========================this function WILL OVERWRITE ANY FILE IN THE TARGET DIRECTORY=========================
def copy_file(s_old, s_new):
    if does_file_exist(s_old):                  # if the file exists
        shutil.copy(str(s_old), str(s_new))     # copy the file to new location


# used to delete individual files. Checks if the file exists to prevent errors
def delete_file(s_name):
    if does_file_exist(str(s_name)):    # if the file exists
        os.remove(str(s_name))          # delete the file


# deletes all data files from previous runs (except polar). Done to prevent mses from getting confused with old files
def clear_files():
    # delete mdat files
    delete_file('mdat')
    delete_file('mdat_acp')
    delete_file('mdat_re')

    # delete polarx files
    delete_file('polarx')
    delete_file('polarx_acp')
    delete_file('polarx_re')

    delete_file('mses')     # delete mses config file
    delete_file('spec')     # delete spec config file


# an inclusive file that will rename and move the finished polar file
# A file name string = successfully moved, '' = File did not exist
def polar_rename_and_move(f_amin, f_amax, f_remin, f_remax, f_mamin, f_mamax, i_ncrit, f_mcrit, f_mucon):
    # divide the Reynolds number values by 1e6 for formatting purposes
    f_remax /= 1e6
    f_remin /= 1e6

    # creates the new name for the polar file
    s_newname = 'polar for a(' + str(f_amin) + ' to ' + str(f_amax) + ') Re(' + str(f_remin) + 'e6 to ' + str(f_remax) \
                + 'e6) Ma(' + str(f_mamin) + ' to ' + str(f_mamax) + ') n(' + str(i_ncrit) + ') m(' + str(f_mcrit) \
                + ') mu(' + str(f_mucon) + ')'

    s_return = move_file('polar', s_newname, 'Completed Tests')    # move the polar file

    # makes remembering what mses settings were used easier
    msesname = s_newname.replace('polar', 'mses')   # creates name for mses configuration file
    move_file('mses', msesname, 'Completed Tests')  # move the mses file

    return s_return  # returns the new name in case it is needed


# ===========================================================
# These functions are used to create files
# ===========================================================
# Creates a polar file that includes information about major and minor variables used for the calculation
# This will be filled with JAMES/MSES format polar coordinates
def create_polar(f_alow, f_ahigh, f_relow, f_rehigh, f_malow, f_mahigh, i_ncrit, f_mcrit, f_mucon):
    polarfile = open('polar', 'w')  # over write the polar file
    
    # write what the range of major values used were
    polarfile.write('Major values used were: alpha = ' + str(f_alow) + ' to ' + str(f_ahigh) + ', Reynolds = '
                    + str(f_relow / 1e6) + 'e6 to ' + str(f_rehigh / 1e6) + 'e6, Mach = ' + str(f_malow) + ' to '
                    + str(f_mahigh) + '\n')
    # write what the minor values used were
    polarfile.write('Minor values used were: ncrit = ' + str(i_ncrit) + ', mcrit = ' + str(f_mcrit) +
                    ', mucon = ' + str(f_mucon) + '\n')
    # write the name of the airfoil tested
    polarfile.write('Airfoil tested: ' + get_blade_name() + '\n')
    # write information for the columns
    polarfile.write('\n   alpha    CL        CD       CM       CDw       CDv       CDp      Mach      Re      '
                    'Top_Xtr  Bot_Xtr\n  ------ -------- --------- -------- --------- --------- --------- ------- '
                    '---------- -------- --------\n')
    
    polarfile.close()               # close the file
    print('Polar file created.')    # inform user


# creates the mses file in a format MSES will understand
def create_mses(f_mach, f_re, f_alpha, f_sweep, i_ncrit, f_mcrit, f_mucon):
    mses = open('mses', 'w')  # create the mses file itself

    # write necessary global variables
    mses.write('3  4  5  7 ')
    if f_sweep == 15:
        mses.write(' 15\n')
    elif f_sweep == 17:
        mses.write(' 10\n')
    else:
        mses.write('\n')

    # write necessary global constraints
    mses.write('3  4  5  7 ')
    if f_sweep == 15:
        mses.write(' 15\n')
    elif f_sweep == 17:
        mses.write(' 17\n')
    else:
        mses.write('\n')

    # write other parameters/variables
    mses.write(str(f_mach) + '  0.0  ' + str(f_alpha) + '\t\t\t| MACHin  CLIFin  ALFAin\n')
    mses.write('3  2\t\t\t\t| ISMOM  IFFBC\n')
    mses.write(str(f_re) + '  ' + str(i_ncrit) + '\t\t\t| REYNin ACRIT\n')
    mses.write('1.0  1.0\t\t\t| XTR1 XTR2\n')
    mses.write(str(f_mcrit) + '  ' + str(f_mucon) + '\t\t\t| MCRIT  MUCON')

    mses.close()  # close the file

