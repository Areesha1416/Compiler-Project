import compiler

while True:
    text = input('basic > ')
    result, error = compiler.execute('<stdin>', text)

    if error: print(error.display_error())
    else: print(result)
