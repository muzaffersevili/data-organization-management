import csv
import json

# 2019510016 Elif Aras - 2019510069 Muzaffer Sevili

dict_student = {}
sorted_dict_student = {}
selected_student = {}
sorted_selected_student = {}


# ############################################################################### DICT OPERATION
def sorted_dict():
    S = sorted(dict_student.items(), key=lambda x: x[0], reverse=False)
    for elements in S:
        sorted_dict_student[elements[0]] = elements[1]


def crate_dict():
    with open('students.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')
        next(readCSV)
        for row in readCSV:
            dict_student[int(row[0])] = [int(row[0]), row[1], row[2], row[3], int(row[4])]


# ############################################################################### GENERAL SEARCH IN DICT
# The "key" information of the studentsn(exp: grade !< 40) who supply the required condition is kept in the list data structure. 
def students_keys(index, control_operation, student, control_int_or_string):
    keys_list = []
    for key, value in sorted_dict_student.items():
        if control_operation == "=":
            if value[index] == student:
                keys_list.append(key)
        elif control_operation == "!=":
            if value[index] != student:
                keys_list.append(key)

        if not control_int_or_string:  # for int value
            if control_operation == "<":
                if value[index] < student:
                    keys_list.append(key)
            elif control_operation == ">":
                if value[index] > student:
                    keys_list.append(key)
            elif control_operation == "<=" or control_operation == "!>":
                if value[index] <= student:
                    keys_list.append(key)
            elif control_operation == ">=" or control_operation == "!<":
                if value[index] >= student:
                    keys_list.append(key)
    return keys_list

# Required "key" list is kept according to the attribute type in the condition
def condition(string_line, i):
    info_split = string_line.split()
    key_list = []
    if info_split[i].lower() == "id":
        key_list = students_keys(0, info_split[i + 1], int(info_split[i + 2]), False)
    elif info_split[i].lower() == "name":
        key_list = students_keys(1, info_split[i + 1], info_split[i + 2][1:-1], True)
    elif info_split[i].lower() == "lastname":
        key_list = students_keys(2, info_split[i + 1], info_split[i + 2][1:-1], True)
    elif info_split[i].lower() == "email":
        key_list = students_keys(3, info_split[i + 1], info_split[i + 2][1:-1], True)
    elif info_split[i].lower() == "grade":
        key_list = students_keys(4, info_split[i + 1], int(info_split[i + 2]), False)
    return key_list


# ############################################################################### ADD STUDENT
def add_student(add_student, control):
    info = add_student[7:-1]
    info_split = info.split(",")
    if not control:
        sorted_dict_student[int(info_split[0])] = [int(info_split[0]), info_split[1], info_split[2], info_split[3],
                                                   int(info_split[4])]
    if control:
        selected_student[int(info_split[0])] = [int(info_split[0]), info_split[1], info_split[2], info_split[3],
                                                int(info_split[4])]


# ############################################################################### DELETE STUDENT
# Students are deleted according to condition number and condition type
def sub_func_del(con_type, key_list1, key_list2, and_or, control):
    if con_type == 1:
        for e in key_list1:
            if control:
                del selected_student[e]
            else:
                del sorted_dict_student[e]
    else:
        for e in (set(key_list1) & set(key_list2)):
            if control:
                del selected_student[e]
            else:
                del sorted_dict_student[e]
        if and_or == "or":
            for e in (set(key_list1) ^ set(key_list2)):
                if control:
                    del selected_student[e]
                else:
                    del sorted_dict_student[e]

# The sub_func_del function is called according to the condition.
def delete_student(delete_string_line, control):
    # name = 'John' and grade <= 20
    info_split = delete_string_line.split()
    key_list2 = []
    key_list1 = condition(delete_string_line, 0)
    if len(info_split) == 3:
        sub_func_del(1, key_list1, key_list2, "", control)
    elif len(info_split) == 7:
        key_list2 = condition(delete_string_line, 4)
        sub_func_del(2, key_list1, key_list2, info_split[3].lower(), control)


# ############################################################################### SELECT STUDENT
# Students are selected according to condition number and condition type
def sub_func_select(con_type, key_list1, key_list2, and_or):
    if con_type == 1:
        for e in key_list1:
            selected_student[e] = sorted_dict_student.get(e)
    else:
        for e in (set(key_list1) & set(key_list2)):
            selected_student[e] = sorted_dict_student.get(e)
        if and_or == "or":
            for e in (set(key_list1) ^ set(key_list2)):
                selected_student[e] = sorted_dict_student.get(e)

