from tkinter import *
import tkinter.font as tkfont
from tkinter import messagebox
from logic import *
from constant import *
from variable import *
from equation import *
from theory import *
from method import *

# colors and other variables
color_dark = "#2b2b2b"  # background color
color_mid = "#383838"   # button background color
color_light = "#404040"  # frame colors
accent_dark = "#323232"  # accent color dark
accent_light = '#949596'  # accent color light
text_color = "#eaeaea"  # color for text

relief_style = 'flat'  # type of relief (flat, groove, raised, ridge, solid, sunken)

spacing_out_x = 10
spacing_out_y = 5
spacing_in = 2
fontsize = 11
left_side_thickness = 400
right_side_thickness = 150

# stuff that transcends various dimensions
previously_altered_widgets = []
step_num = 1
item_to_edit = ""

# test variables ======================================================================================================
l_logic = Logic("Logic boi", "some information about logic stuff that is super long and designed to break the ui", "")
v_test = Variable("variable boi", "v", None, "rad", "Variable test description.")
c_test = Constant("constant boi", "c", 21.69, "m/s", "Constant test description.")
e_test = Equation("equation boi", "Equation description testing.", "sin(" + str(v_test.get_symbol()) + "+" +
                  str(c_test.get_symbol()) + "^2)", [v_test, c_test])
t_test = Theory("theory boi", "Theory description test", e_test)
m_test = Method("method boi", "method test description", [l_logic, v_test, c_test, e_test, t_test])

test_items = [l_logic, v_test, c_test, e_test, t_test, m_test]
# test variables ======================================================================================================

search_results = []  # create an array of the results

# main window stuff
window = Tk()  # creates the window
window.title("My Engineering Glossary")
window.state('normal')  # "zoomed" for full screen
window.configure(background=color_dark)

# set default font size
default_font = tkfont.Font(size=fontsize)
window.option_add("*Font", default_font)

# measure the length of m to get an idea of the number of pixels a character is
m_len = default_font.measure("m")

# set these items default font style and size
window.option_add("*Labelframe.Font", "Arial "+str(fontsize)+" bold italic")

# sets the default colors for various activities
window.tk_setPalette(background=color_light, foreground=text_color, activeBackground=color_dark,
                     activeForeground=text_color, selectColor=color_dark)

# set these items default background to color_mid
window.option_add("*Button.Background", color_mid)
window.option_add("*Radiobutton.Background", color_mid)
window.option_add("*Canvas.Background", color_mid)
window.option_add("*Entry.Background", color_mid)

window.option_add("*Label.Anchor", "w")     # default label anchor

window.option_add("*relief", 'flat')
window.option_add("*Button.relief", 'ridge')
window.option_add("*highlightthickness", 1)
window.option_add("*Canvas.highlightthickness", 0)


item_type_to_add_or_edit = StringVar()  # this is for adding/editing items. Let it be


# this stuff is for sorting out the resizing of the right column and lower row
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(1, weight=1)


