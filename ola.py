

string = "asdasdasdasdasdasda0s"

'''checked = False


for caracter in string:
    if caracter == "0":
        checked = True


if checked:
    print("tem 0!")
else:
    print("nao tem 0!")'''


if any([caracter == "0" for caracter in string]):
    print("tem 0!")
else:
    print("nao tem 0!")