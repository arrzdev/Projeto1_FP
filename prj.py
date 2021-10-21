


'''
   Send a message to a recipient

   :param str segment: The person sending the message
   :param str recipient: The recipient of the message
   :param str message_body: The body of the message
   :param priority: The priority of the message, can be a number 1-5
   :type priority: integer or None
   :return: the message id
   :rtype: int
   :raises ValueError: if the message_body exceeds 160 characters
   :raises TypeError: if the message_body is not a basestring
   '''

# -- Correção de documentação -- #

def corrigir_palavra(segment: str) -> str: 
    '''
   This function receives a segment containing "trash" and cleans it returning the cleaned segment
   Example: "cCdatabasacCADde" should return "database"

    - param str segment: segment that contains the "trash"   
   '''

    letter_index = 0

    #here we are going from 1 to len(segment)-1 because we don't want to test the last letter since we don't have any letter after it.
    while letter_index < len(segment)-1:
        
        #store the current letter and the next letter into 2 variables
        current_letter = segment[letter_index]
        next_letter = segment[letter_index+1]

        #here we are converting the letters to ASCII code and checking if the modulo of the diference between them are 32 (difference between lower and capital in ASCII)
        if abs(ord(current_letter) - ord(next_letter)) == 32:
            letters_to_remove = current_letter + next_letter
            segment = segment.replace(letters_to_remove, "")
            
            # in case of a "hit" remove 1 from letter_index so we can test the letter that is before the current letter again. Since we removed some "trash" it's possible that we "created" new trash. For example: ("ABba")
            letter_index -= 1
        else:
            #otherwise keep going trough the letters
            letter_index += 1

    #return the clean segment
    return segment

def eh_anagrama(segment1: str, segment2: str) -> bool:
    '''
    This function returns a boolean, True if the segment1 and segment2 are anagrams, False other wise.
    This function is case insensitive.
    Example: "Caso", "Saco" should return True; "saco", "sacos" should return False 
    '''

    #convert all letters of both segments to lower case letters
    segment1 = segment1.lower()
    segment2 = segment2.lower()

    #use the built-in sorted method to "create" a sorted list of the letters and compare the lists 
    res = sorted(segment1) == sorted(segment2)

    return res

def corrigir_doc(string: str) -> str:
    '''
    This function receives a string containing segments separated by a space. This segments can contain trash so we "send" each segment to the function corrigir_palavra() and after cleaning all of the segments join them together (basically removing all the trash in the received string), we exclude from the segments that will be joined the ones that are anagrams of any segment that is present before them (we dont consider equal segments anagrams).
    Example: "JlLjbaoOsuUeYy cChgGvValLCwMmWBbclLsNn" should return "base has"
    '''

    #string check

    #AQUI deixo assim, ou tiro aquilo lá de dentro e mudo a identeção?
    if type(string) == str:
        #create a list containing the bugged bugged_segments
        bugged_segments = string.split()

        #--Professor: esta verificaçãio não está a ser realizada em nenhum teste no mooshak? é suposto manter?

        #check if the segments are separated by 1 or more white spaces and raise Error if that happen

        #AQUI meto if string.count("  ") ou deixo assim?
        if string.count("  ") > 0:
            raise ValueError("corrigir_doc: argumento invalido")
            
        #check if every caracter is the segment is a letter (lower case or upper case)
        for bugged_segment in bugged_segments:
            if not bugged_segment.isalpha():
                raise ValueError("corrigir_doc: argumento invalido")
    
    else:
        raise ValueError("corrigir_doc: argumento invalido")


    #initialize an empty list where we are going to save our clean segments
    clean_segments = []

    for bugged_segment in bugged_segments:
        #call the function that clean the "bugged" segment
        clean_current_segment = corrigir_palavra(bugged_segment)

        #here I am using the any method and list comprehension to check if there is any segment that is an anagram of the current cleaned segment
        #here we do not consider equal segments as anagrams also we need to convert that to lower before checking  
        #AQUI
        if not any([eh_anagrama(clean_segment, clean_current_segment) and clean_segment.lower() != clean_current_segment.lower() for clean_segment in clean_segments]):
            clean_segments.append(clean_current_segment)

        #AQUI colocar isto invés do any/list comprehension
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

    #join the cleaned segments and build the cleaned string
    cleaned_string = " ".join(clean_segments)

    return cleaned_string

#--------------------------------#


# -- Descoberta do PIN -- #

