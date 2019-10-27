import tatsu
import pprint

def check_result(self, result):
    if result[0] == []:
        raise Exception("You missed rules!")

    if result[1] == []:
        raise Exception("You missed initial facts!")

    elif len(result[1]) > 1:
        raise Exception("You passed more than one initial facts block!")

    if result[2] == []:
        raise Exception("You missed query!")

    elif len(result[2]) > 1:
        raise Exception("You passed more than one query block!")

class Parser:

    def read_file(self, file_name):
        try:
            with open(file_name) as file:
                data = file.read()
        except:
            print('Could not open file.log')

        return data

    def compile(self, file_grammar):
        grammar = self.read_file(file_grammar)
        parser = tatsu.compile(grammar)
        return parser

    def parse(self, file_input, grammar):
        input_data = self.read_file(file_input)
        parser = self.compile(grammar)
        ast = parser.parse(input_data)

        # self.check_result(ast)

        #delete
        print('# PPRINT')
        pprint.pprint(ast, indent=2, width=20)

        return ast