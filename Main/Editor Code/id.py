import re


# Functions to create id's
def s_id(inp):
    x_id = f'S{inp}'
    return x_id


def ip_id(inp):
    x_id = 'IP'
    return f'{inp}_{x_id}'


def c_id(inp):
    x_id = f'C{inp}'
    return x_id


def p_id(inp):
    x_id = f'P{inp}'
    return x_id


def ch_id(inp):
    x_id = f'CH{inp}'
    return x_id


def npc_id(inp):
    x_id = f'NPC{inp}'
    return x_id


def mst_id(inp):
    x_id = f'MST{inp}'
    return x_id


def obj_id(inp):
    x_id = f'OBJ{inp}'
    return x_id


def con_id(inp):
    x_id = f'CON{inp}'
    return x_id


# Functions to convert one id to another
def conv(new, number):
    x_id_dict = {
        "s_id": 'S',
        "ip_id": 'IP',
        "p_id": 'P',
        "c_id":  'C'
    }
    letter = x_id_dict.get(new)
    return f'{letter}{number}'


# Function to retrieve the number from an id
def id_int(inp):
    cut_id_x = re.findall('(\d+|[A-Za-z]+)', inp)
    if cut_id_x[-1] == 'IP':
        return 0
    else:
        return cut_id_x[-1]


# Decoder to return a list of str of an ID
def decoder_1(inp):
    output_1 = inp.split("_")
    cut_id_list = []
    final_list = []
    for id_x in output_1:
        cut_id_x = re.findall('(\d+|[A-Za-z]+)', id_x)
        cut_id_list.append(cut_id_x)

    for id_x in cut_id_list:
        inside_list = []

        if id_x == cut_id_list[1]:
            position = 'from'
        else:
            position = 'to'

        if id_x[0] == 'S':
            inside_list.append('In Story N.')
            inside_list.append(id_x[1])
        if id_x[0] == 'IP':
            inside_list.append('From Initial Paragraph')
        if id_x[0] == 'C':
            inside_list.append('Choice N.')
            inside_list.append(id_x[1])

        if id_x[0] == 'P' and position == 'from':
            inside_list.append('From Paragraph N.')
            inside_list.append(id_x[1])
        if id_x[0] == 'P' and position == 'to':
            inside_list.append('To Paragraph N.')
            inside_list.append(id_x[1])
        final_list.append(inside_list)
    return final_list


# Decoder to split ID
def decoder_2(inp):
    output_1 = inp.split("_")
    return output_1


# Decoder to input str text of ID
def decoder_3(inp):
    raw_code = decoder_1(inp)
    output = []
    for lt in raw_code:
        inside_list = []
        for index in range(len(lt)):
            inside_list += ([f'{lt[index]}'])
        output.append(inside_list)

    final_text = ''
    for lt in output:
        if not lt == output[0]:
            final_text += '\n'
        for item in lt:
            final_text += f'{item}'

    return final_text


def decoder_4(inp):
    output_1 = inp.split("_")
    cut_id_list = []
    final_list = []
    for id_x in output_1:
        cut_id_x = re.findall('(\d+|[A-Za-z]+)', id_x)
        cut_id_list.append(cut_id_x)

    for id_x in cut_id_list:
        inside_list = []

        if id_x[0] == 'P':
            inside_list.append('Paragraph N.')
            inside_list.append(id_x[1])

        final_list.append(inside_list)
    return final_list


# Function To Return Just Paragraph N.X
def decoder_5(inp):
    raw_code = decoder_4(inp)
    output = []
    for lt in raw_code:
        inside_list = []
        for index in range(len(lt)):
            inside_list += ([f'{lt[index]}'])
        output.append(inside_list)

    final_text = ''
    for lt in output:
        for item in lt:
            final_text += f'{item}'

    return final_text


"""print(decoder_5("S1_P1"))"""


# Decoder to return the letter of an ID
def id_str(inp):
    x_id = inp[0]
    return x_id

# Decoder to transform a str in tuple in a list into a str in a list
def raw_conv(inp):
    id_list = []
    for tp in inp:
        for item in tp:
            id_list.append(item)
    return id_list


# Functions to create looped version of a c_id
def loop_1(inp):
    original_id = decoder_2(inp)
    modified_id = f'{original_id[0]}_{original_id[3]}'
    return modified_id


def loop_2(inp):
    original_id = decoder_2(inp)
    modified_id = f'{original_id[1]}'
    return modified_id


# Function to sort the id's for the paragraph creation tab and avoiding displaying choices
# that already have a paragraph assigned to them
def c_id_sorter(inp):
    output = []
    for id_x in inp:
        if id_str(decoder_2(id_x)[-1]) == 'C':
            output.append(id_x)
    return output


"""print(c_id_sorter(['S1_IP_C1_P1', 'S1_IP_C2_P3', 'S1_IP_C3_P2', 'S1_P1_C11_P2', 'S1_P1_C12_P2', 'S1_P2_C21_P3', 'S1_P2_C31_P3', 'S1_P3_C32', 'S1_P3_C35']))"""


# Function to convert a list of id's to a list of their numbers
def int_list(inp):
    output = []
    for item in inp:
        output.append(id_int(item))
    return output


# Function to get the max number of a list
def max_num(inp):
    final_num = ''
    initial_num = 0
    for i in inp:
        if int(i) > int(initial_num):
            final_num = i
            initial_num = i
    return final_num


# Function to remove assigned paragraph from a choice
def p_del(inp):
    x_id = decoder_2(inp)
    x_id.pop(-1)
    output = ''
    for item in x_id:
        output += f'{item}_'
    output = output[:-1]
    return output


