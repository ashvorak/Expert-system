import sys
from parser import Parser

GRAMMAR = 'rules_to_parse.peg'

class ExpertSystem:
    def __init__(self):
        self.parser = Parser()
        self.rules = None
        self.trues = None
        self.search = None
        self.knowledge_base = None

    def parse_file(self, file):
        parser_output = self.parser.parse(file, GRAMMAR)

        if parser_output is None:
            exit('Something wrong with file!')

        if parser_output != 'empty':
            self.rules = parser_output[0]
            self.trues = parser_output[1][0]
            self.search = parser_output[2][0]

        else:
            exit('Wrong file content or file is empty!')

    def Run(self, file):
        self.parse_file(file)


def main():
    try:
        if len(sys.argv) == 1:
            exit('There is no input arguments! Type -h argument to read help for this program!')

    except Exception:
        print('Error')

    ExpertSystem().Run(sys.argv[1])


if __name__ == '__main__':
    main()
