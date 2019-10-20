import re
import sys
from functools import reduce

IMPLIES = '=>'
IF_AND_ONLY_IF = '<=>'
AND = '+'
OR = '|'
XOR = '^'


class Operand:

    def __init__(self, value, formula, to_find):
        self.value = value
        self.formula = formula

    def calculate(self):
        pass


def parse_data(args):
    raw_data = []
    trues = None
    to_find = None

    with open(args[0]) as f:
        for line in f:
            if not line.startswith('#'):

                line = line.replace(' ', '').rstrip('\n')

                if '#' in line:
                    line = line.split('#')[0]

                if re.match("(^[A-Za-z()!?+^|=<>\s*\t*]*)", line)[0] != line:
                    exit('Wrong data format (invalid symbols).')

                if line.startswith('?'):

                    if to_find:
                        exit('Values to find are already added.')
                    to_find = line[1:]
                    continue

                elif line.startswith('='):

                    if trues:
                        exit('True values are already added.')
                    trues = line[1:]
                    continue

                raw_data.append(line)
    return {'raw_data': raw_data, 'to_find': to_find, 'trues': trues}



# class Parser:
#
#     def __init__(self, args):
#         self.args = args
#
#
#     def parse_data(self):
#         raw_data = []
#         trues = None
#         to_find = None
#
#         with open(self.args[0]) as f:
#             for line in f:
#                 if not line.startswith('#'):
#
#                     line = line.replace(' ', '').rstrip('\n')
#
#                     if '#' in line:
#                         line = line.split('#')[0]
#
#                     if re.match("(^[A-Za-z()!?+^|=<>\s*\t*]*)", line)[0] != line:
#                         exit('Wrong data format (invalid symbols).')
#
#                     if line.startswith('?'):
#
#                         if to_find:
#                             exit('Values to find are already added.')
#                         to_find = line[1:]
#                         continue
#
#                     elif line.startswith('='):
#
#                         if trues:
#                             exit('True values are already added.')
#                         trues = line[1:]
#                         continue
#
#                     raw_data.append(line)
#         return {'raw_data': raw_data, 'to_find': to_find, 'trues': trues}


