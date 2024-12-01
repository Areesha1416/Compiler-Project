DIGIT_CHARS = '0123456789'

class CustomError:
    def __init__(self, start_position, end_position, error_title, error_details):
        self.start_position = start_position
        self.end_position = end_position
        self.error_title = error_title
        self.error_details = error_details
    
    def display_error(self):
        result  = f'{self.error_title}: {self.error_details}\n'
        result += f'File {self.start_position.file_name}, line {self.start_position.line_number + 1}'
        return result

class InvalidCharacterError(CustomError):
    def __init__(self, start_position, end_position, error_details):
        super().__init__(start_position, end_position, 'Invalid Character', error_details)


class TextPosition:
    def __init__(self, index, line_number, column_number, file_name, file_text):
        self.index = index
        self.line_number = line_number
        self.column_number = column_number
        self.file_name = file_name
        self.file_text = file_text

    def move_forward(self, current_char):
        self.index += 1
        self.column_number += 1

        if current_char == '\n':
            self.line_number += 1
            self.column_number = 0

        return self

    def clone(self):
        return TextPosition(self.index, self.line_number, self.column_number, self.file_name, self.file_text)



TOKEN_INT		= 'integer'
TOKEN_FLOAT     = 'decimal'
TOKEN_PLUS      = 'addition'
TOKEN_MINUS     = 'subtraction'
TOKEN_MULTIPLY  = 'multiplication'
TOKEN_DIVIDE    = 'division'
TOKEN_LPAREN    = 'left_parenthesis'
TOKEN_RPAREN    = 'right_parenthesis'

class Token:
    def __init__(self, token_type, token_value=None):
        self.token_type = token_type
        self.token_value = token_value
    
    def __repr__(self):
        if self.token_value: return f'{self.token_type}:{self.token_value}'
        return f'{self.token_type}'



class Tokenizer:
    def __init__(self, file_name, text_content):
        self.file_name = file_name
        self.text_content = text_content
        self.current_position = TextPosition(-1, 0, -1, file_name, text_content)
        self.active_character = None
        self.move_next()
    
    def move_next(self):
        self.current_position.move_forward(self.active_character)
        self.active_character = self.text_content[self.current_position.index] if self.current_position.index < len(self.text_content) else None

    def generate_tokens(self):
        token_list = []

        while self.active_character is not None:
            if self.active_character in ' \t':
                self.move_next()
            elif self.active_character in DIGIT_CHARS:
                token_list.append(self.construct_number())
            elif self.active_character == '+':
                token_list.append(Token(TOKEN_PLUS))
                self.move_next()
            elif self.active_character == '-':
                token_list.append(Token(TOKEN_MINUS))
                self.move_next()
            elif self.active_character == '*':
                token_list.append(Token(TOKEN_MULTIPLY))
                self.move_next()
            elif self.active_character == '/':
                token_list.append(Token(TOKEN_DIVIDE))
                self.move_next()
            elif self.active_character == '(':
                token_list.append(Token(TOKEN_LPAREN))
                self.move_next()
            elif self.active_character == ')':
                token_list.append(Token(TOKEN_RPAREN))
                self.move_next()
            else:
                start_position = self.current_position.clone()
                invalid_char = self.active_character
                self.move_next()
                return [], InvalidCharacterError(start_position, self.current_position, "'" + invalid_char + "'")

        return token_list, None

    def construct_number(self):
        number_string = ''
        decimal_count = 0

        while self.active_character is not None and self.active_character in DIGIT_CHARS + '.':
            if self.active_character == '.':
                if decimal_count == 1: break
                decimal_count += 1
                number_string += '.'
            else:
                number_string += self.active_character
            self.move_next()

        if decimal_count == 0:
            return Token(TOKEN_INT, int(number_string))
        else:
            return Token(TOKEN_FLOAT, float(number_string))

#######################################
# EXECUTION
#######################################

def execute(file_name, input_text):
    tokenizer = Tokenizer(file_name, input_text)
    token_stream, token_error = tokenizer.generate_tokens()

    return token_stream, token_error 
