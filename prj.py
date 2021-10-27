'''
In this project we are creating some functions to fix the problems in (Buggy Data Base, BDB).
We made a total of 15 functions (3 functions for each problem).
André Filipe Silva Santos
ist1103597

https://github.com/arrzdev
'''

# -- Correção de documentação -- #

def corrigir_palavra(segment: str) -> str: 
    '''
    This function "cleans" a segment
    
    This function receives a segment of caracters with some "errors" and cleans it.
    By errors we consider sequences of the same two caracters with different cases one lower and one upper, for example "Aa", "aA".

    - segment: str
    \n\tSegment that is incorrect and need to be "cleaned"
    
    Examples:
    "cCdatabasacCADde" -> "database"
    '''

    letter_index = 0

    #len(segment) - 1 so we do not go through the last letter since we don't have any letter after it
    while letter_index < len(segment)-1:
        
        current_letter = segment[letter_index]
        next_letter = segment[letter_index+1]

        #converting both letters to the correspondent ASCII code and then checking if the modulo of the difference is the difference between "a" and "A" in ASCII (difference between lower and capital letters: 32)
        if abs(ord(current_letter) - ord(next_letter)) == ord("a") - ord("A"):
            letters_to_remove = current_letter + next_letter
            segment = segment.replace(letters_to_remove, "")
            
            #when we fix something subtract 1 to the letter index to check the last letter again (example: abBA, when we clean "bB", "aA" is "created")
            letter_index -= 1
        else:
            letter_index += 1
    
    return segment

def eh_anagrama(segment1: str, segment2: str) -> bool:
    '''
    Function to check if two segments of caracters are anagrams.
    
    This function check if two segments are anagrams returning a boolean.
    True if the segment1 and segment2 are anagrams, False other wise.
    This function is case insensitive.

    - segment1: str
    \n\tOne of the segments that will be compared
    - segment2: str
    \n\tOne of the segments that will be compared

    Examples:
    "Caso", "Saco" -> True; 
    "saco", "sacos" -> False 
    '''

    #convert all letters of both segments to lower case letters
    segment1 = segment1.lower()
    segment2 = segment2.lower()

    #use the built-in sorted method to "create" a sorted list of the letters and compare the lists 
    return sorted(segment1) == sorted(segment2)

def corrigir_doc(string: str) -> str:
    '''
    This function receives a string containing segments separated by a space. This segments can contain trash so we "send" each segment to the function corrigir_palavra() and after cleaning all of the segments join them together (basically removing all the trash in the received string), we exclude from the segments that will be joined the ones that are anagrams of any segment that is present before them (we dont consider equal segments anagrams).

    - string: str
    \n\tString containing one or more segments that will be fixed

    Example: "JlLjbaoOsuUeYy cChgGvValLCwMmWBbclLsNn" -> "base has"
    '''

    if type(string) != str or len(string) == 0:
        raise ValueError("corrigir_doc: argumento invalido")

    bugged_segments = string.split()

    if string.count("  "): #any number greater than 0 
        raise ValueError("corrigir_doc: argumento invalido")
        
    for bugged_segment in bugged_segments:
        if not bugged_segment.isalpha():
            raise ValueError("corrigir_doc: argumento invalido")

    clean_segments = []

    for bugged_segment in bugged_segments:
        clean_current_segment = corrigir_palavra(bugged_segment)

        #list comprehension to check if there is any word that is an anagram and is not equal with the word that we are going through, if "not any" return False then add the segment to the cleaned segments
        if not any([eh_anagrama(clean_segment, clean_current_segment) and clean_current_segment.lower() != clean_segment.lower() for clean_segment in clean_segments]):
            clean_segments.append(clean_current_segment)

    cleaned_string = " ".join(clean_segments)

    return cleaned_string

#--------------------------------#


# -- Descoberta do PIN -- #

def obter_posicao(movement: str, position: int) -> int:
    '''
    This function receives a position and a movement and returns the position after "moving", here we consider "C" as going Up, "B" as going down, "E" as going left and "D" as going right. If we are on the edge of the board we stay in the same place.
    
    - movement: str 
    \n\tString containing one of the possible moves ("E", "D", "B", "C")
    - position: int
    \n\tThis parameter contain the position that we are moving from
    
    Examples:
    "C", 5 -> 2;
    "E", 4 -> 4;
    '''

    new_position = position

    C_limit = (1,2,3)
    B_limit = (7,8,9)
    E_limit = (1,4,7)
    D_limit = (3,6,9)

    if movement == "C" and position not in C_limit:
        new_position = position - 3 #3 is the difference between a number and the number that is above/under
    elif movement == "B" and position not in B_limit:
        new_position = position + 3
    elif movement == "E" and position not in E_limit:
        new_position = position - 1 #1 is the difference between a number and the number that is on is right/left
    elif movement == "D" and position not in D_limit:
        new_position = position + 1

    return new_position