def obter_posicao(movement: str, position: int) -> int:
    '''
    This function receives a position and a movement and returns the position after "moving", here we consider "C" as going Up, "B" as going down, "E" as going left and "D" as going right. If we are on the edge of the board we stay in the same place.
    Example: "C", 5 should return 2

    - param str movement: "type" of moving we are making
    - param int position: position on the board that we are moving from
    '''

    #here we define the board limits for each movement
    #AQUI: eu acho que usando board era mais dificil de implementar devido à logica mas se for melhor o farei.
    #board = [[1,2,3],[4,5,6],[7,8,9]]

    C_limit = (1,2,3)
    B_limit = (7,8,9)
    E_limit = (1,4,7)
    D_limit = (3,6,9)
     
    #logic to check the next position based on the position we are moving from and the movement
    if movement == "C" and position not in C_limit:
        #AQUI: isto é obvio necessito de deixar estes comentarios?
        #to get the position above the current position we need to subtract 3 from the current position
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

def obter_digito(sequence: str, position: int) -> int:
    '''
    This function receives a sequence of movements and a starting position and return the position that we end with after all the moves.
    Example: "CEE", 5 should return 1

    - param str sequence: sequence of movements that will be looped through to get the last position
    - param int position: starting position
    '''
    
    #go through all the movements in the sequence and using the function "obter_posicao()" get the new position 
    for movement in sequence:
        position = obter_posicao(movement, position)

    #return the last position that we end with
    return position

def obter_pin(sequences: tuple) -> tuple:
    '''
    This function receives some sequences of movements and returns a pin, each sequence corresponds to 1 digit in the pin.
    Example: "CEE", "DDBBB", "ECDBE", "CCCCB" should return (1, 9, 8, 5)

    - param tuple sequences: a tuple that contain the sequences of movements
    '''


    #AQUI: neste tipo de verificações fica mais explicito assim ou se colocasse por exemplo if not(type(sequences) == tuple and len(sequences) > 4 and len(sequences) < 10);

    #check type and lenght of the argument "sequences"
    if type(sequences) != tuple or len(sequences) < 4 or len(sequences) > 10:
        raise ValueError("obter_pin: argumento invalido")
    
    valid_movements = ("C","B","E","D")

    #check if the received sequences do not have invalid movements
    for sequence in sequences:
        #sequence can't be an empty string..
        if sequence == "":
            raise ValueError("obter_pin: argumento invalido")
        else:
            for movement in sequence:
                if movement not in valid_movements:
                    raise ValueError("obter_pin: argumento invalido")

    #initialize an empty tuple to save the pin
    pin = ()

    #initialize a variable with the "standard/starting" position (middle)
    position = 5

    for sequence in sequences:
        #update the position with the new position
        position = obter_digito(sequence, position)

        #create a tuple (digito) containing the position that we ended on after running the sequence of movements
        digito = (position,)

        #concatenate the two tuples to add the digito to the pins 
        pin += digito

    return pin

#-------------------------#


# -- Verificação de dados -- #

def eh_entrada(entrada: tuple) -> bool:
    '''
    WE ENDED HERE
    '''

    if type(entrada) != tuple or len(entrada) != 3:
        return False

    #initialize variables
    cifra = entrada[0]
    checksum = entrada[1]
    tuplo = entrada[2]


    segments = cifra.split("-")

    #alpha and low case check
    for segment in segments:
        if segment == "":
            return False

        for letter in segment:
            if not letter.isalpha() or not letter.islower():
                return False

    #checksum check
    if type(checksum) == str and len(checksum) == 7 and checksum[0] == "[" and checksum[-1] == "]":
        for letter in checksum[1:-1]:
            if not letter.isalpha() or not letter.islower():
                return False
    else:
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

    #verify types of the keys
    if type(name) != str or type(passw) != str or type(vals) != tuple or type(char) != str:
        return False

    #verify lengths
    if len(name) < 1 or len(passw) < 1 or len(vals) != 2 or len(char) != 1:
        return False

    #char alpha and lower case check
    if not char.isalpha():
        return False

    #vals check
    if type(vals[0]) != int or type(vals[1]) != int or vals[0] < 1 or vals[1] < 1 or vals[0] > vals[1]:
        return False
    
    #else
    return True

def eh_senha_valida(password: str, rule: dict):
    #gerais

    vowels = ("a", "e", "i", "o", "u")

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
        #since the eh_senha_valida return True if it is correct we return the opposite of the received boolean, because we want the wrong 
        return not eh_senha_valida(dictionary["pass"], dictionary["rule"])

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