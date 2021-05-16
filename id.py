import re


# Functions to create id's
def s_id(inp):
    x_id = f'S{inp}'
    return x_id


def ip_id(inp):
    x_id = f'IP{id_int(inp)}'
    return f'{inp}_{x_id}'


def c_id(inp):
    x_id = f'C{inp}'
    return x_id


def p_id(inp):
    x_id = f'P{inp}'
    return x_id


# Functions to convert one id to another
def id_conv(new, number):
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
    return cut_id_x[-1]


# Function to decode an id
def decoder_1(inp):
    output_1 = inp.split("_")
    cut_id_list = []
    for id_x in output_1:
        cut_id_x = re.findall('(\d+|[A-Za-z]+)', id_x)
        cut_id_list.append(cut_id_x)
    final_list = []
    for id_x in cut_id_list:
        inside_list = []
        if id_x[0] == 'S':
            inside_list.append('Story N.')
            inside_list.append(id_x[1])
        if id_x[0] == 'IP':
            inside_list.append('Initial Paragraph')
        if id_x[0] == 'C':
            inside_list.append('Choice N.')
            inside_list.append(id_x[1])
        if id_x[0] == 'P':
            inside_list.append('Paragraph N.')
            inside_list.append(id_x[1])
        final_list.append(inside_list)
    return final_list


def decoder_2(inp):
    output_1 = inp.split("_")
    return output_1


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
        final_text += '\n'
        for item in lt:
            final_text += f'{item}'

    return final_text


