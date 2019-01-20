import os


def get_component_count_by_project(project_id):
    with open('projects.txt', 'r', encoding='utf8') as file_ptr:
        file_string = file_ptr.read()
        file_line = file_string.split('\n')
        circuit_id_list = []
        for i in range(0, len(file_line)):
            if project_id in file_line[i]:
                circuit_id = file_line[i].split(' ')
                circuit_id_list.append(circuit_id[5])
        if not circuit_id_list:
            return None

    for i in range(0, len(circuit_id_list)):
        filename = 'circuit_' + circuit_id_list[i] + '.txt'
        with open(os.path.join('Circuits', filename), 'r', encoding='utf8') as file_ptr:
            file_string = file_ptr.read()
            return tuple(count_component(file_string))


def count_component(file_string):  # input file string and count component items and return [R, L, C, T]
    file_line = file_string.split('\n')
    component_list = file_line[4].split(',')
    component_count = [0, 0, 0, 0]    # [resistor R, inductor L, capacitor C, Transistor T]
    for i in range(0, len(component_list)):
        component = component_list[i].replace(' ', '')  # cut list of components
        if component[0] == 'R':
            component_count[0] += 1
        elif component[0] == 'L':
            component_count[1] += 1
        elif component[0] == 'C':
            component_count[2] += 1
        elif component[0] == 'T':
            component_count[3] += 1
    return component_count