def obter_digito(sequence: str, position: int) -> int:
    '''
    This function receives a sequence of movements and a starting position and return the position that we end with after making all the moves.
    
    - sequence: str
    \n\tSequence of movements that will be made
    - position: int
    \n\tposition: Starting position
    
    Examples:
    "CEE", 5 -> 1
    '''
 
    for movement in sequence:
        position = obter_posicao(movement, position)

    return position

def obter_pin(sequences: tuple) -> tuple:
    '''
    This function receives some sequences of movements and returns a pin, each sequence corresponds to 1 digit in the pin.
    
    - sequences: tuple
    \n\Tuple that contain the sequences of movements
    
    Examples: 
    "CEE", "DDBBB", "ECDBE", "CCCCB" -> (1, 9, 8, 5)
    '''

    #check type and lenght of the argument "sequences"
    if type(sequences) != tuple or len(sequences) < 4 or len(sequences) > 10:
        raise ValueError("obter_pin: argumento invalido")
    
    valid_movements = ("C","B","E","D")

    pin = ()

    #5 is the starting position
    position = 5

    for sequence in sequences:
        if sequence == "":
            raise ValueError("obter_pin: argumento invalido")

        for movement in sequence:
            if movement not in valid_movements:
                raise ValueError("obter_pin: argumento invalido")

        digito = obter_digito(sequence, position)

        #update the current position
        position = digito

        pin += (digito,)

    return pin

#-------------------------#


# -- Verificação de dados -- #

def eh_entrada(entry: tuple) -> bool:
    '''
    This function receives a tuple and return a boolean, False if the entry have something wrong, True otherwise.

    PARAMETERS
    ----------
    - entry: tuple
    \n\tTuple that contain the information that we are going to check, contains a string with single caracteres divided by "-", a string (checksum) containing 5 digits of control inside square brackets "[]" and a tuple with two or more positive intengers.

    RETURN
    ------


    Examples: 
    ("a-b-c-d-e-f-g-h", "[xxxxx]", (950,300)), -> True; ("a-b-c-d-e-f-g-h-2", "[abcde]", (950,300)) -> False
    '''

    if type(entry) != tuple or len(entry) != 3:
        return False

    #initialize variables
    cifra = entry[0]
    checksum = entry[1]
    tuplo = entry[2]

    segments = cifra.split("-")

    if type(cifra) != str:
        return False
    
    for segment in segments:
        #already testing if the segment is "" that would happen if we have two slashes in a row "--"
        if not segment.isalpha() or not segment.islower():
            return False

    #checksum check
    if type(checksum) != str or len(checksum) != 7 or checksum[0] != "[" or checksum[-1] != "]":
        return False

    #get the caracters inside the "[", "]"
    control_caracters = checksum[1:-1]

    if not control_caracters.isalpha() or not control_caracters.islower():
        return False

    if type(tuplo) != tuple or len(tuplo) < 2:
        return False
    
    for element in tuplo:
        if type(element) != int or element < 0:
            return False

    return True 

def validar_cifra(cifra:str, checksum:str) -> bool:
    '''
    This function returns a boolean, True if the control caracters on the checksum correspond to the first 5 letters sorted by number of occurence and undrawing by alphabetic order

    - param str cifra: string that we are going to run the sort algorithm on
    - param str checksum: contains the control caracters inside "[]" 
    
    Examples:
    "a-b-c-d-e-f-g-h", "[abcde]" -> True; "a-b-c-d-e-f-g-h", "[xxxxx]" -> False
    '''

    #get the caracters inside the "[", "]"
    control_caracters = checksum[1:-1]

    joined_cifra = cifra.replace("-", "")

    ordered = []

    #we want the 5 letters that are the most common and undraw by alphabetic order
    for _ in range(5):

        #start by defining a list that contains on the index 0 the best letter and on the index 1 the number of times that the letter appeared
        #0 because any letter that we are going throught will appear at least 1 time so we are just initializing this 
        best = ["", 0]

        for letter in joined_cifra:
            letter_count = joined_cifra.count(letter)
    
            if letter_count > best[1]:
                best = [letter, letter_count]
            
            #if the number of ocurrences of the current letter is equal to the best letter undraw by alphabetic order
            elif letter_count == best[1]:
                if ord(letter) < ord(best[0]):
                    best = [letter, letter_count]

        #add to the ordered list the best caracter 
        ordered.append(best[0])

        #remove the letter from the joined_cifra so we do not go through that letter again
        joined_cifra =  joined_cifra.replace(best[0], "")


    ordered_string = "".join(ordered)

    result = control_caracters == ordered_string

    return result

def filtrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing "entries" and return a list containing the ones that had wrong cifras (based on the checksum).

    Examples: 
    [("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950,300)), ("a-b-c-d-e-f-g-h", "[abcde]", (124,325,7)), ("entry-muito-errada", "[abcde]", (50,404))] -> [("entry-muito-errada", "[abcde]", (50,404))]
    '''

    if type(entries) != list or len(entries) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")

    for entry in entries:
        if not eh_entrada(entry):
            raise ValueError("filtrar_bdb: argumento invalido")

    #AQUI: Este comentario chega para explicar a list comprehension

    #list comprehension to filter the list and get the ones that have wrong cifra's
    filtered_list = [entry for entry in entries if not validar_cifra(entry[0], entry[1])]

    return filtered_list

#----------------------------#


# -- Desencriptação de dados -- #

def obter_num_seguranca(tuplo: tuple) -> int:
    '''
    This function receive a tuple containing positive intengers and return a intenger that correspond to the lowest number possibly achievable by subtracting a number in the tuple by other number in the tuple (except it self).
    
    Examples:
    (2223,424,1316,99) -> 325
    '''

    #start by defining security number has +infinit so that we can for sure have anything lower than +inf
    security_number = float("+inf")

    #go through the numbers in the tuplo and get their index and 
    for index, number in enumerate(tuplo):
        #go once again through the numbers in the tuplo, this time this is to "calculate" all the possible subtractions with the number we are iterating in the above loop
        for subtract_index, subtract_number in enumerate(tuplo):

            #we dont want to subtract the same number with him self
            if index == subtract_index:
                continue

            #using modulo to get always the subtraction that gives us the positive number
            possible_security = abs(number - subtract_number)

            if possible_security < security_number:
                security_number = possible_security
             
    return security_number

def decifrar_texto(cifra: str, security: int) -> str:
    '''
    This function receives a cifra and a security number and decrypts it returning the decrypted string.
    
    Examples:
    "qgfo-qutdo-s-egoes-wzegsnfmjqz", 325 -> "esta cifra e quase inquebravel"
    '''

    #replace the slash with a space in the cifra
    cifra = cifra.replace("-", " ")

    #create a list that will start with all the cifra caracters encrypted and will be decrypted from the start to the end
    decrypted_caracters = list(cifra)

    for index_caracter, caracter in enumerate(cifra):

        #if the caracter is a whitespace or any other non alphabetic caracter skip iteration
        if not caracter.isalpha():
            continue

        #convert the letter to a number (ASCII CODE) and subtract "ord("a")" (97) to get a (0 to 25, corresponding to the alphaber) order
        alphabet_number = ord(caracter) - ord("a")

        if index_caracter % 2 == 0:
            alphabet_number += 1
        else:
            alphabet_number -= 1

        alphabet_number += security

        #"cycle" through the alphabet and get a number between in the range 0-25, example: 25 = "z"; 26 = 0 = "a"
        alphabet_number %= 26 #cycle throught the alphabet

        #add "ord("a")" (97) to get the alphabet number to the correct ascii code and then convert back to the correspondent letter
        new_caracter = chr(alphabet_number + ord("a"))

        #update/decrypt the letter in the list
        decrypted_caracters[index_caracter] = new_caracter


    decrypted_cifra = "".join(decrypted_caracters)

    return decrypted_cifra

def decifrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing entries each entry containing a cifra, a checksum and a tuple containing the digits that will be used to calculate the security code and return a list with all the correspondent cifras decrypted

    Examples:
    [("qgfo-qutdo-s-egoes-wzegsnfmjqz", "[abcde]", (2223,424,1316,99)), ("lctlgukvzwy-ji-xxwmzgugkgw", "[abxyz]", (2388, 367, 5999)), ("nyccjoj-vfrex-ncalml", "[xxxxx]", (50, 404))] -> ["esta cifra e quase inquebravel", "fundamentos da programacao", "entrada muito errada"]
    '''

    if type(entries) != list or len(entries) == 0: 
        raise ValueError("decifrar_bdb: argumento invalido")

    #initialize decrypted list where we are going to save our decrypted entries
    decrypted_list = []

    for entry in entries:

        #check
        if not eh_entrada(entry):
            raise ValueError("decifrar_bdb: argumento invalido")

        cifra = entry[0]
        security_tuple = entry[2]

        security_code = obter_num_seguranca(security_tuple)

        decrypted_cifra = decifrar_texto(cifra, security_code)

        decrypted_list.append(decrypted_cifra)

    return decrypted_list

#-------------------------------#


# -- Depuração de senhas -- #

def eh_utilizador(dictionary: dict) -> bool:
    '''
    This function receives a dictionary and returns a boolean, True if the dictionary follow every rule, False othewise

    Examples:
    {"name":"john.doe", "pass":"aabcde", "rule":{"vals": (1,3), "char":"a"}} -> True
    '''

    #verify the type and len of the dictionary
    if type(dictionary) != dict or len(dictionary) != 3: 
        return False

    #verify if we have the keys "name", "pass" and "rule"
    dictionary_keys = dictionary.keys()
    if "name" not in dictionary_keys or "pass" not in dictionary_keys or "rule" not in dictionary_keys:
        return False

    #check val and char
    dictionary_rule_keys = dictionary["rule"].keys()
    if "char" not in dictionary_rule_keys or "vals" not in dictionary_rule_keys:
        return False

    name = dictionary["name"]
    passw = dictionary["pass"]

    char = dictionary["rule"]["char"]
    vals = dictionary["rule"]["vals"]

    #verify types of the keys
    if type(name) != str or type(passw) != str or type(vals) != tuple or type(char) != str:
        return False

    #verify lengths
    if len(name) == 0 or len(passw) == 0 or len(vals) != 2 or len(char) != 1:
        return False

    #char alpha and lower case check
    if not char.isalpha():
        return False

    #vals check
    if type(vals[0]) != int or type(vals[1]) != int or vals[0] < 1 or vals[1] < 1 or vals[0] > vals[1]:
        return False
    
    return True

def eh_senha_valida(password: str, rule: dict) -> bool:
    '''
    This function receives a password and a individual rule and checks if the password follows the general rules and the individual rules, returning a boolean.

    Example: "aabcde", {"vals": (1,3), "char":"a"} -> True
    '''

    vowels = ("a", "e", "i", "o", "u")

    vowels_count = 0

    #initialize variable that stores a boolean, password have at least 1 letter that appears twice in a row or not
    two_followed = False

    for caracter in password:
        #count the vowels
        if caracter.islower() and caracter in vowels:
            vowels_count += 1

        #check if the caracter appears twice or more in a row int the password
        if not two_followed:
            if password.count(caracter*2) > 0:
                two_followed = True


    if vowels_count < 3 or not two_followed:
        return False

    #individual checks
    char = rule["char"]
    char_min = rule["vals"][0]
    char_max = rule["vals"][1]

    if not(char_max >= password.count(char) >= char_min):
        return False

    return True

def filtrar_senhas(lista: list) -> list:
    '''
    This function receives a list containing bdb entries (dicitonaries) and returns an alphabetic sorted list with the names of the users with wrong passwords

    Examples:
    [{"name":"john.doe", "pass":"aabcde", "rule":{"vals":(1,3), "char":"a"}}, {"name":"jane.doe", "pass":"cdefgh", "rule":{"vals":(1,3), "char":"b"}}, {"name":"jack.doe", "pass":"cccccc", "rule":{"vals":(2,9), "char":"c"}}] -> ["jack.doe", "jane.doe"]
    '''

    if type(lista) != list or len(lista) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")
    
    #AQUI: visto que faço a verificação e depois uso list comprehension para filtrar estou a repetir o mesmo loop duas vezes, vale a pena passar de list comprehension para dentro deste for ou entao levantar os erros na list comprehension se der?!?!

    #check if we have any wrong dictionary in this list
    for dictionary in lista:
        if not eh_utilizador(dictionary):
            raise ValueError("filtrar_senhas: argumento invalido")

    #AQUI: Eu posso dar join destas 2 e fazer uma unica list comprehension
    names = [dictionary["name"] for dictionary in lista if not eh_senha_valida(dictionary["pass"], dictionary["rule"])]

    #ordenate the names by alphabetic order
    sorted_names = sorted(names)

    return sorted_names

#---------------------------#