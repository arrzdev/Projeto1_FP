
# -- Correção de documentação -- #

def corrigir_palavra(segment: str): 
    #This function clean the bugs that are in a segment of caracters..

    letter_index = 0

    while letter_index < len(segment):
        #the current letter that we are checking
        current_letter = segment[letter_index]

        #the letter that need to be next so that we have the pattern
        if current_letter.islower():
            next_pattern_letter = current_letter.upper()
        else:
            next_pattern_letter = current_letter.lower()
    
        #if we are not checking the last letter and if the next letter is the one that we need to have a "pattern"
        if letter_index != len(segment)-1 and segment[letter_index+1] == next_pattern_letter:
            segment = segment.replace(current_letter+next_pattern_letter, "")

            #if we have removed a "pattern" we go back 1 in the index so we can test the letter before that can now have a pattern based on the modification that we just did
            if letter_index >= 1:
                letter_index -= 1
        else: #keep searching forward if we don't remove any thing
            letter_index += 1

    return segment

def eh_anagrama(segment1: str, segment2: str):
    #This function returns True or False based on the segment1 and the segment2 being anagrams or not

    #the sorted method creates a list with ordenated caracters

    res = sorted(segment1.lower()) == sorted(segment2.lower())

    return res

def corrigir_doc(string: str):
    #This function receives the documentation and clean it removing the bugs

    #string check
    if type(string) == str:
        #create a list containing the bugged bugged_segments
        bugged_segments = string.split()

        #spaces check
        if string.count("  ") > 0:
            raise ValueError("corrigir_doc: argumento invalido")
            
        #at least 1 letter and only letterns in each segment check
        for bugged_segment in bugged_segments:
            for caracter in bugged_segment:
                if not caracter.isalpha():
                    raise ValueError("corrigir_doc: argumento invalido")
    else:
        raise ValueError("corrigir_doc: argumento invalido")


    #initialize an empty list where we are going to save our clean segments
    clean_segments = []

    #loop throught the bugged segments
    for bugged_segment in bugged_segments:

        #call the function that clean the "bugged" segment
        clean_current_segment = corrigir_palavra(bugged_segment)

        if not any([eh_anagrama(clean_segment, clean_current_segment) and clean_segment.lower() != clean_current_segment.lower() for clean_segment in clean_segments]):
            clean_segments.append(clean_current_segment)

        '''#initialize anagram check boolean
        any_anagram = False

        #loop throught the clean segments and make the anagram verify
        for clean_segment in clean_segments:

            #if the current clean_segment is an anagram of any already saved clean segment and they have not the same caracter order change anagram_check to True
            if eh_anagrama(clean_segment, clean_current_segment) and clean_segment != clean_current_segment:
                any_anagram = True

        #append the recently cleaned segment to the list if it isn't an anagram of any of the previous saved cleaned segments
        if not any_anagram:
            clean_segments.append(clean_current_segment)
        '''

    #join the segments and build the cleaned string
    cleaned_string = " ".join(clean_segments)

    return cleaned_string

#--------------------------------#


# -- Descoberta do PIN -- #

def obter_posicao(movement: str, position: int):
    
    C_limit = (1,2,3)
    B_limit = (7,8,9)
    E_limit = (1,4,7)
    D_limit = (3,6,9)

    #CBED
     
    if movement == "C" and position not in C_limit:
        new_position = position - 3
    elif movement == "B" and position not in B_limit:
        new_position = position + 3
    elif movement == "E" and position not in E_limit:
        new_position = position - 1
    elif movement == "D" and position not in D_limit:
        new_position = position + 1
    else:
        new_position = position

    return new_position

def obter_digito(sequence: str, position: int):
    for movement in sequence:
        position = obter_posicao(movement, position)

    return position

