import compiler

while True:
    text = input('basic > ')
    result, error = compiler.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)