# The sub_func_select function is called according to the condition.
def select_student(con_number, sel_attribute1, sel_con1, sel_value1, or_and, sel_attribute2, sel_con2, sel_value2):
    # SELECT xxx FROM STUDENTS WHERE grade !< 40 ORDER BY ASC              --> 11 data
    # SELECT xxx FROM STUDENTS WHERE grade !< 40 or id !< 40 ORDER BY ASC  --> 15 data
    key_list1 = []
    key_list2 = []

    string_line = sel_attribute1 + " " + sel_con1 + " " + sel_value1
    key_list1 = condition(string_line, 0)
    if con_number == 1:
        sub_func_select(1, key_list1, key_list2, "")
    elif con_number == 2:
        string_line = sel_attribute2 + " " + sel_con2 + " " + sel_value2
        key_list2 = condition(string_line, 0)
        sub_func_select(2, key_list1, key_list2, or_and)

# asc dsc event in select is happening
def asc_dsc(asc_or_dsc):
    sorted_control = False
    if asc_or_dsc.lower() == "dsc":
        sorted_control = True
    S = sorted(selected_student.items(), key=lambda x: x[0], reverse=sorted_control)
    for elements in S:
        sorted_selected_student[elements[0]] = elements[1]


def print_select(json_info):
    split_json = json_info.split(",")
    for key, value in sorted_selected_student.items():
        i = 0
        for j in split_json:
            if j.lower() == "all":
                print("id:", value[0]," - name: ", value[1]," - lastname: ", value[2]," - email: ", value[3]," - grade:", value[4])
            elif j == "id":
                print("id:", value[0], end=" ")
            elif j == "name":
                print("name: " + value[1], end=" ")
            elif j == "lastname":
                print("lastname: " + value[2], end=" ")
            elif j == "email":
                print("email: " + value[3], end=" ")
            elif j == "grade":
                print("grade:", value[4], end="  ")

            if i != len(split_json) - 1:
                print(end="- ")
                i = i + 1

        print()


# INPUT CONTROL FOR SELECTION
def sel_control(sel_input, i):
    controller = False

    # id-grade, operations, integer girişi ve "order by asc/dsc" kontrolü
    if (sel_input[i] == 'id' or sel_input[i] == 'grade') and (sel_input[i + 1] == '=' or sel_input[i + 1] == '!=' or
                                                              sel_input[i + 1] == '>' or sel_input[i + 1] == '<' or
                                                              sel_input[i + 1] == '<=' or
                                                              sel_input[i + 1] == '>=' or sel_input[i + 1] == '!<' or
                                                              sel_input[i + 1] == '!>') and (
            sel_input[i + 2][:1] != "‘" and sel_input[i + 2][-1] != "’") and sel_input[i + 3] == "order" and \
            sel_input[i + 4] == "by" and (sel_input[i + 5] == "asc" or sel_input[i + 5] == "dsc"):
        controller = True

    # name-lastname-email, string operations, string girişi ve "order by asc/dsc" kontrolü
    elif (sel_input[i] == 'name' or sel_input[i] == 'lastname' or sel_input[i] == 'email') and (sel_input[i + 1] == '='
                                                                                                or sel_input[
                                                                                                    i + 1] == '!=') and (
            sel_input[i + 2][:1] == '‘' and sel_input[i + 2][-1] == '’') and \
            sel_input[i + 3] == "order" and sel_input[i + 4] == "by" and (sel_input[i + 5] == "asc" or
                                                                          sel_input[i + 5] == "dsc"):
        controller = True

    return controller


# Operations control
def sub_control_input(inputt, int_or_str, i):
    control = False
    if int_or_str:  # for str
        if (inputt[i] == '=' or inputt[i] == '!=') and (
                inputt[i + 1][:1] == '‘' and inputt[i + 1][-1] == '’'):
            control = True

    # id/grade , operations ve string olmadığının kontrolü
    else:  # for int
        if (inputt[i] == '=' or inputt[i] == '!=' or inputt[i] == '>' or inputt[i] == '<' or inputt[i] == '<=' or
            inputt[i] == '>=' or inputt[i] == '!<' or inputt[i] == '!>') and (inputt[i + 1][:1] != "‘" and
                                                                              inputt[i + 1][-1] != "’"):
            control = True

    return control


