import tatsu
import enum


class Errors(enum.Enum):
   NoRules = 'No rules'
   NoQueries = 'No queries'
   NoInitFacts = 'No initial line'
   InitTooMuch = 'You need only 1 init line'
   QueryTooMuch = 'You need only 1 query line'
   CantRead = 'Cant read the file'


def error_management(result):
    if result[0] == []:
        raise Exception(Errors.NoRules.value)

    if result[1] == []:
        raise Exception(Errors.NoInitFacts.value)

    elif len(result[1]) > 1:
        raise Exception(Errors.InitTooMuch.value)

    if result[2] == []:
        raise Exception(Errors.NoQueries.value)

    elif len(result[2]) > 1:
        raise Exception(Errors.QueryTooMuch.value)


class Parser:

    def read_file(self, file_name):
        data = ''
        try:
            with open(file_name) as file:
                data = file.read()
        except:
            (Errors.CantRead.value)

        return data

    def compile(self, file_grammar):
        grammar = self.read_file(file_grammar)
        parser = tatsu.compile(grammar)
        return parser

    def parse(self, file_input, grammar):
        input_data = self.read_file(file_input)
        parser = self.compile(grammar)
        ast = parser.parse(input_data)

        error_management(ast)

        return ast