def get_component_count_by_student(student_name):
    student_id = parse_student_name(student_name)[2]
    total_count = [0, 0, 0, 0]
    if student_id:
        for file in os.listdir('Circuits'):
            with open(os.path.join('Circuits', file), 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                participant_list = file_string.split('\n')[1].split(',')
                if student_id in participant_list:
                    count = count_component(file_string)
                    total_count = [x + y for x, y in zip(total_count, count)]   # sum of two lists index by index
        return tuple(total_count)
    else:
        return None


def parse_student_name(student_name):   # input 'student_name' and return [first, last, student_ID]
    with open('students.txt', 'r', encoding='utf8') as file_ptr:
        file_line = file_ptr.read().split('\n')  # extract first last names and ID
        for i in range(2, len(file_line) - 1):
            name = file_line[i].split(' ')
            first = name[1]
            student_id = name[-1]
            last = name[0].replace(',', '')
            if last in student_name and first in student_name:
                return [first, last, student_id]
    return None


def parse_student_id(given_student_id):
    with open('students.txt', 'r', encoding='utf8') as file_ptr:
        file_line = file_ptr.read().split('\n')  # extract first last names and ID
        for i in range(2, len(file_line) - 1):
            name = file_line[i].split(' ')
            first = name[1]
            student_id = name[-1]
            last = name[0].replace(',', '')
            if given_student_id == student_id:
                return first + ' ' + last
    return None


def find_all_index(ls, match):    # return all the index as a list of matched items
    return [i for i, item in enumerate(ls) if item == match]


def remove_all_match(ls, match):
    return list(filter(lambda x: x != match, ls))


def get_participation_by_student(student_name):
    student_name_id = parse_student_name(student_name)
    project_id_set = set()
    circuit_id = ''
    if not student_name_id:
        return None
    else:
        for filename in os.listdir('Circuits'):
            with open(os.path.join('Circuits', filename), 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()  # count all the stuff
                participant_list = file_string.split('\n')[1].split(',')
                if student_name_id[2] in participant_list:
                    circuit_id = filename.replace('circuit_', '').replace('.txt', '')    # extract the circuit ID

            with open('projects.txt', 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                file_line = file_string.split('\n')
                for i in range(2, len(file_line)):
                    file_line_list = file_line[i].split(' ')
                    if circuit_id in file_line_list:
                        project_id = file_line_list[-1]
                        project_id_set.add(project_id)
        return project_id_set


def get_participation_by_project(project_id):
    circuit_id_list = parse_project_id(project_id)
    participant_set = set()
    if not circuit_id_list:
        for i in range(0, len(circuit_id_list)):
            with open('Circuits/circuit_' + circuit_id_list[i] + '.txt', 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                file_line = file_string.split('\n')
                student_id_list = file_line[1].split(',')
                for j in range(0, len(student_id_list)):
                    participant_set.add(parse_student_id(student_id_list[j]))
        return participant_set
    else:
        return None


def parse_project_id(project_id):   # input project ids and output a list of circuit ids
    circuit_id_list = []
    with open('projects.txt', 'r', encoding='utf8') as file_ptr:
        file_string = file_ptr.read()
        file_line = file_string.split('\n')
        for i in range(2, len(file_line)):
            file_line_list = file_line[i].split(' ')
            circuit_project_id = remove_all_match(file_line_list, '')
            if project_id in circuit_project_id:
                circuit_id_list.append(circuit_project_id[0])
    return circuit_id_list


def parse_circuit_id(circuit_id):   # input circuit id and output project id
    with open('projects.txt', 'r', encoding='utf8') as file_ptr:
        file_string = file_ptr.read()
        file_line = file_string.split('\n')
        for i in range(2, len(file_line)):
            file_line_list = file_line[i].split(' ')
            circuit_project_id = remove_all_match(file_line_list, '')
            if circuit_id in circuit_project_id:
                return circuit_project_id[1]


def get_project_by_component(components):
    lookup_table = {}
    for i in range(0, len(components)):
        lookup_table[components[i]] = set()
        for file in os.listdir('Circuits'):
            with open('Circuits/' + file, 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                file_line = file_string.split('\n')
                component_list = file_line[4].split(',')
                for j in range(0, len(component_list)):
                    if component_list[j] in components:
                        circuit_id = file.replace('circuit_', '').replace('.txt', '')
                        project_id = parse_circuit_id(circuit_id)
                        lookup_table[components[i]].add(project_id)
    return lookup_table


def get_student_by_component(components):
    lookup_table = {}
    for i in range(0, len(components)):
        lookup_table[components[i]] = set()
        for file in os.listdir('Circuits'):
            with open('Circuits/' + file, 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                file_line = file_string.split('\n')
                component_list = file_line[4].split(',')
                for j in range(0, len(component_list)):
                    if component_list[j] in components:
                        student_id_list = file_line[1].split(',')
                        for k in range(0, len(student_id_list)):
                            student_name = parse_student_id(student_id_list[k].replace(' ', ''))
                            lookup_table[components[i]].add(student_name)
    return lookup_table


def get_component_by_student(student_names):
    lookup_table = {}
    for i in range(0, len(student_names)):
        lookup_table[student_names[i]] = set()
        student_id = parse_student_name(student_names[i])[2]
        for file in os.listdir('Circuits'):
            with open('Circuits/' + file, 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                file_line = file_string.split('\n')
                student_id_list = file_line[1].split(',')
                if student_id in student_id_list:
                    component_list = file_line[4].split(',')
                    lookup_table[student_names[i]] = lookup_table[student_names[i]].union(set(component_list))
    return lookup_table


def parse_circuit_id_get_components(circuit_id):
    with open(os.path.join('Circuits', 'circuit_' + circuit_id + '.txt'), 'r', encoding='utf8') as file_ptr:
        file_string = file_ptr.read()
        file_line = file_string.split('\n')
        component_list = file_line[4].split(',')
        for i in range(0, len(component_list)):
            component_list[i] = component_list[i].replace(' ', '')
    return component_list


def get_common_by_project(project_id1, project_id2):
    circuit_id1_list = parse_project_id(project_id1)
    circuit_id2_list = parse_project_id(project_id2)
    if circuit_id1_list == [] or circuit_id2_list == []:
        return None
    else:
        common_component_set = set()
        for i in range(0, len(circuit_id1_list)):
            component_list_1 = parse_circuit_id_get_components(circuit_id1_list[i])
            for j in range(0, len(circuit_id2_list)):
                component_list_2 = parse_circuit_id_get_components(circuit_id2_list[j])
                common_component_set = set(component_list_1).union(set(component_list_2))
        if common_component_set == set():
            return []
        else:
            common_component_list = list(common_component_set)
            common_component_list.sort(reverse=False, key=reorganize)
            return common_component_list


def reorganize(item):
    if item[0] == 'R':
        return float(item[1:])
    elif item[0] == 'L':
        return 1000 + float(item[1:])
    elif item[0] == 'C':
        return 2000 + float(item[1:])
    elif item[0] == 'T':
        return 3000 + float(item[1:])


def get_common_by_student(student_name1, student_name2):
    student_id_1 = parse_student_name(student_name1)[2]
    student_id_2 = parse_student_name(student_name2)[2]
    common_component_set = set()
    if student_id_1 and student_id_2:
        for file in os.listdir('Circuits'):
            with open('Circuits/' + file, 'r', encoding='utf8') as file_ptr:
                file_string = file_ptr.read()
                file_line = file_string.split('\n')
                student_id_list = file_line[1]
                if student_id_1 in student_id_list and student_id_2 in student_id_list:
                    component_list = file_line[4].split(',')
                    for i in range(0, len(component_list)):
                        component_list[i] = component_list[i].replace(' ', '')
                    common_component_set = common_component_set.union(set(component_list))
        common_component_list = list(common_component_set)
        common_component_list.sort(reverse=False, key=reorganize)
        return common_component_list
    else:
        return None


def get_project_by_circuit():
    lookup_table = {}
    for file in os.listdir('Circuits'):
        with open('Circuits/' + file, 'r', encoding='utf8') as file_ptr:
            circuit_id = file.replace('circuit_', '').replace('.txt', '')
            file_string = file_ptr.read()
            file_line = file_string.split('\n')
            component_list = file_line[4].split(',')
            for i in range(0, len(component_list)):
                component_list[i] = component_list[i].replace(' ', '')
            component_list.sort(reverse=False, key=reorganize)
            lookup_table[circuit_id] = component_list
    return lookup_table


def get_circuit_by_student():
    lookup_table = {}
    with open('students.txt', 'r', encoding='utf8') as file_ptr:
        file_line = file_ptr.read().split('\n')
        for i in range(2, len(file_line) - 1):
            name = file_line[i].split(' ')
            first = name[1]
            student_id = name[-1]
            last = name[0].replace(',', '')
            lookup_table[first + ' ' + last] = []
            for file in os.listdir('Circuits'):
                with open('Circuits/' + file, 'r', encoding='utf8') as file_ptr_1:
                    circuit_id = file.replace('circuit_', '').replace('.txt', '')
                    file_line_1 = file_ptr_1.read().split('\n')
                    participant_list = file_line_1[1]
                    if student_id in participant_list:
                        lookup_table[first + ' ' + last].append(circuit_id)
    for i in lookup_table:
        lookup_table[i] = sorted(lookup_table[i], key=lambda x: int(x))
    return lookup_table


def get_circuit_by_student_partial(student_name):
    lookup_table = {}
    full_lookup = get_circuit_by_student()
    with open('students.txt', 'r', encoding='utf8') as file_ptr:
        file_line = file_ptr.read().split('\n')
        for i in range(2, len(file_line) - 1):
            name = file_line[i].split(' ')
            first = name[1]
            last = name[0].replace(',', '')
            if student_name == first or student_name == last:
                lookup_table[first + ' ' + last] = full_lookup[first + ' ' + last]
    return lookup_table


if __name__ == "__main__":
    # print(get_component_count_by_student('Amanda Allen'))
    # print(get_component_count_by_project('082D6241-40EE-432E-A635-65EA8AA374B6'))
    # print(parse_student_name('Adams, Keith '))
    # print(get_participation_by_student('Keith Adams'))
    # print(parse_project_id('082D6241-40EE-432E-A635-65EA8AA374B6'))
    # print(get_participation_by_project('082D6241-40EE-432E-A635-65EA8AA374B6'))
    # get_project_by_component(2)
    # print(parse_circuit_id('15565'))
    # s = ('L341.064', 'R15.503', 'C471.636', 'R227.524', 'L104.513', 'C108.908', 'C447.493')
    # a = get_project_by_component(s)
    # s = ('Keith Adams', 'Amanda Allen')
    # a = get_component_by_student(s)
    # print(get_common_by_project('082D6241-40EE-432E-A635-65EA8AA374B6', '90BE0D09-1438-414A-A38B-8309A49C02EF'))
    # print(parse_student_id('06139-33248'))
    # print(parse_circuit_id_get_components('15565'))
    # print(reorganize('T291.176'))
    # print(reorganize('T426.533'))
    # print(get_common_by_student('Watson, Martin', 'Washington, Annie'))
    # print(get_project_by_circuit())
    # print(get_circuit_by_student())
    # print(get_circuit_by_student_partial('Kelly'))
    pass