def obter_pin(sequences: tuple):

    #check type and lenght of the argument "sequences"
    if type(sequences) != tuple or len(sequences) < 4 or len(sequences) > 10:
        raise ValueError("obter_pin: argumento invalido")
    
    valid_movements = ("C","B","E","D")

    #check if the input follow every rule... (CBDE)
    for sequence in sequences:
        if sequence == "":
            raise ValueError("obter_pin: argumento invalido")
        else:
            for movement in sequence:
                if movement not in valid_movements:
                    raise ValueError("obter_pin: argumento invalido")

    #initialize an empty tuple to save the pin
    pin = ()

    #initialize the position variable with 5 (middle)
    position = 5

    #loop through the sequence
    for sequence in sequences:
        #update the position with the new position
        position = obter_digito(sequence, position)

        #create a tuple containing the digito 
        digito = (position,)

        #concatenate the two tuples
        pin += digito

    #return the pin
    return pin

#-------------------------#


# -- Verificação de dados -- #

def eh_entrada(entrada: tuple):
    if type(entrada) != tuple or len(entrada) != 3:
        return False

    #initialize variables
    cifra = entrada[0]
    checksum = entrada[1]
    tuplo = entrada[2]

    #check types of the variables
    if type(cifra) != str or type(checksum) != str or type(tuplo) != tuple:
        return False

    #get the segments of the cifra that we will use for the tests
    segments = cifra.split("-")

    #cifra alpha and low case check 
    for segment in segments:
        if segment == "":
            return False

        for letter in segment:
            if not letter.isalpha() or not letter.islower():
                return False

    #check lenght and format of checksum
    if len(checksum) != 7 or checksum[0] != "[" or checksum[-1] != "]":
        return False

    #checksum alpha and low case check
    for letter in checksum[1:-1]:
        if not letter.isalpha() or not letter.islower():
            return False

    #tuplo check
    if type(tuplo) == tuple and len(tuplo) >= 2:
        for elemento in tuplo:
            if type(elemento) != int or elemento < 0:
                return False
    else:
        return False

    #otherwise
    return True 

def validar_cifra(cifra:str, checksum:str):
    
    control = checksum[1:-1]
    joined_cifra = cifra.replace("-", "")

    ordered = []

    #we want the 5 letters that are the most common and undraw by alphabetic order
    for _ in range(5):
        #start by defining a list that contains on the index 0 the best letter and on the index 1 the number of times that the letter appeared
        best = ["", 0]
        for letter in joined_cifra:

            #number of times the letter we are testing appear on the string
            letter_count = joined_cifra.count(letter)
            
            if letter_count > best[1]:
                best = [letter, letter_count]
            elif letter_count == best[1]:
                if ord(letter) < ord(best[0]):
                    best = [letter, letter_count]

        #add to the list the best caracter
        ordered.append(best[0])

        #remove the caracter that we just added from the strings
        joined_cifra = joined_cifra.replace(best[0], "")


    #check if the control list correspond to the best order list and return boolean
    result = list(control) == ordered 

    return result


def filtrar_bdb(entradas: list):

    if type(entradas) != list or len(entradas) < 1:
        raise ValueError("filtrar_bdb: argumento invalido")

    #is this supposed to be here?
    for entrada in entradas:
        if not eh_entrada(entrada):
            raise ValueError("filtrar_bdb: argumento invalido")

    #define the filter function
    def filter_funct(entrada):

        #validar_cifra will return True if the cifra is correct but because we want the ones that are not correct we need to "change" the boolean so the filter function returns True if the cifra is not valid
        res = not validar_cifra(entrada[0], entrada[1])

        return res

    filtered_list = list(filter(filter_funct, entradas))

    return filtered_list

#----------------------------#


# -- Desencriptação de dados -- #

def obter_num_seguranca(tuplo: tuple):
    security_number = float("+inf")

    for index, number in enumerate(tuplo):
        for sub_index, sub_number in enumerate(tuplo):

            #we dont want to subtract the same number with him self
            if index == sub_index:
                continue

            #using modulo to get always the subtraction that gives us the positive number
            possible_security = abs(number - sub_number)

            #update security number in case the recent calculated one is lower
            if possible_security < security_number:
                security_number = possible_security
             
    return security_number

