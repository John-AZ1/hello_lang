import re

def debug(variables):
    for var in variables:
        print(var)

class token:
    def __init__(self, token_type):
        self.token_type = token_type
        self.data = {}
    def append_data(self, key, data):
        self.data[key] = data
    def edit_data(self, key, data):
        self.append_data(key, data)

def parse_params(params_string, seperator=','):
    pattern = re.compile('([^{}]*)'.format(seperator))
    unclean_params = pattern.findall(params_string)
    params = []
    for param in unclean_params:
        if param is '':
            continue
        else:
            params.append(param.strip())
    return(params)

def open_file(file):
    return(open(file, 'r').read())

def lex(data, var='CODE'):
    tokens = []
    current_tok = ''
    for char in data:
        if char is '\n':
            continue
        elif char is '(':
            tokens.append(token('FUNCTION'))
            tokens[-1].append_data('name', current_tok)
            current_tok = ''
        elif char is ')':
            params = parse_params(current_tok)
            tokens[-1].append_data('parameters', params)
            current_tok = ''
        else:
            current_tok += char
    
    # for tok in tokens:
        # debug(['{}:{} PARAMETERS:{}'.format(
        #     tok.token_type,
        #     tok.data['name'],
        #     tok.data['parameters']
        # )])
    # debug(['Lex Output: ',tokens])
    return(tokens)

def parse(tokens):
    parsed_data = ''
    # debug(['Parse Input: ', tokens])
    for token in tokens:
        # debug([token])
        if token.token_type is 'FUNCTION':
            parsed_data += '{}({})'.format(
                token.data['name'],
                '{}'.format(*token.data['parameters'])
            )
    return(parsed_data)
    debug([parsed_data])

def write_file(contents):
    file_ob = open('example.py', 'w')
    file_ob.write(contents)

def run():
    data = open_file('example.hlang')
    tokens = lex(data)
    file_contents = parse(tokens)
    write_file(file_contents)

run()