class Solver:

    def __init__(self, raw_data, to_find, trues):
        self.raw_data = raw_data
        self.to_find = to_find
        self.trues = trues
        self.knowledge_base = dict()
        self.result = dict()
        self.letters = self.get_letter()
        self.values = self.get_values()
        self.conclusions = dict()
        self.get_conclusions()
        self.get_values_for_to_find_letters()
        # self.conclusions_processing()

    def get_letter(self):
        return {i for item in self.raw_data for i in item if i.isalpha()}

    def get_values(self):
        self.knowledge_base = {letter: True for letter in self.letters if letter in self.trues}
        return {letter: True if letter in self.trues else False for letter in self.letters}

    def get_conclusions(self):
        for item in self.raw_data:
            if IF_AND_ONLY_IF in item:
                pass
                # parts = item.split(IF_AND_ONLY_IF)
                # self.conclusions.append({parts[1]: parts[0]})
                # self.conclusions.append({parts[0]: parts[1]})

            elif IMPLIES in item:
                parts = item.split(IMPLIES)
                self.conclusions[parts[1]] = parts[0]

    def operator_processing(self, value1, value2, operator):
        if operator == AND:
            return value1 and value2
        elif operator == OR:
            return value1 or value2
        elif operator == XOR:
            return value1 ^ value2
        else:
            exit('Invalid operator!!!')

    def get_letter_value(self, letter):
        if len(letter) > 1:
            return not self.values[letter[1]]
        return self.values[letter]

    def sub_rule_processing(self, letters_values, operators):
        res = letters_values[0]
        for i, operator in enumerate(operators):
            res = self.operator_processing(res, letters_values[i + 1], operator)
        return res

    # def rule_processing(self, rule):
    #     parsed_rule = re.findall(r'\(([A-Z|^+]*)\)|(!?[A-Z])|([|^+])', rule)
    #     # print(parsed_rule)
    #
    #     letters = [elem[1] if elem[1] else elem[0] for elem in parsed_rule if not elem[2]]
    #     operators = [elem[2] for elem in parsed_rule if elem[2]]
    #     letters_values = []
    #
    #     for elem in letters:
    #         if len(elem) > 2:
    #             elems = re.findall(r'(!?[A-Z])|([|^+])', elem)
    #             internal_letters = [elem[0] for i, elem in enumerate(elems) if i % 2 == 0]
    #             internal_letters_values = [self.get_letter_value(letter) for letter in internal_letters]
    #             internal_operators = [elem[1] for i, elem in enumerate(elems) if i % 2 == 1]
    #             letters_values.append(self.sub_rule_processing(internal_letters_values, internal_operators))
    #         else:
    #             letters_values.append(self.get_letter_value(elem))
    #
    #     res = self.sub_rule_processing(letters_values, operators)
    #     return res

    # def check_knowledge(self, rule):
    #     letters = re.findall(r'([A-Z])', rule)
    #     for letter in letters:
    #         if letter not in self.knowledge_base.keys():
    #             return False
    #     return True



    def get_rule_value(self, rule, left_result=None):
        parsed_rule = re.findall(r'\(([A-Z|^+]*)\)|(!?[A-Z])|([|^+])', rule)
        # print(parsed_rule)

        letters = [elem[1] if elem[1] else elem[0] for elem in parsed_rule if not elem[2]]
        operators = [elem[2] for elem in parsed_rule if elem[2]]
        letters_values = []

        for elem in letters:

            if len(elem) > 2:
                elems = re.findall(r'(!?[A-Z])|([|^+])', elem)
                internal_letters = [elem[0] for i, elem in enumerate(elems) if i % 2 == 0]
                internal_letters_values = [self.get_letter_value(letter) for letter in internal_letters]
                internal_operators = [elem[1] for i, elem in enumerate(elems) if i % 2 == 1]
                letters_values.append(self.sub_rule_processing(internal_letters_values, internal_operators))
            else:
                # self.knowledge_base[elem] = self.get_letter_value(elem)
                if len(elem) == 1 and self.knowledge_base.get(elem) != None:
                    letters_values.append(self.knowledge_base.get(elem))
                elif len(elem) == 2 and self.knowledge_base.get(elem[1]):
                    letters_values.append(not self.knowledge_base.get(elem[1]))
                elif left_result:
                    elem_value = self.get_value_for_one_letter(elem if len(elem) == 1 else elem[1], left_result)


                else:
                    elem_value = self.get_value_for_one_letter(elem if len(elem) == 1 else elem[1])
                    letters_values.append(elem_value)

        res = self.sub_rule_processing(letters_values, operators)
        return res

    def search_letter_in_keys(self, letter):
        for key in self.knowledge_base.keys():
            if letter in key:
                return key
        return None

    def get_value_for_one_letter(self, letter_to_find, left_result=None):
        if self.knowledge_base.get(letter_to_find):
            return self.knowledge_base.get(letter_to_find)
        elif self.conclusions.get(letter_to_find):
            self.knowledge_base[letter_to_find] = self.get_rule_value(self.conclusions.get(letter_to_find))
        elif self.conclusions.get('!{}'.format(letter_to_find)):
            self.knowledge_base[letter_to_find] = self.get_rule_value(self.conclusions.get('!{}'.format(letter_to_find)))
        elif left_result:
            pass
        elif self.conclusions.get(letter_to_find):
            key = search_letter_in_keys(letter_to_find)
            if key:
                left_rule_value = self.get_rule_value(key)
                self.get_rule_value(self.conclusions.get(key), left_rule_value)

            else:
                pass
        else:
            self.knowledge_base[letter_to_find] = False
        return self.knowledge_base.get(letter_to_find)

    def get_values_for_to_find_letters(self):
        result = dict()
        self.knowledge_base = {item: True for item in self.trues}
        for letter_to_find in self.to_find:
            result[letter_to_find] = self.get_value_for_one_letter(letter_to_find)

        print('Result = {}'.format(result))

    def show_info(self):
        print('Conclusions: ', self.conclusions)
        print('Letter values: ', self.values)
        print()
        print('To find: ', self.to_find)
        print('Trues: ', self.trues)


def main(*args, **kwargs):
    solver = Solver(**parse_data(args))
    solver.show_info()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('Invalid input.')
    main(sys.argv[1])
