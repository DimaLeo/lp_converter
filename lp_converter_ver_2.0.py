import numpy as np
import re


# function that reads the file and exports each line to 1 list item
def read_file():
    input_file = open('lp.txt', 'r')
    file_container_arr = []

    for line in input_file.readlines():
        file_container_arr.append(line)

    input_file.close()

    return file_container_arr


# function that cleans up unnecessary spaces and blank lines from the input file
def cleanup_input_data(data_array):
    temp_array = []
    for line in data_array:
        if line != '\n':
            clean_line = ''.join(re.split('[/ *]', line))
            clean_line = clean_line.rstrip('\n')
            clean_line = clean_line.rstrip(',')
            temp_array.append(clean_line)

    return temp_array


# function that check if the problem is correctly written using regular expressions
def check_problem_validity(problem_arr):
    obj_fn_regex = re.compile('^[\+\-]?(\d*x\d\d*)([\+\-]\d*x\d\d*)*$')
    subject_to_regex = re.compile('(subject\ to)|(s{1}\.t{1}\.)|(st)')
    constraints_regex = re.compile('^[\+\-]?(\d*x\d\d*)([\+\-]\d*x\d\d*)*((>=)|(<=)|(=))([\+\-]?\d\d*)$')

    minmax_arr = ['min', 'max', 'Min', 'Max']
    signs_arr = ['+', '-']
    equality_arr = ['=', '<=', '>=']

    line_counter = 0

    valid_elements_arr = []
    if problem_arr[len(problem_arr) - 1] == 'end':
        problem_arr.remove('end')
    else:
        raise Exception('Problem end error: No end string was found at the end of the file')

    for line in problem_arr:
        if line_counter == 0:
            minmax = line[:3]
            if minmax not in minmax_arr:
                raise Exception('Problem declaration format error: given function does not start with min or max\n' +
                                'make sure the first line of the input file starts with  min/max z= ...\n' +
                                'program exiting ...')

            if minmax == 'min':
                valid_elements_arr.append('-1')
            elif minmax == 'max':
                valid_elements_arr.append('1')

            objective_fn = line[3:].lstrip('z=')

            if not re.match(obj_fn_regex, objective_fn):
                raise Exception('Objective function format error: objective function elements should be\n' +
                                'followed by + or -. First variable can start with + or -\n' +
                                'Example : 2x1+3x2+4x3+5x4\n' + 'program exiting ...')
            valid_elements_arr.append(objective_fn)
        elif line_counter == 1:
            if not re.match(subject_to_regex, line):
                raise Exception('ST line error: 2nd line of the input file must contain the characters st, s.t.\n' +
                                ' or the phrase \'subject to\'\n program exiting ...')
        else:
            if not re.match(constraints_regex, line):
                raise Exception('Constraint format error: Constraint no.' + str(line_counter - 1) +
                                ' of the input file is not written correctly.\n' +
                                'make sure it is in the correct format eg. 2x1+3x2+4x3<=7\n' +
                                'program exiting ...')
            valid_elements_arr.append(line)

        line_counter += 1

    return valid_elements_arr


def extract_coefficient(function):
    coefficient_list = []

    for item in function:
        if item == '+' or item == '':
            coefficient_list.append('1')
        elif item == '-':
            coefficient_list.append('-1')
        elif re.match('\+\d\d*', item):
            coefficient_list.append(item.lstrip('+'))
        else:
            coefficient_list.append(item)

    return coefficient_list


def write_output_file(MinMax, c, A, b, Eqin):
    # make arrays numpy arrays
    Eqin = np.array(Eqin)[:, np.newaxis]
    # print(Eqin)
    # print('\n')
    b = np.array(b)[:, np.newaxis]
    # print(b)
    # print('\n')
    A = np.array(A)
    # print(A)
    c = np.array(c)
    # print(c)

    lp_out = open('lp_2.txt', 'w')
    """
    write file using numpy prints
    lp_out.write(str(MinMax)+'\n')
    lp_out.write('\n')
    lp_out.write('c = '+np.array2string(c))
    lp_out.write('\n')
    lp_out.write('A = '+np.array2string(A))
    lp_out.write('\n')
    lp_out.write('b = '+np.array2string(b))
    lp_out.write('\n')
    lp_out.write('Eqin = '+np.array2string(Eqin))
    """
    # writing file so that it looks like given example

    lp_out.write(str(MinMax) + '\n')
    lp_out.write('\n')
    # Write c transpose
    lp_out.write('c = [')
    i = 0
    for c_val in c:
        if i == len(c) - 1:
            lp_out.write(c_val + ']\n')
        else:
            lp_out.write(c_val + '\n')
        i += 1
    lp_out.write('\n')

    # Write A
    y = 0
    lp_out.write('A = [')
    for line in A:
        x = 0
        for a_val in line:
            if x == len(line) - 1:
                if y == len(A) - 1:
                    lp_out.write(a_val + ']\n')
                else:
                    lp_out.write(a_val + '\n')
            else:
                lp_out.write(a_val + ' ')
            x += 1
        y += 1
    lp_out.write('\n')

    # Write b
    lp_out.write('b = [')
    i = 0
    for b_val in b:
        if i == len(b) - 1:
            lp_out.write(b_val[0] + ']\n')
        else:
            lp_out.write(b_val[0] + '\n')
        i += 1
    lp_out.write('\n')

    # Write Eqin
    lp_out.write('Eqin = [')
    i = 0
    for e_val in Eqin:
        if i == len(Eqin) - 1:
            lp_out.write(e_val[0] + ']\n')
        else:
            lp_out.write(e_val[0] + '\n')
        i += 1
    lp_out.write('\n')

    lp_out.close()


def main():
    A = []
    b = []
    c = []
    Eqin = []
    MinMax = 0

    file_data_arr = []
    file_data_arr = read_file()

    problem_arr = []
    problem_arr = cleanup_input_data(file_data_arr)

    post_validation_data = []
    post_validation_data = check_problem_validity(problem_arr)

    # assign the type of the problem -- always in the first slot of the list
    MinMax = post_validation_data[0]

    objective_function = post_validation_data[1]
    objective_function = re.split('x\d\d*', objective_function)[:-1]

    no_of_vars = len(objective_function)
    # print(no_of_vars)

    # extract values for c array from objective function
    c = extract_coefficient(objective_function)

    # extract values for A array from constraints
    for const in post_validation_data[2:]:
        temp = []
        if re.match('([\+\-]?x\d*\=\d*)', const):
            adjusted_const = [None] * no_of_vars
            position = int(const[:-2].lstrip('x')) - 1
            adjusted_const[position] = re.split('x\d\d*', const)[0]
            temp = adjusted_const

            counter = 0
            for item in temp:
                if item is None:
                    temp[counter] = '0'
                counter += 1

            A.append(extract_coefficient(temp))

        else:
            temp = re.split('x\d\d*', const)
            A.append(extract_coefficient(temp[:-1]))

        b_str = re.split('>=|<=|=', const)
        b.append(b_str[len(b_str) - 1])

        try:
            found = re.search('((>=)|(<=)|(=))', const).group(1)
            if found == '=':
                Eqin.append('0')
            elif found == '>=':
                Eqin.append('1')
            elif found == '<=':
                Eqin.append('-1')

        except AttributeError:
            # equation sign not found
            found = ''  # apply your error handling
    """
    print('c = ')
    print(c)
    print('\n')
    print('A = ')
    print(A)
    print('\n')
    print('b = ')
    print(b)
    print('\n')
    print('Eqin = ')
    print(Eqin)
    print('\n')
    """

    write_output_file(MinMax, c, A, b, Eqin)


main()
