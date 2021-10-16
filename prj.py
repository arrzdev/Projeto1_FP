
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
            
            #if we have removed a "pattern" we go back to the beggining and start searching from the beggining
            letter_index = 0
        else: #keep searching forward if we don't remove any thing
            letter_index += 1
    return segment
 
def eh_anagrama(segment1: str, segment2: str):
    #This function returns True or False based on the segment1 and the segment2 being anagrams or not

    #the sorted method creates a list with ordenated caracters
    return sorted(segment1.lower()) == sorted(segment2.lower())

def corrigir_doc(string: str):
    #This function receives the documentation and clean it removing the bugs

    #string check
    if type(string) == str:
        #create a list containing the bugged bugged_segments
        bugged_segments = string.split()

        #spaces check
        if string.count(" ") != len(bugged_segments)-1:
            raise ValueError("corrigir_doc: argumento invalido")
            
        #at least 1 letter and only letterns in each segment check
        for bugged_segment in bugged_segments:
            for caracter in bugged_segment:
                if not caracter.isalpha():
                    raise ValueError("corrigir_doc: argumento invalido")

            #check if the segment has at least 1 letter
            '''
            for caracter in segment:
                if caracter.isalpha():
                    has_letter = True
                    break
            '''
    else:
        raise ValueError("corrigir_doc: argumento invalido")


    #initialize an empty list where we are going to save our clean segments
    clean_segments = []

    #loop throught the bugged segments
    for bugged_segment in bugged_segments:

        #call the function that clean the "bugged" segment
        clean_current_segment = corrigir_palavra(bugged_segment)
        
        #initialize anagram check boolean
        any_anagram = False

        #loop throught the clean segments and make the anagram verify
        for clean_segment in clean_segments:

            #if the current clean_segment is an anagram of any already saved clean segment and they have not the same caracter order change anagram_check to True
            if eh_anagrama(clean_segment, clean_current_segment) and clean_segment != clean_current_segment:
                any_anagram = True

        #append the recently cleaned segment to the list if it isn't an anagram of any of the previous saved cleaned segments
        if not any_anagram:
            clean_segments.append(clean_current_segment)


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
    if type(sequences) != tuple or (10 < len(sequences) < 4):
        raise ValueError("obter_pin: argumento invalido")
    
    valid_movements = ("C","B","E","D")

    #check if the input follow every rule... (CBDE)
    for sequence in sequences:
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
    if type(entrada) == tuple:

        cifra = entrada[0]
        checksum = entrada[1]
        tuplo = entrada[2]

        #cifra check
        for segmento in cifra.split("-"):            
            #in case we had two sequencial "-" the split method will create an empty element in the list, so we check here if that appened
            if segmento == "":
                return False

            for letter in segmento:
                if not letter.isalpha() or not letter.islower():
                    return False

        #checksum check
        if checksum[0] == "[" and checksum[-1] == "]" and len(checksum) == 7:
           for letter in checksum[1:-1]:
               if not letter.isalpha() or not letter.islower():
                   return False
        else:
            return False

        #tuplo check
        if type(tuplo) == tuple and len(tuplo) >= 2:
            for elemento in tuplo:
                if type(elemento) != int:
                    return False
        else:
            return False

        #return True
        return True 
    else:
        return False

def validar_cifra(cifra:str, control:str):
    
    def sort_funct(key):
        #this function sort the list based on how common the letter is in the cifra and based on alphabetic order to resolve draws
        return common_dictionary[key] - ord(key)


    #replace "-" with "" so that I can go trough all of the letters like a single string
    joined_cifra = cifra.replace("-", "")

    common_dictionary = {}

    for letter in joined_cifra:
        if letter not in common_dictionary:
            common_dictionary.update({
                letter: joined_cifra.count(letter)
                })

    #reorganizar a lista
    order_list = sorted(common_dictionary, key=sort_funct, reverse=True)

    #control should be equal to the first 5 caracters of the order_list
    result = list(control[1:-1]) == order_list[:5]

    return result

def filtrar_bdb(entradas: list):

    if type(entradas) != list or len(entradas) < 1:
        raise ValueError("filtrar bdb: argumento invalido")

    '''#--TODO: is this supposed to be here?
    for entrada in entradas:
        if not eh_entrada(entrada):
            raise ValueError("filtrar bdb: argumento invalido")'''

    #define the filter function
    def filter_funct(entrada):
 
        #we want to filter and get only the ones that are wrong so we will return True if the "entrada" is not OK and False if the "entrada" is OK
        if not eh_entrada(entrada):
            return True

        res = not validar_cifra(entrada[0], entrada[1])

        return res

    filtered_list = list(filter(filter_funct, entradas))

    return filtered_list

#----------------------------#


# -- Desencriptação de dados -- #

def obter_num_seguranca(tuplo: tuple):

    security_number = float("+inf")

    tuplo_size = len(tuplo)

    for index_numero in range(tuplo_size):
        for index_sub_numero in range(tuplo_size):
            
            #we dont want to subtract the same number with him self
            if index_numero == index_sub_numero:
                continue
    
            number1 = tuplo[index_numero]
            number2 = tuplo[index_sub_numero]

            #using modulo to get always the subtraction that gives us the positive number
            possible_security = abs(number1 - number2)

            if possible_security < security_number:
                security_number = possible_security
             
    return security_number

def decifrar_texto(cifra: str, security: int):

    caracter_list = list(cifra)

    for index_caracter in range(len(cifra)):
        
        caracter = cifra[index_caracter]

        if caracter == "-":
            continue

        alphabet_number = ord(caracter) - 96
        caracter_list[index_caracter] = str(alphabet_number)

        if index_caracter % 2 == 0:
            alphabet_number += 1
        else:
            alphabet_number -= 1

        #add security
        alphabet_number += security

        #convert to 1-26 alphabet order
        alphabet_number %= 26

        #correspondent letter
        new_caracter = chr(alphabet_number + 96)

        #update the caracter in the list
        caracter_list[index_caracter] = new_caracter

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
    if type(dictionary) != dict:
        return False

    #verify if we have all the keys
    try:
        name = dictionary["name"]
        passw = dictionary["pass"]
        vals = dictionary["rule"]["vals"]
        char = dictionary["rule"]["char"]
    except:
        return False
    
    #verify names and passwords
    if len(name) < 1 or len(passw) < 1 or len(char) < 1 or type(vals) != tuple or (vals[0] > vals[1]):
        return False 


    #else
    return True

def eh_senha_valida(password: str, rule: dict):
    #gerais

    vowels = ["a", "e", "i", "o", "u"]

    #initialize variable that stores the number of vowels that are present in the password
    number_vowels = 0

    #initialize variable that stores a boolean (True or False) corresponding to the result of the squence rule pass
    sequence_check = False

    #loop through the caracters
    for caracter in password:

        #count the vowels
        if caracter.islower() and caracter in vowels:
            number_vowels += 1

        #check if the caracter appears twice or more in a row 
        if password.count(caracter*2):
            sequence_check = True

    #if the password did not pass the general return False, otherwise continue to individual checks
    if number_vowels < 3 or not sequence_check:
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

    #Am I supposed to add "eh utilizado" here???

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