def decifrar_texto(cifra: str, security: int):

    caracter_list = list(cifra)

    for index_caracter, caracter in enumerate(cifra):
        if caracter == "-":
            continue

        #convert the letter to a number and subtract 96 to get a (1 to 26) order
        alphabet_number = ord(caracter) - 96 

        #if the caracter is in a even index in the string add 1 otherwise subtract 1
        if index_caracter % 2 == 0:
            alphabet_number += 1
        else:
            alphabet_number -= 1

        #add security code
        alphabet_number += security

        #get the number to the interval 1-26
        alphabet_number %= 26

        #add 96 to get the alphabet number to the correct utf8 and then convert back to the correspondent letter
        new_caracter = chr(alphabet_number + 96)

        #update the caracter in the list
        caracter_list[index_caracter] = new_caracter

    #join the caracters of the list again and then replace the "-" with a white space
    final_string = "".join(caracter_list).replace("-", " ")

    return final_string

def decifrar_bdb(entradas: list):
    if type(entradas) != list or len(entradas) < 1: 
        raise ValueError("decifrar_bdb: argumento invalido")

    #check if we have only entries
    for possible_entrada in entradas:
        if not eh_entrada(possible_entrada):
            raise ValueError("decifrar_bdb: argumento invalido")

    #initialize decrypted list where we are going to save our decrypted entries
    decrypted_list = []

    for entrada in entradas:
        cifra = entrada[0]
        controlo = entrada[1]
        security_segment = entrada[2]

        security_code = obter_num_seguranca(security_segment)

        decrypted_list.append(decifrar_texto(cifra, security_code))


    return decrypted_list

#-------------------------------#


# -- Depuração de senhas -- #

def eh_utilizador(dictionary: dict):

    #verify the type of the argument
    if type(dictionary) != dict or len(dictionary) != 3: 
        return False

    #verify if we have all the keys
    try:
        name = dictionary["name"]
        passw = dictionary["pass"]
        vals = dictionary["rule"]["vals"]
        char = dictionary["rule"]["char"]
    except:
        return False
    
    
    #verify's

    #name and passwrd check
    if len(name) < 1 or len(passw) < 1:
        return False
    
    #char check
    if len(char) != 1 or not char.isalpha():
        return False

    #vals check
    if type(vals) != tuple or len(vals) != 2 or type(vals[0]) != int or type(vals[1]) != int or vals[0] > vals[1]:
        return False
    
    #else
    return True

def eh_senha_valida(password: str, rule: dict):
    #gerais

    vowels = ["a", "e", "i", "o", "u"]

    #initialize variable that stores the number of vowels that are present in the password
    vowels_number = 0

    #initialize variable that stores a boolean corresponding to the result of the sequence rule pass
    sequence_check = False

    #loop through the caracters
    for caracter in password:
        #count the vowels
        if caracter.islower() and caracter in vowels:
            vowels_number += 1

        #check if the caracter appears twice or more in a row int the password
        if password.count(caracter*2) > 0:
            sequence_check = True

    #if the password did not pass the general return False, otherwise continue to individual checks
    if vowels_number < 3 or not sequence_check:
        return False


    #define individual variables
    individual_caracter = rule["char"]
    individual_min = rule["vals"][0]
    individual_max = rule["vals"][1]

    #actually check if we passed the individual rules
    if individual_max >= password.count(individual_caracter) >= individual_min:
        return True
    else:
        return False 

def filtrar_senhas(lista: list):
    if type(lista) != list or len(lista) < 1:
        raise ValueError("filtrar_senhas: argumento invalido")

    #check if we have any wrong dictionary in this list
    for dictionary in lista:
        if not eh_utilizador(dictionary):
            raise ValueError("filtrar_senhas: argumento invalido")
    

    def filter_funct(dictionary):
        #we want the dictionarys that have wrong passwords so return True when the passwords are wrong, return False otherwise
        if not eh_senha_valida(dictionary["pass"], dictionary["rule"]):
            return True
        else:
            return False

    def map_funct(dictionary):
        return dictionary["name"]

    #here we have only the dictionaries that are "wrong"
    filtered_dictionaries = list(filter(filter_funct, lista))

    #get only the names present on that dictionaries
    names = list(map(map_funct, filtered_dictionaries))

    #ordenate the names by alphabetic order
    ordenated_names = sorted(names)

    return ordenated_names

    
#---------------------------#