# items for the checkboxes, will save 0 or 1 if it has not or has been checked
search_variables = IntVar(value=1)
search_constants = IntVar(value=1)
search_equations = IntVar(value=1)
search_theories = IntVar(value=1)
search_logic = IntVar(value=1)
search_methods = IntVar(value=1)
search_names = IntVar(value=1)
search_description = IntVar(value=1)
search_symbol = IntVar(value=1)
search_value = IntVar(value=1)
search_units = IntVar(value=1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print every saved item that is selected in the checkboxes
def print_all():
    destroy_results()  # will delete all the old search results

    search_results.clear()  # removes all items from search results

    if search_variables.get() == 1:  # when the user whats to search through variables
        search_results.extend(string_to_item(get_file_lines("Dictionary/variables.txt"), "Variable"))
    if search_constants.get() == 1:  # when the user whats to search through constants
        search_results.extend(string_to_item(get_file_lines("Dictionary/constants.txt"), "Constant"))
    if search_equations.get() == 1:  # when the user whats to search through equations
        search_results.extend(string_to_item(get_file_lines("Dictionary/equations.txt"), "Equation"))
    if search_theories.get() == 1:  # when the user whats to search through theories
        search_results.extend(string_to_item(get_file_lines("Dictionary/theories.txt"), "Theory"))
    if search_logic.get() == 1:  # when the user whats to search through logic
        search_results.extend(string_to_item(get_file_lines("Dictionary/logic.txt"), "Logic"))
    if search_methods.get() == 1:  # when the user whats to search through methods
        search_results.extend(string_to_item(get_file_lines("Dictionary/methods.txt"), "Method"))

    print_results()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Will search though the database and fill the array to ultimately have it printed
def search():
    destroy_results()  # will delete all the old search results

    if txt_search.get() != '':
        search_results.clear()      # removes all items from search results

        if search_variables.get() == 1:         # when the user whats to search through variables
            search_results.extend(string_to_item(get_file_lines("Dictionary/variables.txt"), "Variable"))
        if search_constants.get() == 1:         # when the user whats to search through constants
            search_results.extend(string_to_item(get_file_lines("Dictionary/constants.txt"), "Constant"))
        if search_equations.get() == 1:         # when the user whats to search through equations
            search_results.extend(string_to_item(get_file_lines("Dictionary/equations.txt"), "Equation"))
        if search_theories.get() == 1:          # when the user whats to search through theories
            search_results.extend(string_to_item(get_file_lines("Dictionary/theories.txt"), "Theory"))
        if search_logic.get() == 1:             # when the user whats to search through logic
            search_results.extend(string_to_item(get_file_lines("Dictionary/logic.txt"), "Logic"))
        if search_methods.get() == 1:           # when the user whats to search through methods
            search_results.extend(string_to_item(get_file_lines("Dictionary/methods.txt"), "Method"))

        search_in_list(txt_search.get(), search_results)

        # check to see if there are any results
        if search_results:
            print_results()
        else:   # if there are not results let the user know there was nothing found
            Label(frm_results_inner, text="No results fit your search criteria.\nPlease try different criteria.").grid()


    # save_items(search_results)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# will use the given text to search through the search_results list and will weed out anything that doesn't match
def search_in_list(search_text, list_to_search):
    i = 0
    while i < len(list_to_search):
        remove = 0
        remove_value = 0

        # when the user whats to search through names
        if search_names.get() == 1:
            # if the users text is nowhere to be found. Just leave it be if its somewhere in there
            if search_text not in list_to_search[i].get_name():
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # when the user whats to search through descriptions
        if search_description.get() == 1:
            # if the users text is nowhere to be found. Just leave it be if its somewhere in there
            if search_text not in list_to_search[i].get_description():
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # checks to make sure one can search within these categories by checking to see what type of item it is
        if get_item_type(list_to_search[i]) == "Variable" or get_item_type(list_to_search[i]) == "Constant":
            # when the user whats to search through symbols
            if search_symbol.get() == 1:
                # if the users text is nowhere to be found. Just leave it be if its somewhere in there
                if search_text not in list_to_search[i].get_symbol():
                    remove += 1
                remove_value += 1  # incremented to understand the number of parameters that will be considered

            # when the user whats to search through values
            if search_value.get() == 1:
                # if the users text is nowhere to be found. Just leave it be if its somewhere in there
                if search_text not in list_to_search[i].get_value():
                    remove += 1
                remove_value += 1  # incremented to understand the number of parameters that will be considered

            # when the user whats to search through units
            if search_units.get() == 1:
                # if the users text is nowhere to be found. Just leave it be if its somewhere in there
                if search_text not in list_to_search[i].get_units():
                    remove += 1
                remove_value += 1  # incremented to understand the number of parameters that will be considered

        # when searching though an equation one must also look into the variables/constants within
        elif get_item_type(list_to_search[i]) == "Equation":

            # get the list of variables/constants and search though them and save the result
            equ_search_list = search_in_list(search_text, list_to_search[i].get_all_variables())

            # if there is nothing in the resulting list then nothing relevant was found
            if len(equ_search_list) == 0:
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # when searching though a method one must also look into the steps within
        elif get_item_type(list_to_search[i]) == "Method":

            # get the list of steps and search though them and save the result
            equ_search_list = search_in_list(search_text, list_to_search[i].get_steps())

            # if there is nothing in the resulting list then nothing relevant was found
            if len(equ_search_list) == 0:
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # checks to see if a search result should be removed
        if remove == remove_value:  # if the item has no relevance to the searched text and limiters
            del list_to_search[i]
        else:                       # if it should stay
            i += 1

    return list_to_search


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# destroys all previous search results to allow new ones to be printed. also deletes stored widgets
def destroy_results():
    # destroys all widgets in frame
    for widget in frm_results_inner.winfo_children():
        widget.destroy()

    # required since the widgets in here no longer exist
    global previously_altered_widgets
    previously_altered_widgets = ""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# called when a search result is clicked to get the widget's row. From there display_info can display correct item
def callback_get_widget_row(event):
    global previously_altered_widgets   # required for the bit where this variable needs to be set to this

    caller = event.widget           # get the widget that corresponds to the event
    r = caller.grid_info()['row']   # get the row of the widget

    # if something was clicked before this will reset the colors so its not highlighted
    if previously_altered_widgets != "":
        for widget in previously_altered_widgets:
            widget.configure(activebackground=color_mid, selectcolor=color_mid)

    # saves an array of all the widgets in the row
    widgets_to_alter = frm_results_inner.grid_slaves(row=r)
    for widget in widgets_to_alter:
        widget.configure(activebackground=color_dark, selectcolor=color_dark)   # changes widget color to highlight

    previously_altered_widgets = widgets_to_alter   # saves array of widgets for if statement seen above
    display_info(r)   # display item corresponding to clicked row


# ========================= Basically done, just need to make it expand horizontally =========================
# will print the results into the results box
def print_results():
    r = 0  # used to increment rows to allow for a list to be displayed

    # loop that will print every result into radiobuttons that can be pressed to select item
    for result in search_results:
        radb_name = Radiobutton(frm_results_inner, text=result.get_name(), activebackground=color_mid,
                                activeforeground=text_color, borderwidth=0, selectcolor=color_mid, indicatoron=False)
        radb_name.bind("<Button-1>", callback_get_widget_row)
        radb_name.grid(sticky="n, s, e, w", row=r, column=0)

        # will set the specific formatting based on the item type
        if isinstance(result, Variable):  # when displaying info about a variable
            radb_sym = Radiobutton(frm_results_inner, text=str(result.get_symbol()), activebackground=color_mid,
                                   activeforeground=text_color, borderwidth=0, selectcolor=color_mid, indicatoron=False)
            radb_sym.bind("<Button-1>", callback_get_widget_row)
            radb_sym.grid(sticky="n, s, e, w", row=r, column=1)

            radb_unit = Radiobutton(frm_results_inner, text=str(result.get_units()), activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_unit.bind("<Button-1>", callback_get_widget_row)
            radb_unit.grid(sticky="n, s, e, w", row=r, column=2, columnspan=2)

            radb_type = Radiobutton(frm_results_inner, text="Variable", activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_type.bind("<Button-1>", callback_get_widget_row)
            radb_type.grid(sticky="n, s, e, w", row=r, column=4)

        elif isinstance(result, Constant):  # when displaying info about a constant
            radb_sym = Radiobutton(frm_results_inner, text=str(result.get_symbol()), activebackground=color_mid,
                                   activeforeground=text_color, borderwidth=0, selectcolor=color_mid, indicatoron=False)
            radb_sym.bind("<Button-1>", callback_get_widget_row)
            radb_sym.grid(sticky="n, s, e, w", row=r, column=1)

            radb_val = Radiobutton(frm_results_inner, text=str(result.get_value()), activebackground=color_mid,
                                   activeforeground=text_color, borderwidth=0, selectcolor=color_mid, indicatoron=False)
            radb_val.bind("<Button-1>", callback_get_widget_row)
            radb_val.grid(sticky="n, s, e, w", row=r, column=2)

            radb_unit = Radiobutton(frm_results_inner, text=str(result.get_units()), activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_unit.bind("<Button-1>", callback_get_widget_row)
            radb_unit.grid(sticky="n, s, e, w", row=r, column=3)

            radb_type = Radiobutton(frm_results_inner, text="Constant", activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_type.bind("<Button-1>", callback_get_widget_row)
            radb_type.grid(sticky="n, s, e, w", row=r, column=4)

        elif isinstance(result, Equation):  # when displaying info about a equation
            radb_equ = Radiobutton(frm_results_inner, text=str(result.get_equation_normal()),
                                   activebackground=color_mid, activeforeground=text_color, borderwidth=0,
                                   selectcolor=color_mid, indicatoron=False)
            radb_equ.bind("<Button-1>", callback_get_widget_row)
            radb_equ.grid(sticky="n, s, e, w", row=r, column=1, columnspan=3)

            radb_type = Radiobutton(frm_results_inner, text="Equation", activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_type.bind("<Button-1>", callback_get_widget_row)
            radb_type.grid(sticky="n, s, e, w", row=r, column=4)

        elif isinstance(result, Theory):  # when displaying info about a theory
            radb_theory = Radiobutton(frm_results_inner, text="Not implemented", activebackground=color_mid,
                                      activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                      indicatoron=False)
            radb_theory.bind("<Button-1>", callback_get_widget_row)
            radb_theory.grid(sticky="n, s, e, w", row=r, column=1, columnspan=3)

            radb_type = Radiobutton(frm_results_inner, text="Theory", activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_type.bind("<Button-1>", callback_get_widget_row)
            radb_type.grid(sticky="n, s, e, w", row=r, column=4)

        elif isinstance(result, Method):  # when displaying info about a method
            radb_descr = Radiobutton(frm_results_inner, text="Number of steps:", activebackground=color_mid,
                                     activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                     indicatoron=False)
            radb_descr.bind("<Button-1>", callback_get_widget_row)
            radb_descr.grid(sticky="n, s, e, w", row=r, column=1, columnspan=2)

            radb_num_step = Radiobutton(frm_results_inner, text=str(result.get_num_steps()), activebackground=color_mid,
                                        activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                        indicatoron=False)
            radb_num_step.bind("<Button-1>", callback_get_widget_row)
            radb_num_step.grid(sticky="n, s, e, w", row=r, column=3)

            radb_type = Radiobutton(frm_results_inner, text="Method", activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_type.bind("<Button-1>", callback_get_widget_row)
            radb_type.grid(sticky="n, s, e, w", row=r, column=4)

        elif isinstance(result, Logic):  # when displaying logic info
            radb_log = Radiobutton(frm_results_inner, text="Click for more info", activebackground=color_mid,
                                   activeforeground=text_color, borderwidth=0, selectcolor=color_mid, indicatoron=False)
            radb_log.bind("<Button-1>", callback_get_widget_row)
            radb_log.grid(sticky="n, s, e, w", row=r, column=1, columnspan=3)

            radb_type = Radiobutton(frm_results_inner, text="Logic", activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_type.bind("<Button-1>", callback_get_widget_row)
            radb_type.grid(sticky="n, s, e, w", row=r, column=4)

        r += 1  # increment rows so that items will not overlap


# =========================TO-DO=========================
# will display a selected item's info in the display area
def display_info(r):
    # destroys anything that was in the frame before
    for widget in frm_info_inner.winfo_children():
        widget.destroy()

    global item_to_edit

    display_item = search_results[r]    # get the search_result from the corresponding row
    item_to_edit = display_item         # in the case were we want to edit this item


    # Name of the item
    Label(frm_info_inner, text=str(display_item.get_name()), bg=color_light, anchor='center', font=("TkDefaultFont", fontsize+15, "bold"))\
        .grid(row=0, rowspan=2, column=0, columnspan=3, padx=spacing_out_y, pady=spacing_out_y, sticky="n, s, w, e")

    # Button to edit item
    Button(frm_info_inner, text="Edit Item", command=lambda: add_edit_item_window(True),
           activeforeground=text_color).grid(row=0, column=3, padx=spacing_out_y, pady=spacing_out_y, sticky="e")

    item_type = get_item_type(display_item)     # get the type of item being displayed
    r = 2   # set the row to an initial value

    if item_type == "Logic":        # when displaying info about logic
        Label(frm_info_inner, text="Logic").grid(padx=spacing_out_x*2, sticky="e", row=1, column=3)

    elif item_type == "Variable":    # when displaying info about a variable
        Label(frm_info_inner, text="Variable").grid(padx=spacing_out_x*1.1, sticky="e", row=1, column=3)
        display_info_var_const(display_item, 2)
        r = 3

    elif item_type == "Constant":  # when displaying info about a constant
        Label(frm_info_inner, text="Constant").grid(padx=spacing_out_x*0.9, sticky="e", row=1, column=3)
        display_info_var_const(display_item, 2)
        r = 3

    elif item_type == "Equation":  # when displaying info about a equation
        Label(frm_info_inner, text="Equation").grid(padx=spacing_out_x*0.9, sticky="e", row=1, column=3)
        display_info_equ(display_item, 3)

    elif item_type == "Theory":  # when displaying info about a theory
        Label(frm_info_inner, text="Thoery").grid(padx=spacing_out_x*1.5, pady=spacing_out_y, sticky="e", row=1, column=3)
        Label(frm_info_inner, text="theory not implemented") \
            .grid(row=2, column=0, columnspan=3)
        r = 3

    elif item_type == "Method":  # when displaying info about a method
        Label(frm_info_inner, text="Method").grid(padx=spacing_out_x*1.4, pady=spacing_out_y, sticky="e", row=1, column=3)
        Label(frm_info_inner, text=display_item.get_description()).grid(row=2, column=0, columnspan=4, sticky="n, s, e, w")

        r = 3   # set starting row

        # loops through each step and displays the steps information
        for s in range(0, display_item.get_num_steps()):
            # add step title with items name in it
            Label(frm_info_inner, text="Step " + str(s+1) + ": " + display_item.get_step(s).get_name(),
                  font=("TkDefaultFont", fontsize+6, "bold", "italic", "underline"))\
                .grid(row=r, column=0, columnspan=4, sticky="n, s, e, w", pady=spacing_out_y)
            r += 1

            i_t = get_item_type(display_item.get_step(s))
            if i_t == "Variable" or i_t == "Constant":        # variable/constant step
                display_info_var_const(display_item.get_step(s), r)
                r += 1

            elif i_t == "Equation":                    # equation step
                r = display_info_equ(display_item.get_step(s), r)
                r += 1

            Label(frm_info_inner, text=display_item.get_step(s).get_description()) \
                .grid(row=r, column=0, columnspan=4, pady=spacing_out_y)
            r += 1

    # put item description at the end for all these values as it will make the most sence
    # methods have their descriptions placed before all the steps
    if item_type != "Method":
        Label(frm_info_inner, text=display_item.get_description(), bg=color_light).grid(row=r, column=0, columnspan=4, sticky="n, s, e, w")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# used to display information for equations. was taken out just to reduce repetition
# does NOT display the name or description of the equation
def display_info_equ(equ, row):
    Label(frm_info_inner, text=equ.get_equation_normal()).grid(row=row, column=0, columnspan=3)
    row += 1

    # header for list of variables/constants
    Label(frm_info_inner, text="Featured variables/constants:",
          font=("TkDefaultFont", fontsize+3, "italic", "underline")) \
        .grid(row=row, column=0, columnspan=3, pady=spacing_out_y)
    row += 1

    # loop thorough each variable/constant and display each one's info
    for variable in equ.get_all_variables():
        # this is purely for spacing purposes
        Label(frm_info_inner, text="", fg=color_mid, font=("TkDefaultFont",1)).grid(row=row, column=0)
        row += 1

        Label(frm_info_inner, text=str(variable.get_name()), font=("TkDefaultFont", fontsize, "underline")) \
            .grid(row=row, column=0)
        row += 1

        display_info_var_const(variable, row)
        row += 1

    return row      # return the row so the above code knows where to start up again


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# used to display information for variables and constants. was taken out just to reduce repetition
# does NOT display names or descriptions
def display_info_var_const(var_or_const, row):
    Label(frm_info_inner, text="Symbol: " + var_or_const.get_symbol()) \
        .grid(row=row, column=0)

    if get_item_type(var_or_const) == "Constant":  # for a constant specifically
        Label(frm_info_inner, text="Value: " + var_or_const.get_value()) \
            .grid(row=row, column=1)

    Label(frm_info_inner, text="Units: " + var_or_const.get_units()) \
        .grid(row=row, column=2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get the corresponding string of each item type
def item_to_string(item):
    # will decide the correct save string of the item
    if isinstance(item, Variable):  # when displaying info about a variable
        item_string = str("\n" + str(item.get_name()) + '&' + str(item.get_description()) + '&' +
                          str(item.get_symbol()) + '&' + str(item.get_units()) + '&' + str(item.get_value()))
    elif isinstance(item, Constant):  # when displaying info about a constant
        item_string = str("\n"+str(item.get_name()) + '&' + str(item.get_description()) + '&' + str(item.get_symbol()) +
                          '&' + str(item.get_units()) + '&' + str(item.get_value()))
    elif isinstance(item, Equation):  # when displaying info about a equation
        item_string = str("\n" + str(item.get_name()) + '&' + str(item.get_description()) + '&' +
                          str(item.get_equation_normal()))

        for var in item.get_all_variables():
            item_string += "&type:" + str(get_item_type(var)) + '&' + item_to_string(var).replace("\n", "")

        item_string += "&end:Equation"
    elif isinstance(item, Theory):  # when displaying info about a theory
        item_string = str("\n"+str(item.get_name()) + '&' + str(item.get_description()) + '& NOT IN USE')
    elif isinstance(item, Method):  # when displaying info about a method
        item_string = str("\n"+str(item.get_name()) + '&' + str(item.get_description()))

        for step in item.get_steps():
            item_string += "&type:" + str(get_item_type(step)) + '&' + item_to_string(step).replace("\n", "")

        item_string += "&end:Method"

    elif isinstance(item, Logic):  # when displaying logic info
        item_string = str("\n"+str(item.get_name()) + '&' + str(item.get_description()) + '&' + str(item.get_image()))
    else:
        return False

    return item_string


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# will return a filled out list of items. Checks if its given multiple lines of strings or just one line
def string_to_item(lines, item_type):
    items = []
    if isinstance(lines, str):
        items = string_to_item_conversion_logic(lines, item_type)
    else:  # when an array is passed
        for line in lines:
            result = string_to_item_conversion_logic(line, item_type)
            if result:
                items.append(result)

    return items  # return the list of items


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# will return a filled out item based on the string given. Shouldn't be used on its own
def string_to_item_conversion_logic(line, item_type):
    item = False        # just in case nothing is written to this it will return a 'False' error message

    # splits the string and removes \n and puts this array into split_string
    split_line = str(line).replace("\n", "")
    split_line = split_line.split('&')

    # checks to make sure not to run the first line with description info through the item creator
    if split_line[0] != "_=^=_" and split_line[0] != "":

        # will decide and create the correct item type
        if item_type == "Variable":  # when displaying info about a variable
            item = Variable(split_line[0], split_line[2], split_line[4], split_line[3], split_line[1])
        elif item_type == "Constant":  # when displaying info about a constant
            item = Constant(split_line[0], split_line[2], split_line[4], split_line[3], split_line[1])
        elif item_type == "Equation":  # when displaying info about a equation
            list_of_var_con = []  # will hold the list of variables and constants the equation will have

            # will look at whether there are variables/constants in the string
            # if there are it will create and add them to a list of variables/constants list_of_var_con
            for i in range(0, len(split_line) - 1):
                if split_line[i] == "type:Variable":  # when there its a variable
                    list_of_var_con.append(Variable(split_line[i+1], split_line[3 + i], split_line[5 + i],
                                                    split_line[4 + i], split_line[2 + i]))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                elif split_line[i] == "type:Constant":  # when there its a constant
                    list_of_var_con.append(Constant(split_line[1 + i], split_line[3 + i], split_line[5 + i],
                                                    split_line[4 + i], split_line[2 + i]))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ""

            expr = split_line[2].replace("\\\\", "\\")

            # will create a new equation and add it to the list of items
            item = Equation(split_line[0], split_line[1], expr, list_of_var_con)
        elif item_type == "Theory":  # when displaying info about a theory
            item = Theory(split_line[0], split_line[1], split_line[2])
        elif item_type == "Method":  # when displaying info about a method
            list_of_steps = []
            for i in range(0, len(split_line)):
                inner_string = ""
                if split_line[i] == "type:Variable":
                    for s in range(1, 6):  # loop through each piece that corresponds to variables
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a variable
                    list_of_steps.append(string_to_item(inner_string, "Variable"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                if split_line[i] == "type:Constant":
                    for s in range(1, 6):  # loop through each piece that corresponds to constants
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a constant
                    list_of_steps.append(string_to_item(inner_string, "Constant"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                if split_line[i] == "type:Equation":
                    end = 0  # used to save when the end occurs

                    # find "end:Equation" to figure when the equation ends
                    for e in range(i, len(split_line)):
                        if split_line[e] == "end:Equation":
                            end = e  # save the block when "end:Equation" occurs
                            break  # stop the loop

                    for s in range(i + 1, end):  # loop through each piece that corresponds to equation
                        inner_string += split_line[s] + '&'  # puts them all into one string

                    # pass the string to convert it into an equation
                    list_of_steps.append(string_to_item(inner_string, "Equation"))

                    # will remove all item flags in already considered area
                    for s in range(i, end):  # loop through each piece that corresponds to method
                        if split_line[s] == "type:Variable" or split_line[s] == "type:Constant" or split_line[s] == "type:Equation" or \
                                split_line[s] == "type:Theory" or split_line[s] == "type:Logic" or split_line[s] == "type:Method":
                            split_line[s] = ''

                if split_line[i] == "type:Theory":
                    for s in range(1, 3):  # loop through each piece that corresponds to theory
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a theory
                    list_of_steps.append(string_to_item(inner_string, "Theory"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                if split_line[i] == "type:Method":
                    end = 0  # used to save when the end occurs

                    # find "end:Method" to figure when the method ends
                    for e in range(i, len(split_line)):
                        if split_line[e] == "end:Method":
                            end = e  # save the block when "end:Method" occurs
                            break  # stop the loop

                    for s in range(i + 1, end):  # loop through each piece that corresponds to method
                        inner_string += split_line[s] + '&'  # puts them all into one string

                    # pass the string to convert it into a method
                    list_of_steps.append(string_to_item(inner_string, "Method"))

                    # will remove all item flags in already considered area
                    for s in range(i, end):  # loop through each piece that corresponds to method
                        if split_line[s] == "type:Variable" or split_line[s] == "type:Constant" or split_line[s] == "type:Equation" or \
                                split_line[s] == "type:Theory" or split_line[s] == "type:Logic" or split_line[s] == "type:Method":
                            split_line[s] = ''

                if split_line[i] == "type:Logic":
                    for s in range(1, 4):  # loop through each piece that corresponds to logic
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a logic
                    list_of_steps.append(string_to_item(inner_string, "Logic"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

            # will combine everything together into a method item and add it to the list
            item = Method(split_line[0], split_line[1], list_of_steps)
        elif item_type == "Logic":  # when displaying logic info
            item = Logic(split_line[0], split_line[1], "image info goes here")

    return item  # return the item


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get correct file directory for item
def get_item_file_directory(item):
    # will decide the correct file directory for the item
    if isinstance(item, Variable):  # when displaying info about a variable
        file_directory = "Dictionary/variables.txt"
    elif isinstance(item, Constant):  # when displaying info about a constant
        file_directory = "Dictionary/constants.txt"
    elif isinstance(item, Equation):  # when displaying info about a equation
        file_directory = "Dictionary/equations.txt"
    elif isinstance(item, Theory):  # when displaying info about a theory
        file_directory = "Dictionary/theories.txt"
    elif isinstance(item, Method):  # when displaying info about a method
        file_directory = "Dictionary/methods.txt"
    elif isinstance(item, Logic):  # when displaying logic info
        file_directory = "Dictionary/logic.txt"
    else:
        file_directory = "Dictionary/lost_items.txt"
    return file_directory


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# will save item(s) into respective files within the dictionary directory
def save_items(items):
    # this for loop is just in case an array is given. Functionality that might be provided in the future

    try:
        for i in items:
            file = open(str(get_item_file_directory(i)), 'a')  # open the corresponding file
            file.write(item_to_string(i))  # save the corresponding item string
            file.close()  # close the file
    except TypeError:
        file = open(str(get_item_file_directory(items)), 'a')  # open the corresponding file
        file.write(item_to_string(items))  # save the corresponding item string
        file.close()  # close the file


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# saves all the lines of a target_file
def get_file_lines(target_file):

    file_existence_filter(target_file)

    file = open(target_file, 'r')  # open file
    lines = file.readlines()  # save the lines
    file.close()  # close the file

    return lines


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# will filter the target file to make sure it exists. if it doesn't it will create it
def file_existence_filter(target_file):
    try:
        file = open(target_file, 'r')  # open file
        file.close()  # close the file
    except FileNotFoundError:
        file = open(target_file, 'w')  # open file

        if target_file == "Dictionary/variables.txt":       # when writing info for a variable
            file.write("_=^=_& name & description & symbol & unit & last saved value")
        elif target_file == "Dictionary/constants.txt":     # when writing info for a constant
            file.write("_=^=_& name & description & symbol & unit & value")
        elif target_file == "Dictionary/equations.txt":  # when writing info for a equation
            file.write("_=^=_& name & description & equation in latex form & list of accompanying items")
        elif target_file == "Dictionary/theories.txt":  # when writing info for a theory
            file.write("_=^=_& name & description & other unfinished shite")
        elif target_file == "Dictionary/logic.txt":  # when writing info for a logic
            file.write("_=^=_& name & description & image")
        elif target_file == "Dictionary/methods.txt":  # when writing info for method
            file.write("_=^=_& name & description & steps listed as various items")

        file.close()  # close the file


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# will return a letter based on the type of item
def get_item_type(item):
    if isinstance(item, Variable):  # when displaying info about a variable
        item_type = "Variable"
    elif isinstance(item, Constant):  # when displaying info about a constant
        item_type = "Constant"
    elif isinstance(item, Equation):  # when displaying info about a equation
        item_type = "Equation"
    elif isinstance(item, Theory):  # when displaying info about a theory
        item_type = "Theory"
    elif isinstance(item, Method):  # when displaying info about a method
        item_type = "Method"
    elif isinstance(item, Logic):  # when displaying logic info
        item_type = "Logic"
    else:
        item_type = False
    return item_type


# =========================TO-DO=========================
# used to create the add/edit item window
def add_edit_item_window(to_edit):
    # stuff for creating the pop-up window
    small_win = Toplevel()
    small_win.configure(background=color_dark)
    small_win.grid_rowconfigure(0, weight=1)
    small_win.grid_columnconfigure(0, weight=1)

    small_win.grab_set()        # stops the user from interacting with the main window

    # the frame that will hold the canvas and all the other scrolling shite
    frm_add_edit_scroll_wrapper = Frame(small_win, highlightthickness=1, highlightbackground=accent_light)
    # reveals the frame holding the scrollbar, canvas, and wrapping frame
    frm_add_edit_scroll_wrapper.grid(column=0, row=0, sticky="n, s, e, w")
    # configures the row with the canvas to be able to expand
    frm_add_edit_scroll_wrapper.grid_rowconfigure(0, weight=1)
    frm_add_edit_scroll_wrapper.grid_columnconfigure(0, weight=1)

    # the canvas that will enable the possibility to scroll through the various search results
    canv_add_edit = Canvas(frm_add_edit_scroll_wrapper)
    # frame in which the results will be listed
    frm_add_edit_inner = Frame(canv_add_edit, bg=color_mid)
    # scroll bar that will can scroll through results shown in frm_results_inner on the canvas
    srlb_add_edit = Scrollbar(frm_add_edit_scroll_wrapper, orient="vertical", command=canv_add_edit.yview)

    # configures the canvas to include a scrolling command linked to the scrollbar
    canv_add_edit.configure(yscrollcommand=srlb_add_edit.set)

    # write out everything for the search results. They won't show up because
    canv_add_edit.grid(column=0, row=0, sticky="n, s, e, w")
    srlb_add_edit.grid(column=1, row=0, sticky="n, s, e, w")

    # creates a window in which the frame is placed. This allows the frame to be scrolled through
    canv_add_edit.create_window((0, 0), window=frm_add_edit_inner, anchor='nw')

    # calls the function that will actually enable the scrolling. I don't understand why this works so leave it alone
    frm_add_edit_inner.bind("<Configure>", lambda e: canv_add_edit.configure(scrollregion=canv_add_edit.bbox("all")))

    # configures the row with the canvas to be able to expand
    frm_add_edit_inner.grid_columnconfigure(1, weight=1)

    lab_name = Label(frm_add_edit_inner, text="Name:",
                     highlightthickness=1, highlightbackground=accent_light)
    lab_name.grid(column=0, row=1, sticky="n, s, e, w")
    txt_name = Entry(frm_add_edit_inner,
                     highlightthickness=1, highlightbackground=accent_light)
    txt_name.grid(column=1, columnspan=2, row=1, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    lab_def = Label(frm_add_edit_inner, text="Definition:", highlightthickness=1,
                    highlightbackground=accent_light)
    lab_def.grid(column=0, row=2, sticky="n, s, e, w")
    txt_def = Entry(frm_add_edit_inner,
                    highlightthickness=1, highlightbackground=accent_light)
    txt_def.grid(column=1, columnspan=2, row=2, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_name.insert(0, item_to_edit.get_name())
        txt_def.insert(0, item_to_edit.get_description())

    # drop down for adding items, "e" will give the option that was clicked on
    opm_type = OptionMenu(frm_add_edit_inner, item_type_to_add_or_edit,
                          "Logic", "Constant", "Variable", "Equation", "Theory", "Method",
                          command=lambda e: add_edit_item_option_display(e, frm_add_edit_inner, False))
    opm_type.grid(column=0, columnspan=2, row=0, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    Button(frm_add_edit_inner, text="Submit Item", command=lambda: item_submit(frm_add_edit_inner, to_edit))\
        .grid(column=2, row=0, sticky="n, s, e, w")

    # will set the initial value of the option menu to the correct item type
    if to_edit:
        small_win.title("Edit")

        it = get_item_type(item_to_edit)

        if it == "Variable":
            item_type_to_add_or_edit.set("Variable")
            add_edit_item_option_display("Variable", frm_add_edit_inner, to_edit)
        elif it == "Constant":
            item_type_to_add_or_edit.set("Constant")
            add_edit_item_option_display("Constant", frm_add_edit_inner, to_edit)
        elif it == "Equation":
            item_type_to_add_or_edit.set("Equation")
            add_edit_item_option_display("Equation", frm_add_edit_inner, to_edit)
        elif it == "Method":
            item_type_to_add_or_edit.set("Method")
            add_edit_item_option_display("Method", frm_add_edit_inner, to_edit)
        elif it == "Logic":
            item_type_to_add_or_edit.set("Logic")
        else:
            item_type_to_add_or_edit.set("Theory")
            add_edit_item_option_display("Theory", frm_add_edit_inner, to_edit)

    else:
        small_win.title("Add")
        item_type_to_add_or_edit.set("Logic")

    small_win.mainloop()


# =========================TO-DO=========================
# displays the correct input criteria for each of the item types
def add_edit_item_option_display(type_to_display, container_widget, to_edit):
    # saves all the widgets after the first 5 which are always gonna be there
    widgets = container_widget.winfo_children()[6:]

    # deletes those widgets to remove remnants
    for w in widgets:
        w.destroy()

    # reset this value as something different is being added
    global step_num
    step_num = 1

    row = 3
    # will decide what needs to be displayed depending on the type of item
    if type_to_display == "Variable" or type_to_display == "Constant":  # when displaying info about a variable/constant
        add_edit_item_v_or_c_display(type_to_display, container_widget, to_edit, item_to_edit)

    elif type_to_display == "Equation":  # when displaying info about a equation
        add_edit_item_equation_display(container_widget, to_edit, item_to_edit)

    elif type_to_display == "Theory":  # when displaying info about a theory
        lab_theory = Label(container_widget, text="Theory in limbo and not done.",
                           relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
        lab_theory.grid(column=0, row=3, columnspan=3, sticky="n, s, e, w")

    elif type_to_display == "Method":  # when displaying info about a method
        selected_item_to_add = StringVar()  # create the item type in this fancy way I don't understand
        selected_item_to_add.set("Select an item to add")  # will set the initial value

        opm_type = OptionMenu(container_widget, selected_item_to_add,
                              "Logic", "Constant", "Variable", "Equation", "Theory")
        opm_type.grid(column=1, columnspan=2, row=3, sticky="n, s, e, w")

        Button(container_widget, text="Add Step:",
               command=lambda: add_edit_method_step_add(selected_item_to_add.get(), container_widget, to_edit, ""))\
            .grid(column=0, row=3, sticky="n, s, e, w")

        # will automatically display all the steps affiliated with this method when in editing mode
        if to_edit:
            for step in item_to_edit.get_steps():
                add_edit_method_step_add(get_item_type(step), container_widget, to_edit, step)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# displays the correct input criteria for each of the item types
def add_edit_item_v_or_c_display(type_to_display, container_widget, to_edit, e_item):
    r = container_widget.winfo_children()[-1].grid_info()['row'] + 3    # not sure why it always gets 0 but it works

    lab_sym = Label(container_widget, text="Symbol:",
                    relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    lab_sym.grid(column=0, row=r, sticky="n, s, e, w")
    txt_sym = Entry(container_widget,
                    relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    txt_sym.grid(column=1, columnspan=2, row=r, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    r += 1

    if type_to_display == "Constant":  # for the constant specifically
        lab_val = Label(container_widget, text="Value:",
                        relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
        lab_val.grid(column=0, row=r, sticky="n, s, e, w")
        txt_val = Entry(container_widget,
                        relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
        txt_val.grid(column=1, columnspan=2, row=r, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        # will add the edit item's stuff into the entry boxes
        if to_edit:
            txt_val.insert(0, e_item.get_value())

        r += 1

    lab_unit = Label(container_widget, text="Units:",
                     relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    lab_unit.grid(column=0, row=r, sticky="n, s, e, w")
    txt_unit = Entry(container_widget,
                     relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    txt_unit.grid(column=1, columnspan=2, row=r, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    r += 1

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_sym.insert(0, e_item.get_symbol())
        txt_unit.insert(0, e_item.get_units())

    return r


# =========================TO-DO=========================
# displays the correct input criteria for each of the item types
def add_edit_item_equation_display(container_widget, to_edit, equ_to_display):
    start_row = container_widget.winfo_children()[-1].grid_info()['row']+3

    lab_equ = Label(container_widget, text="Equation:", highlightthickness=1,
                    highlightbackground=accent_light)
    lab_equ.grid(column=0, row=start_row, sticky="n, s, e, w")
    txt_equ = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
    txt_equ.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    start_row += 1

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_equ.insert(0, equ_to_display.get_equation_normal())

    frm_equ_holder = Frame(container_widget)
    frm_equ_holder.grid(column=0, columnspan=3, row=start_row, sticky="n, s, e, w")
    frm_equ_holder.columnconfigure(2, weight=1)
    frm_equ_holder.columnconfigure(3, weight=1)

    Label(frm_equ_holder, text="Featured variables/constants:", highlightthickness=1, highlightbackground=accent_light,
          font=("TkDefaultFont", fontsize+2, "bold", "italic"))\
        .grid(column=0, columnspan=2, row=1, sticky="n, s, e, w")

    frm_add_btns_holder = Frame(frm_equ_holder)
    frm_add_btns_holder.grid(column=2, row=1, sticky="n, s, e, w")
    frm_add_btns_holder.columnconfigure(0, weight=1)
    frm_add_btns_holder.columnconfigure(1, weight=1)

    btn_add_var = Button(frm_add_btns_holder, text="Add Variable",
                         command=lambda: add_edit_item_equation_item_add("Variable", frm_equ_holder, False))
    btn_add_var.grid(column=0, row=0, sticky="n, s, e, w")

    btn_add_const = Button(frm_add_btns_holder, text="Add Constant",
                           command=lambda: add_edit_item_equation_item_add("Constant", frm_equ_holder, False))
    btn_add_const.grid(column=1, row=0, sticky="n, s, e, w")

    # will automatically display all the variables and constants affiliated with this equation when in editing mode
    if to_edit:
        for var_const in equ_to_display.get_all_variables():
            add_edit_item_equation_item_add(var_const, frm_equ_holder, to_edit)


# =========================TO-DO=========================
# displays wrapping items then calls add_edit_item_v_or_c_display to display all var/const in/to add to the equation 
def add_edit_item_equation_item_add(item_to_add, container_widget, to_edit):
    if to_edit:
        type_to_display = get_item_type(item_to_add)
    else:
        type_to_display = item_to_add

    start_row = container_widget.winfo_children()[-1].grid_info()['row'] + 1

    if type_to_display == "Variable":
        Label(container_widget, text="Variable:",
              anchor="center", font=("TkDefaultFont", fontsize,"italic", "underline"))\
            .grid(column=0, columnspan=3, row=start_row, sticky="n, s, e, w")

    else:
        Label(container_widget, text="Constant:",
              anchor="center", font=("TkDefaultFont", fontsize, "italic", "underline"))\
            .grid(column=0, columnspan=3, row=start_row, sticky="n, s, e, w")

    start_row += 1

    lab_name = Label(container_widget, text="Name:", highlightthickness=1, highlightbackground=accent_light)
    lab_name.grid(column=0, row=start_row, sticky="n, s, e, w")
    txt_name = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
    txt_name.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    start_row += 1

    lab_def = Label(container_widget, text="Definition:", highlightthickness=1, highlightbackground=accent_light)
    lab_def.grid(column=0, row=start_row, sticky="n, s, e, w")
    txt_def = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
    txt_def.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    start_row += 1

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_name.insert(0, item_to_add.get_name())
        txt_def.insert(0, item_to_add.get_description())

    add_edit_item_v_or_c_display(type_to_display, container_widget, to_edit, item_to_add)


# =========================TO-DO=========================
# displays wrapping items then calls respective item addition to display all items in/to add to the method
def add_edit_method_step_add(type_to_display, container_widget, to_edit, item_to_display):
    global step_num

    # used to check to make sure user selected an actual item
    if type_to_display != "Select an item to add":
        start_row = container_widget.winfo_children()[-1].grid_info()['row'] + 1

        Label(container_widget, highlightthickness=1, text="Step " + str(step_num) + ": " + str(type_to_display),
                         highlightbackground=accent_light, font=("TkDefaultFont", fontsize + 5, "bold", "italic"))\
            .grid(column=0, columnspan=3, row=start_row, sticky="n, s, e, w")

        step_num += 1
        start_row += 1

        lab_name = Label(container_widget, text="Name:")
        lab_name.grid(column=0, row=start_row, sticky="n, s, e, w")
        txt_name = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
        txt_name.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        start_row += 1

        lab_def = Label(container_widget, text="Definition:", highlightthickness=1, highlightbackground=accent_light)
        lab_def.grid(column=0, row=start_row, sticky="n, s, e, w")
        txt_def = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
        txt_def.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        start_row += 1

        # will add the edit item's stuff into the entry boxes
        if to_edit:
            txt_name.insert(0, item_to_display.get_name())
            txt_def.insert(0, item_to_display.get_description())

            start_row += 1

            if type_to_display == "Constant":
                add_edit_item_v_or_c_display("Constant", container_widget, to_edit, item_to_display)

            elif type_to_display == "Variable":
                add_edit_item_v_or_c_display("Variable", container_widget, to_edit, item_to_display)

            elif type_to_display == "Equation":
                add_edit_item_equation_display(container_widget, to_edit, item_to_display)

            elif type_to_display == "Theory":
                Label(container_widget, text="Theory isn't functional").grid(column=0, columnspan=3, row=start_row, sticky="n, s, e, w")

        else:
            if type_to_display == "Constant":
                add_edit_item_v_or_c_display("Constant", container_widget, False, item_to_display)
            elif type_to_display == "Variable":
                add_edit_item_v_or_c_display("Variable", container_widget, False, item_to_display)
            elif type_to_display == "Equation":
                add_edit_item_equation_display(container_widget, False, item_to_display)
            elif type_to_display == "Theory":
                Label(container_widget, text="Theory isn't functional").grid(column=0, columnspan=2, row=start_row, sticky="n, s, e, w")

    else:
        print("Please select an item pop-up window would occur here")


# will add or edit the item the user has given
def item_submit(container_widget, to_edit):
    list_of_widgets = container_widget.winfo_children()
    item_type_item_to_edit = get_item_type(item_to_edit)
    time_type_selected = item_type_to_add_or_edit.get()

    item_to_save = ""
    list_of_txt_box_text = []

    # collect all the text boxes into a list
    for item in list_of_widgets:
        if item.winfo_class() == "Entry":
            list_of_txt_box_text.append(item.get())

    # will start the save logic corresponding to what the user wants to save
    if time_type_selected == "Logic":
        item_to_save = item_submit_log_var_const(list_of_txt_box_text)

    elif time_type_selected == "Variable":
        item_to_save = item_submit_log_var_const(list_of_txt_box_text)

    elif time_type_selected == "Constant":
        item_to_save = item_submit_log_var_const(list_of_txt_box_text)

    elif time_type_selected == "Constant":
        item_to_save = item_submit_log_var_const(list_of_txt_box_text)

    elif time_type_selected == "Equation":
        item_to_save = item_submit_equ(list_of_txt_box_text, list_of_widgets[-1].winfo_children())

    elif time_type_selected == "Method":
        last_child = LabelFrame()
        list_of_steps = []
        list_of_frames = []
        i_entry = 2
        i_frame = 0

        # get all frames in the list_of_widgets. Used only for equations
        for item in list_of_widgets:
            if item.winfo_class() == "Frame":
                list_of_frames.append(item)

        for child in list_of_widgets:
            if last_child.winfo_class() == child.winfo_class() and last_child.winfo_class() == "Label" and last_child.cget("text") != "Theory isn't functional":
                # will keep characters after the ":" then remove the space just before the actual word
                text = last_child.cget("text").rsplit(":", 1)[1]
                check_text = text[1:]

                if check_text == "Variable":
                    list_of_steps.append(item_submit_log_var_const(list_of_txt_box_text[i_entry:i_entry + 4]))
                    i_entry += 4

                elif check_text == "Constant":
                    list_of_steps.append(item_submit_log_var_const(list_of_txt_box_text[i_entry:i_entry + 5]))
                    i_entry += 5

                elif check_text == "Logic":
                    list_of_steps.append(item_submit_log_var_const(list_of_txt_box_text[i_entry:i_entry + 2]))
                    i_entry += 2

                elif check_text == "Theory":
                    list_of_steps.append(Theory(list_of_txt_box_text[i_entry], list_of_txt_box_text[i_entry+1],
                                                "Equation would go here"))
                    i_entry += 1

                elif check_text == "Equation":
                    list_of_steps.append(item_submit_equ(list_of_txt_box_text[i_entry:i_entry + 3],
                                                         list_of_frames[i_frame].winfo_children()))
                    i_frame += 1
                    i_entry += 3

            last_child = child

        item_to_save = Method(list_of_txt_box_text[0], list_of_txt_box_text[1], list_of_steps)

    save_items(item_to_save)

    # # if the user wants the edit an item they can change the type of item they want to edit
    # if to_edit and item_type_item_to_edit == time_type_selected:
    #     pass
    #
    # # if they are adding a new item
    # else:
    #     save_items(item_to_save)


# will return a logic, variable, or constant depending on the length of list given
def item_submit_log_var_const(text_list):
    if len(text_list) < 4:
        return Logic(text_list[0], text_list[1], "image not done")

    elif len(text_list) == 4:
        return Variable(text_list[0], text_list[2], 0, text_list[3], text_list[1])

    else:
        return Constant(text_list[0], text_list[2], text_list[3], text_list[4], text_list[1])


# will return a equation filled out equation
def item_submit_equ(outer_text_list, equ_frame_children):
    equ_frame_txt_box_text = []

    # get list of entry boxes inside the equation frame
    for item in equ_frame_children:
        if item.winfo_class() == "Entry":
            equ_frame_txt_box_text.append(item.get())

    equ_last_frame_child = LabelFrame()
    list_of_variables = []
    i_entry = 0

    for child in equ_frame_children:
        if equ_last_frame_child.winfo_class() == child.winfo_class() and equ_last_frame_child.winfo_class() == "Label":
            if equ_last_frame_child.cget("text") == "Variable:":
                list_of_variables.append(item_submit_log_var_const(equ_frame_txt_box_text[i_entry:i_entry + 4]))
                i_entry += 4

            elif equ_last_frame_child.cget("text") == "Constant:":
                list_of_variables.append(item_submit_log_var_const(equ_frame_txt_box_text[i_entry:i_entry + 5]))
                i_entry += 5

        equ_last_frame_child = child

    return Equation(outer_text_list[0], outer_text_list[1], outer_text_list[2], list_of_variables)


# ======================================================================================================================
# ============================================ NOW THE MAIN CODE BODY BEGINS ===========================================
# ======================================================================================================================


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ---------------------------big title label---------------------------
lab_title = Label(window, text="Dictionary of the Humble First Class Engineer", bg=color_dark,
                  font=("TkDefaultFont", fontsize*3), relief="ridge", highlightbackground="red", highlightthickness=5)
lab_title.grid(column=0, columnspan=2, row=0, padx=spacing_out_x, pady=spacing_out_y,
               ipadx=spacing_out_x / 2, ipady=spacing_out_y / 2)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ---------------------------left side frame stuff---------------------------
frm_left = Frame(window, bg=color_dark)
frm_left.grid(column=0, row=1, sticky="n, s, e, w", padx=spacing_out_x, pady=spacing_out_y)
frm_left.grid_rowconfigure(2, weight=1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ---------------------------area for check boxes of what to include in search---------------------------
# the frame for the accompanying stuff to go in
frm_checkbox_holder = LabelFrame(frm_left, text="What to include in the search?",
                                 highlightthickness=1, highlightbackground=accent_light)
frm_checkbox_holder.grid(column=1, row=0, sticky="n, s, e, w")
frm_checkbox_holder.grid_columnconfigure(0, weight=1)
frm_checkbox_holder.grid_columnconfigure(1, weight=1)


# frame that holds the checkboxes with the types of items to look though along with checkboxes
frm_item_type_checkboxs = LabelFrame(frm_checkbox_holder, text="Item Types:",
                                     highlightthickness=1, highlightbackground=accent_light)
frm_item_type_checkboxs.grid(column=0, row=0, sticky="n, s, e, w", pady=spacing_in*2, padx=spacing_in*2)
# checkboxes for the various areas one can search
Checkbutton(frm_item_type_checkboxs, text="Logic", variable=search_logic) \
    .grid(column=0, row=0, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Variables", variable=search_variables) \
    .grid(column=1, row=0, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Constants", variable=search_constants) \
    .grid(column=2, row=0, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Equations", variable=search_equations) \
    .grid(column=0, row=1, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Theories", variable=search_theories)\
    .grid(column=1, row=1, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Methods", variable=search_methods) \
    .grid(column=2, row=1, sticky="n, s, e, w")


# frame that holds the checkboxes with the places to look though along with checkboxes
frm_places_checkboxs = LabelFrame(frm_checkbox_holder, text="Places to Look:",
                                  relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
frm_places_checkboxs.grid(column=1, row=0, rowspan=2, sticky="n, s, e, w", pady=spacing_in*2, padx=spacing_in*2)
# checkboxes for the various areas one can search
Checkbutton(frm_places_checkboxs, text="Name", variable=search_names) \
    .grid(column=0, row=0, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Description", variable=search_description) \
    .grid(column=1, row=0, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Symbol", variable=search_symbol) \
    .grid(column=0, row=1, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Value", variable=search_value) \
    .grid(column=1, row=1, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Units", variable=search_units) \
    .grid(column=0, row=2, sticky="n, s, e, w")


# button to show everything from the selected item types
btn_search = Button(frm_checkbox_holder, text="Show everything from selected item types.", command=print_all)
# , groove, raised, ridge, , sunken

btn_search.grid(column=0, row=1, sticky="n, s, e, w", padx=spacing_in*1.45, pady=spacing_in*1.45)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ---------------------------area for text input to search stuff---------------------------
# the frame for the accompanying stuff to go in
frm_input = LabelFrame(frm_left, text="What do you want to search for?",
                       highlightthickness=1, highlightbackground=accent_light, highlightcolor=accent_light)
frm_input.grid(column=1, row=1, sticky="n, s, e, w", pady=spacing_out_y * 2)

# text box to get user input
txt_search = Entry(frm_input, highlightthickness=1, highlightbackground=accent_light, selectbackground="green", selectforeground = "red")
txt_search.grid(column=0, columnspan=2, row=1, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)
txt_search.bind("<Return>", lambda x: search())     # allows user to press enter to search

# button to begin searching. Calls the "print_search" function that starts the process of printing results
btn_search = Button(frm_input, text="Search", command=search, activeforeground=text_color)
btn_search.grid(column=1, row=1, sticky="n, s", padx=spacing_in, pady=spacing_in)

# this stuff is for sorting out the resizing of the textbox so that its always as wide as it needs to be
frm_input.grid_columnconfigure(0, weight=1)


# =========================TO-DO=========================
# ---------------------------area for search results---------------------------
# wrapper frame for everything going into the search results area
frm_results = LabelFrame(frm_left, text="Search results", highlightthickness=1, highlightbackground=accent_light)
frm_results.grid(column=1, row=2, sticky="n, s, e, w")
# this stuff is for sorting out the resizing of the middle row and frm_results_scroll_wrapper
frm_results.grid_rowconfigure(1, weight=1)

# the frame that will hold the information about the columns
frm_results_titlerow = Frame(frm_results, highlightthickness=1, highlightbackground=accent_light)
frm_results_titlerow.grid(column=0, columnspan=2, row=0, sticky="w")

# the frame that will hold the canvas and all the other scrolling shite
frm_results_scroll_wrapper = Frame(frm_results, highlightthickness=1, highlightbackground=accent_light)
# reveals the frame holding the scrollbar, canvas, and wrapping frame
frm_results_scroll_wrapper.grid(column=0, columnspan=2, row=1, sticky="n, s, e, w")
# configures the row with the canvas to be able to expand
frm_results_scroll_wrapper.grid_rowconfigure(0, weight=1)
frm_results_scroll_wrapper.grid_columnconfigure(0, weight=1)

# the canvas that will enable the possibility to scroll through the various search results
canv_results = Canvas(frm_results_scroll_wrapper)
# frame in which the results will be listed
frm_results_inner = Frame(canv_results, bg=color_mid)
# scroll bar that will can scroll through results shown in frm_results_inner on the canvas
srlb_results = Scrollbar(frm_results_scroll_wrapper, orient="vertical", command=canv_results.yview)

# configures the canvas to include a scrolling command linked to the scrollbar
canv_results.configure(yscrollcommand=srlb_results.set)

# write out everything for the search results. They won't show up because
canv_results.grid(column=0, row=0, sticky="n, s, e, w")
srlb_results.grid(column=1, row=0, sticky="n, s, e, w")

# creates a window in which the frame is placed. This allows the frame to be scrolled through
canv_results.create_window((0, 0), window=frm_results_inner, anchor='nw')

# calls the function that will actually enable the scrolling. I don't understand why this works so leave it alone
frm_results_inner.bind("<Configure>", lambda e: canv_results.configure(scrollregion=canv_results.bbox("all")))

# create the button that will be used to add more items
btn_add_item = Button(frm_results, text="Add a new item", command=lambda: add_edit_item_window(False),
                      activeforeground=text_color)
btn_add_item.grid(column=1, row=2, sticky="e")

# create the button that will be used to delete more items
btn_add_item = Button(frm_results, text="Delete selected item", command="",
                      activeforeground=text_color)
btn_add_item.grid(column=0, row=2, sticky="w")


# print column titles for easier user understanding
lab_result_name = Label(frm_results_titlerow, bg=color_light, text="Name", anchor="center")
lab_result_name.grid(row=0, column=0, padx=spacing_out_x*3, sticky="w")
lab_result_info = Label(frm_results_titlerow, bg=color_light, text="Information", anchor="center")
lab_result_info.grid(row=0, column=1, padx=spacing_out_x*8)
lab_result_type = Label(frm_results_titlerow, bg=color_light, text="Type", anchor="center")
lab_result_type.grid(row=0, column=2, padx=spacing_out_x*3)

# this is for spacing the titles to fit properly
srlb_results.update()
lab_result_spacing = Label(frm_results_titlerow, text="", width=int(srlb_results.winfo_width() / m_len), background=color_light)
lab_result_spacing.grid(row=0, column=3)

# =========================TO-DO=========================
# ---------------------------area to display item information---------------------------
# the frame for the accompanying stuff to go in
frm_info = Frame(window)
frm_info.grid(column=1, row=1, sticky="n, s, e, w", padx=spacing_out_x, pady=spacing_out_y)


# the outer frame that will hold all information stuff
frm_info_scroll_wrapper = Frame(frm_info, bg=color_mid, highlightthickness=1, highlightbackground=accent_light)
# the canvas that will enable the possibility of scrolling through the info
canv_info = Canvas(frm_info_scroll_wrapper)
# frame in which the info will be placed
frm_info_inner = Frame(canv_info)

# scroll bar that will can scroll through the info shown in frm_info_inner on the canvas
srlb_info = Scrollbar(frm_info_scroll_wrapper, orient="vertical", command=canv_info.yview)
# configures the canvas to include a scrolling command linked to the scrollbar
canv_info.configure(yscrollcommand=srlb_info.set)

# display in everything for the search results. They won't show up because frm_info_scroll_wrapper is not displayed yet
canv_info.grid(column=0, row=0, sticky="n, s, e, w")
srlb_info.grid(column=1, row=0, sticky="n, s, e, w")

# creates a window in which the frame is placed. This allows the frame to be scrolled through
canv_info.create_window((0, 0), window=frm_info_inner, anchor='nw')

# calls the function that will actually enable the scrolling. I don't understand why this works so leave it alone
frm_info_inner.bind("<Configure>",
                    lambda e: canv_info.configure(scrollregion=canv_info.bbox("all")))

# this stuff is for sorting out the resizing of the frame holding the scrolling canvas
frm_info.grid_columnconfigure(0, weight=1)
frm_info.grid_rowconfigure(0, weight=1)
frm_info_scroll_wrapper.grid_columnconfigure(0, weight=1)
frm_info_scroll_wrapper.grid_rowconfigure(0, weight=1)
frm_info_inner.grid_columnconfigure(4, weight=1)

frm_info_scroll_wrapper.grid(column=0, row=0, sticky="n, s, e, w")


# ---------------------------keeping the window open and some widget sizing stuff---------------------------
window.mainloop()  # keeps the window open

# extra stuff that could come in handy
# frm_info.update()  # need to call this to get the size of the item
# print(str(frm_info.winfo_width()))
# print(str(lab_search.winfo_height()))
# save_items(test_items)