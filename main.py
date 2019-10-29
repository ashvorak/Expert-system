import sys
from parser import Parser

GRAMMAR = 'rules_to_parse2.peg'


class Expert:
    def __init__(self):
        self.parser = Parser()
        self.rules = None
        self.trues = None
        self.search = None
        self.knowledge_base = None
        self.results = []

    def check_right_part(self, rules):
        result = list()
        for rule in rules:
            if isinstance(rule[-1], list):
                value = rule[:-1]
                parts = ''.join(rule[-1]).split('+')
                for part in parts:
                    result.append(value + list(part))
            else:
                result.append(rule)
        return result

    def convert_rules(self, rules):
        tmp = dict()
        rules = self.check_right_part(rules)
        for rule in rules:
            if isinstance(rule[-1], list):
                fact = ''.join(rule[-1])
            else:
                fact = rule[-1]
            if tmp.get(fact):
                value = tmp[fact]
                tmp[fact] = [list(value), list(rule[:-2])]
            else:
                tmp[fact] = rule[:-2]

        return tmp

    def parse_file(self, file):
        parser_output = self.parser.parse(file, GRAMMAR)

        if parser_output is None:
            exit('Something wrong with file!')

        if parser_output != 'empty':
            self.rules = self.convert_rules(parser_output[0])
            self.trues = parser_output[1][0]
            self.search = parser_output[2][0]

        else:
            exit('Wrong file content or file is empty!')

    def run(self, file):
        self.parse_file(file)
        # for rule in self.rules:
        print(self.rules)

        print(self.trues)
        print(self.search)
        res = create_classes(self.rules)

        for item in self.search:
            if item in self.trues:
                print(f'{item} in trues = True')
            elif res.get(item):
                if isinstance(res[item], list) and len(res[item]) > 1 and \
                        all([True if not isinstance(i, str) else False for i in res[item]]):
                    for i in res[item]:
                        fact = i.calculate(self.trues, res)
                        if fact:
                            break
                else:
                    fact = res[item].calculate(self.trues, res)
                print(f'{item} in calculation = {fact}')
            else:
                print(f'{item} in else = False')

    #
    # for item in self.search:
    #     for rule in self.rules.keys():
    #         if rule.get(item):
    #             pass
    # self.calculate(rule[item])

    #
    # def calculate(self):
    #     for item in self.search:
    #         for rule in self.rules:


def check_negative_elem(elem):
    if len(elem) > 1 and elem[0] == '!':
        return Not(Element(elem[1]))
    return Element(elem)


def recursive(elem):
    if not isinstance(elem, list):
        return check_negative_elem(elem)
    elif len(elem) == 1:
        return check_negative_elem(elem[0])
    if elem[1] == '+':
        return And(recursive(elem[0]), recursive(elem[2]))
    elif elem[1] == '|':
        return Or(recursive(elem[0]), recursive(elem[2]))
    elif elem[1] == '^':
        return Xor(recursive(elem[0]), recursive(elem[2]))
    else:
        data = []
        for el in elem:
            data.append(recursive(el))
        return data


def create_classes(rules):
    converted_rules = dict()
    for key, rule in rules.items():
        if len(key) > 1 and key[0] == '!':
            converted_rules[key[1]] = Not(recursive(rule))
        else:
            converted_rules[key] = recursive(rule)
    return converted_rules


class Element:

    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return self.element.__repr__()

    def __str__(self):
        return self.element.__str__()

    def calculate(self, trues, res):
        if self.element in trues:
            return True
        elif res.get(self.element):
            return res[self.element].calculate(trues, res)
        else:
            return False


class And:

    def __init__(self, left, right):
        self.left = left
        self.left_bool = False
        self.right = right
        self.right_bool = False

    def __repr__(self):
        return f'{self.left.__repr__()} + {self.right.__repr__()}'

    #
    # def define_bool(self):
    #     if self.left.element in self.trues:
    #         self.left_bool =

    def calculate(self, trues, res):
        return self.left.calculate(trues, res) and self.right.calculate(trues, res)


class Or:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{self.left.__repr__()} | {self.right.__repr__()}'

    def calculate(self, trues, res):
        return self.left.calculate(trues, res) or self.right.calculate(trues, res)


class Xor:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'{self.left.__repr__()} ^ {self.right.__repr__()}'

    def calculate(self, trues, res):
        return self.left.calculate(trues, res) != self.right.calculate(trues, res)


class Not:
    def __init__(self, element):
        self.element = element

    def __repr__(self):
        return f'!{self.element.__repr__()}'

    def calculate(self, trues, res):
        if self.element.element in trues:
            res = True
        elif res.get(self.element.element):
            res = res[self.element.element].calculate(trues, res)
        else:
            res = False
        return not res


def main():
    try:
        if len(sys.argv) == 1:
            exit('There is no input arguments! Type -h argument to read help for this program!')

    except Exception:
        print('Error')

    Expert().run(sys.argv[1])


if __name__ == '__main__':
    main()