# Controlling inputs
def control_input(my_input):
    control = False

    if my_input.lower() == "exit":
        control = True

    # "insert into students values(" and ")" controls
    elif my_input[:28].lower() == 'insert into students values(' and my_input[-1] == ')':
        insert_input = my_input[28:-1].lower().split(",")
        # True format control : example: 15000,Ali,Veli,ali.veli@spacex.com,20
        if len(insert_input) == 5:
            control = True

    # "delete from students where " control
    elif my_input[:27].lower() == "delete from students where ":
        del_input = my_input[27:].lower().split()
        # is input length 3
        if len(del_input) == 3:
            # name/lastname/email columns control
            if del_input[0] == 'name' or del_input[0] == 'lastname' or del_input[0] == 'email':
                control = sub_control_input(del_input, True, 1)

            # id/grade columns control
            elif del_input[0] == 'id' or del_input[0] == 'grade':
                control = sub_control_input(del_input, False, 1)

        # is input length 7
        elif len(del_input) == 7:
            sub_controll = False
            # name/lastname/email columns control
            if del_input[0] == 'name' or del_input[0] == 'lastname' or del_input[0] == 'email':
                sub_controll = sub_control_input(del_input, True, 1)

                # "and" and "or" control
                if (del_input[3] == 'and' or del_input[3] == 'or') and sub_controll is True:

                    # name/lastname/email columns control
                    if del_input[4] == 'name' or del_input[4] == 'lastname' or del_input[4] == 'email':
                        sub_controll = sub_control_input(del_input, True, 5)

                    # id/grade columns control
                    elif del_input[4] == 'id' or del_input[4] == 'grade':
                        sub_controll = sub_control_input(del_input, False, 5)
                    else:
                        sub_controll = False
                else:
                    sub_controll = False

            # id/grade columns control
            elif del_input[0] == 'id' or del_input[0] == 'grade':
                sub_controll = sub_control_input(del_input, False, 1)

                # "and" and "or" control
                if (del_input[3] == 'and' or del_input[3] == 'or') and sub_controll is True:

                    # name/lastname/email columns control
                    if del_input[4] == 'name' or del_input[4] == 'lastname' or del_input[4] == 'email':
                        sub_controll = sub_control_input(del_input, True, 5)

                    # id/grade columns control
                    elif del_input[4] == 'id' or del_input[4] == 'grade':
                        sub_controll = sub_control_input(del_input, False, 5)
                    else:
                        sub_controll = False
                else:
                    sub_controll = False
            control = sub_controll

    # "select " control
    elif my_input[:7].lower() == "select ":
        sel_input = my_input[7:].lower().split()
        # selected columns
        select_column_names = sel_input[0].split(',')

        length = len(select_column_names)

        # controlling selection all columns or other columns
        if 0 < length <= 5:
            select_column_control = True
            for i in select_column_names:
                if i != 'name' and i != 'lastname' and i != 'email' and i != 'grade' and i != 'id' and i != 'all':
                    select_column_control = False

            # "from", "students", "where" and length=14 control
            if (select_column_control is True) and sel_input[1] == "from" and sel_input[2] == "students" and \
                    sel_input[3] == "where" and len(sel_input) == 14:

                # id/grade columns control
                if sel_input[4] == 'id' or sel_input[4] == 'grade':
                    sub_controll = sub_control_input(sel_input, False, 5)

                    # "and - or" control
                    if (sel_input[7] == 'and' or sel_input[7] == 'or') and sub_controll is True and sel_control(
                            sel_input, 8):
                        control = True

                # name/lastname/email columns control
                if sel_input[4] == 'name' or sel_input[4] == 'lastname' or sel_input[4] == 'email':
                    sub_controll = sub_control_input(sel_input, True, 5)

                    # "and - or" control
                    if (sel_input[7] == 'and' or sel_input[7] == 'or') and sub_controll is True and sel_control(
                            sel_input, 8):
                        control = True

            # "from", "students", "where" and length=10 control
            elif (select_column_control is True) and sel_input[1] == "from" and sel_input[2] == "students" and \
                    sel_input[3] == "where" and len(sel_input) == 10 and sel_control(sel_input, 4):
                control = True

    else:
        control = False
    return control


# ###############################################################################ENTER INPUT - MAIN
def write_json(select_control):
    if select_control:
        with open('students.json', 'w') as file:# nested dict is used for json format
                json.dump({'students': [{'id': key, 'name': value[1], 'lastname': value[2], 'email': value[3],'grade': value[4]} for key, value in sorted_selected_student.items()]}, file, indent=2)
    else:
         with open('students.json', 'w') as file:# nested dict is used for json format
                json.dump({'students': [{'id': key, 'name': value[1], 'lastname': value[2], 'email': value[3],'grade': value[4]} for key, value in sorted_dict_student.items()]}, file, indent=2)

# Until the user exits, input is taken and necessary functions are called.        
def get_input():
    enter_input = ""
    control = False
    info_json = ""
    asc_or_dsc = ""
    while enter_input.lower() != "exit":
        enter_input = input(" ENTER INPUT: ")
        if control_input(enter_input):               
            inputs = enter_input.split()
            if inputs[0].lower() == "insert":
                add_student(inputs[3], control)
            elif inputs[0].lower() == "delete":
                delete_student(enter_input[26:], control)
            elif inputs[0].lower() == "select":
                info_json = inputs[1]            
                if len(inputs) == 11:
                    asc_or_dsc = inputs[10]
                    select_student(1, inputs[5], inputs[6], inputs[7], "", "", "", "")
                elif len(inputs) == 15:
                    asc_or_dsc = inputs[14]
                    select_student(2, inputs[5], inputs[6], inputs[7], inputs[8], inputs[9], inputs[10], inputs[11])
                control = True
        else:
            print(" False Input Format! ")
    if control :
        asc_dsc(asc_or_dsc)
        print_select(info_json)        
    write_json(control)


def main():
    crate_dict()
    sorted_dict()
    get_input()
    
main()

