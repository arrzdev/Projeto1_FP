'''
In this project I coded some functions to fix the problems in \
Buggy Data Base (BDB).
I made a total of 15 functions (3 functions for each problem).
André Filipe Silva Santos
ist1103597

https://github.com/arrzdev
'''

# -- Correção de documentação -- #

def corrigir_palavra(segment: str) -> str: 
    '''
    This function "cleans" a segment.
    
    This function receives a string of characters that represents a word (potentially \
    modified by an outbreak of letters) and returns the string that corresponds \
    to the application of the sequence of reductions.

    PARAMETERS
    ----------
    - segment: str 
    \n\tString that is incorrect and need to be "cleaned"

    RETURN
    ------
    - segment: str
    \n\tString that was cleaned 
    
    EXAMPLES
    --------
    "cCdatabasacCADde" -> "database"
    '''

    letter_index = 0

    #len(segment) - 1 so we don't check the last letter
    while letter_index < len(segment)-1:
        
        current_letter = segment[letter_index]
        next_letter = segment[letter_index+1]

        #checking if the difference between the ascii code of the two letters correspond to the difference between two letter with diferent "cases" in modulo... (32)
        if abs(ord(current_letter) - ord(next_letter)) == ord("a") - ord("A"):
            letters_to_remove = current_letter + next_letter
            segment = segment.replace(letters_to_remove, "")
            
            #when we change something in the string subtract 1 to the letter index, so we check if there is some new "pattern" that was created ex:(ABba)
            letter_index -= 1
        else:
            letter_index += 1
    
    return segment

def eh_anagrama(segment1: str, segment2: str) -> bool:
    '''
    This function receives two strings of characters corresponding to two words \
    and returns True if and only if one is anagram of the other, that is, if the \
    words are constituted by the same letters, ignoring differences between upper \
    and lowercase and the order between characters.

    PARAMETERS
    ----------
    - segment1: str
    \n\tOne of the strings that will be compared
    - segment2: str
    \n\tOne of the strings that will be compared

    RETURN
    ------
    - res: bool
	\n\tBoolean, True if the two strings are anagrams, False otherwise

    EXAMPLES
    --------
    "Caso", "Saco" -> True; 
    "saco", "sacos" -> False 
    '''

    segment1 = segment1.lower()
    segment2 = segment2.lower()

    res = sorted(segment1) == sorted(segment2)
    
    return res

def corrigir_doc(string: str) -> str:
    '''
    Function that "clean" a BDB document.
    
    This function receives a string that represents the errored text of the BDB \
    documentation and returns the string of characters filtered with the \
    corrected words and the anagrams removed, leaving only their first \
    occurrence. Anagrams are evaluated after word correction and only anagrams \
    that correspond to different words are removed (sequence of characters other \
    than previous words ignoring case differences). 
    This function check the validity of its argument by raising a \
    ValueError with the message "correct doc: argumento invalido" if its \
    argument isn't valid.

    PARAMETERS
    ----------
    - string: str
    \n\tThe words in this string can only be separated by a single space, the string \
    is formed by one or more words, and each word is formed by at least 1 letter \
    (case independent)
   
    RETURN
    ------
    - cleaned_string: str
    \n\tString that was cleaned
   
    EXAMPLES
    --------
    "JlLjbaoOsuUeYycChgGvValLCwMmWBbclLsNn" -> "base has"
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

        '''
        Check if there is any word that is an anagram and isn't equal with the word \
        that we are going through (since here we consider that equal words are not \
        anagrams), if there isn't any anagram we add the segment to the clean segments list
        '''
        if not any([eh_anagrama(clean_segment, clean_current_segment) and clean_current_segment.lower() != clean_segment.lower() for clean_segment in clean_segments]):
            clean_segments.append(clean_current_segment)

    cleaned_string = " ".join(clean_segments)

    return cleaned_string

#--------------------------------#


# -- Descoberta do PIN -- #

def obter_posicao(movement: str, position: int) -> int:
    '''
    This function receives a string of characters containing only one character \
    that represents the direction of a single movement ("C", "B", "E" or "D") and \
    an integer representing the current position (1, 2, 3, 4, 5, 6, 7, 8 or 9); \
    and returns the integer that corresponds to the new position after movement.  
    
    PARAMETERS
    ----------
    - movement: str 
    \n\tString containing one of the possible moves ("E", "D", "B", "C")
    - position: int
    \n\tThis parameter contain the position that we are moving from
    
    RETURN
    ------
    - new_position: int
    \n\tPosition that we got after making (or not in case of an edge move..) the move.
    
    EXAMPLES
    --------
    "C", 5 -> 2;
    "E", 4 -> 4;
    '''

    '''
    BOARD:
    |-----------|
    | 1   2   3 |
    | 4   5   6 |
    | 7   8   9 |
    |-----------|
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
    This function receives a string containing a sequence of one or more movements \
    and an integer representing the starting position, and returns the integer that \
    corresponds to the digit to be marked after finishing all movements. 

    PARAMETERS
    ----------
    - sequence: str
    \n\tSequence of movements that will be made
    - position: int
    \n\tposition: Starting position
    
    RETURN
    ------
    - position: int
    \n\t The position that we end with after making all the moves

    EXAMPLES
    --------
    "CEE", 5 -> 1
    '''
 
    for movement in sequence:
        position = obter_posicao(movement, position)

    return position

def obter_pin(sequences: tuple) -> tuple:
    '''
    This function receives a tuple containing between 4 and 10 sequences of \
    movements and returns a tuple of integers containing the pin according to \
    the tuple containing the movements.
    This function verify's the validity of its argument, this is, a tuple \
    containing between 4 and 10 sequences of movements, each sequence with 1 or \
    more characters, "C", "B", "E" or "D"), generating a ValueError \
    with the message "obter_pin: argumento invalido" if its argument isn't valid.
    
    PARAMETERS
    ----------
    - sequences: tuple
    \n\tTuple that contain the sequences of movements
    
    RETURN
    ------
    - pin: tuple
    \n\tTuple containing the digits of the pin

    EXAMPLES
    -------- 
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
    This function receives an argument of any type and returns True if and only \
    if its argument corresponds to an entry from BDB (potentially corrupted), this is \
    a tuple with 3 fields: a cipher, a control sequence, and a security code.

    PARAMETERS
    ----------
    - entry: universal
    \n\tArgument that will be checked

    RETURN
    ------
    boolean, True if it is a entry of BDB, False otherwise

    EXAMPLES
    -------- 
    ("a-b-c-d-e-f-g-h", "[xxxxx]", (950,300)), -> True\n
    ("a-b-c-d-e-f-g-h-2", "[abcde]", (950,300)) -> False
    '''

    if type(entry) != tuple or len(entry) != 3:
        return False

    cifra = entry[0]
    checksum = entry[1]
    tuplo = entry[2]

    segments = cifra.split("-")

    if type(cifra) != str:
        return False
    
    for segment in segments:
        if not segment.isalpha() or not segment.islower():
            return False

    if type(checksum) != str or len(checksum) != 7 or checksum[0] != "[" or checksum[-1] != "]":
        return False

    #get the characters inside the "[", "]"
    control_characters = checksum[1:-1]

    if not control_characters.isalpha() or not control_characters.islower():
        return False

    if type(tuplo) != tuple or len(tuplo) < 2:
        return False
    
    for element in tuplo:
        if type(element) != int or element < 0:
            return False

    return True 

def validar_cifra(cifra:str, checksum:str) -> bool:
    '''
    This function receives a string of characters containing a cipher and another \
    chain of characters containing a control sequence, and returns True if and only \
    the sequence is consistent with the cipher as described. 

    PARAMETERS
    ----------
    - param str cifra: 
    \n\tstring that we are going to run the sort algorithm on
    - param str checksum:
    \n\tcontains the control characters inside "[]" 
    
    RETURN
    ------
    - result: bool
    \n\tBoolean, True if control characters and ordered characters are equal

    EXAMPLES
    --------
    "a-b-c-d-e-f-g-h", "[abcde]" -> True\n
    "a-b-c-d-e-f-g-h", "[xxxxx]" -> False
    '''

    #get the characters inside the "[", "]"
    control_characters = checksum[1:-1]

    joined_cifra = cifra.replace("-", "")

    ordered = []

    #we want the 5 letters that are the most common and undraw by alphabetic order
    for _ in range(5):

        '''
        start by defining a list that contains on the index 0 the best letter \
        and on the index 1 the number of times that letter appeared 
        '''
        best = ["", 0]

        for letter in joined_cifra:
            letter_count = joined_cifra.count(letter)
    
            if letter_count > best[1]:
                best = [letter, letter_count]
            
            elif letter_count == best[1]:
                #undraw alphabetically
                if ord(letter) < ord(best[0]):
                    best = [letter, letter_count]

        #add to the ordered list the "best" caracter
        ordered.append(best[0])

        #remove the letter from the joined_cifra so we do not choose that letter again
        joined_cifra =  joined_cifra.replace(best[0], "")

    #get the 5 best letters as a string again
    ordered_string = "".join(ordered)

    result = control_characters == ordered_string

    return result

def filtrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing one or more BDB entries and returns \
    a list containing the entries in which the checksum isn't consistent \
    with the corresponding cipher, in the same order as the original list.
    This function verify's the validity of the its argument by raising a \
    ValueError with the message 'filtrar_bdb: argumento invalido' \
    if it's argument isn't valid.

    PARAMETERS
    ----------
    - entries: list
    \n\tList containing the BDB entries 

    RETURN
    ------
    - filtered_list: list
    \n\tList containing the wrong entries

    EXAMPLE
    -------
    [("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950,300)), ("a-b-c-d-e-f-g-h", "[abcde]", (124,325,7)), ("entry-muito-errada", "[abcde]", (50,404))] -> [("entry-muito-errada", "[abcde]", (50,404))]
    '''

    if type(entries) != list or len(entries) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")

    for entry in entries:
        if not eh_entrada(entry):
            raise ValueError("filtrar_bdb: argumento invalido")

    #loop through the entries and keep the ones that returned False from the "validar_cifra"
    filtered_list = [entry for entry in entries if not validar_cifra(entry[0], entry[1])]

    return filtered_list

#----------------------------#


# -- Desencriptação de dados -- #

def obter_num_seguranca(tuplo: tuple) -> int:
    '''
    This function receives a tuple of positive integers and returns the security \
    number, that is, the smallest positive difference between any \
    pair of numbers.  
    
    PARAMETERS
    ----------
    - tuplo: tuple
    \n\tTuple that contain the positive intengers

    RETURN
    ------
    - security_number: tuple

    EXAMPLES
    --------
    (2223,424,1316,99) -> 325
    '''

    #start with "+infinit" so that we can for sure have anything lower
    security_number = float("+inf")
 
    for index, number in enumerate(tuplo):
        #this second loop get us all the possible combinations of a list with it self
        for subtract_index, subtract_number in enumerate(tuplo):

            #we dont want to subtract the same number with him self so skip
            if index == subtract_index:
                continue

            #using modulo to get always the subtraction that gives us the positive number
            subtraction_result = abs(number - subtract_number)

            if subtraction_result < security_number:
                security_number = subtraction_result
             
    return security_number

def decifrar_texto(cifra: str, security: int) -> str:
    '''
    This function receives a string of characters containing a cipher and a \
    security number and returns the decyphred text as described. 

    PARAMETER
    ---------
    - cifra: str
    \n\tString that contain a cypher

    RETURN
    ------
    - decrypted_cifra: str
    \n\tString that is the decrypted cypher

    EXAMPLES
    --------
    "qgfo-qutdo-s-egoes-wzegsnfmjqz", 325 -> "esta cifra e quase inquebravel"
    '''

    cifra = cifra.replace("-", " ")

    #create a list that will start with all the cifra characters encrypted and 
    #will be decrypted from the start to the end
    decrypted_characters = list(cifra)

    for index_caracter, caracter in enumerate(cifra):
        if not caracter.isalpha(): #this also skips white spaces
            continue

        #convert the letter to the correspondent ascii code and subtract "ord("a")" 
        #to get a number in range (0 to 25) corresponding to the alphabet order
        alphabet_number = ord(caracter) - ord("a")

        if index_caracter % 2 == 0:
            alphabet_number += 1
        else:
            alphabet_number -= 1

        alphabet_number += security

        #"cycle" through the alphabet and get a number in the range (0-25)
        alphabet_number %= 26 #cycle throught the alphabet

        #add "ord("a")" to get the get the correspondent letter once again
        new_caracter = chr(alphabet_number + ord("a"))

        #update/decrypt the letter in the list
        decrypted_characters[index_caracter] = new_caracter


    decrypted_cifra = "".join(decrypted_characters)

    return decrypted_cifra

def decifrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing one or more BDB entries and returns \
    a list of equal size, containing the text of the entries decrypted in the \
    same order.
    This function verify's the validity of it's argument by raising a ValueError \
    with the message 'decifrar_bdb: argumento invalido' in case it's argument isn't \
    valid.

    PARAMETER
    ---------
    - entries: list
    \n\tList that contain the BDB entries to be decyphred.

    RETURN
    ------
    - decrypted_list: list
    \n\tList containing the decrypted BDB entries. 

    EXAMPLES
    --------
    [("qgfo-qutdo-s-egoes-wzegsnfmjqz", "[abcde]", (2223,424,1316,99)), ("lctlgukvzwy-ji-xxwmzgugkgw", "[abxyz]", (2388, 367, 5999)), ("nyccjoj-vfrex-ncalml", "[xxxxx]", (50, 404))] -> ["esta cifra e quase inquebravel", "fundamentos da programacao", "entrada muito errada"]
    '''

    if type(entries) != list or len(entries) == 0: 
        raise ValueError("decifrar_bdb: argumento invalido")

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
    This function receives an argument of any kind and returns True if and only \
    if its argument corresponds to a dictionary containing the relevant user \
    information, this is, name, password and the individual rule. 
    Name and password must have lenght of at least 1 and can contain any caracter. 

    PARAMETERS
    ----------
    - dictionary: universal
    \n\tArgument that will be checked, if it is a BDB entrie or not, it should be a dictionary

    RETURN
    ------
    Bool, True if it is a dicitonary with the relevant user information, False otherwise

    EXAMPLES
    --------
    {"name":"john.doe", "pass":"aabcde", "rule":{"vals": (1,3), "char":"a"}} -> True
    '''

    if type(dictionary) != dict or len(dictionary) != 3: 
        return False

    dictionary_keys = dictionary.keys()
    if "name" not in dictionary_keys or "pass" not in dictionary_keys or "rule" not in dictionary_keys:
        return False

    dictionary_rule_keys = dictionary["rule"].keys()
    if "char" not in dictionary_rule_keys or "vals" not in dictionary_rule_keys:
        return False

    name = dictionary["name"]
    passw = dictionary["pass"]

    char = dictionary["rule"]["char"]
    vals = dictionary["rule"]["vals"]

    if type(name) != str or type(passw) != str or type(vals) != tuple or type(char) != str:
        return False

    if len(name) == 0 or len(passw) == 0 or len(vals) != 2 or len(char) != 1:
        return False

    if not char.isalpha():
        return False

    if type(vals[0]) != int or type(vals[1]) != int or vals[0] < 1 or vals[1] < 1 or vals[0] > vals[1]:
        return False
    
    return True

def eh_senha_valida(password: str, rule: dict) -> bool:
    '''
    This function receives a string of characters corresponding to a password \
    and a dictionary containing the individual password creation rule, returning True \
    if and only if the password complies with all rules (general and individual).

    PARAMETERS
    ----------
    - password: str
    \n\tString that corresponds to the user password
    - rule: dict
    \n\tDictionary that contain the individual rules of password creation

    RETURN
    ------
    Bool, True if the user password passed the individual and general rules, False otherwise

    EXAMPLE
    -------
    "aabcde", {"vals": (1,3), "char":"a"} -> True
    '''

    vowels = ("a", "e", "i", "o", "u")

    vowels_count = 0

    #this is the variable that says if we passed the two letters in a row check..
    two_followed = False

    for caracter in password:

        if caracter.islower() and caracter in vowels:
            vowels_count += 1

        if not two_followed:
            #if the caracter appear 2 times in a row in the string
            if password.count(caracter*2) > 0:
                two_followed = True

    #check if we passed the general rules
    if vowels_count < 3 or not two_followed:
        return False

    #individual checks
    char = rule["char"]
    char_min = rule["vals"][0]
    char_max = rule["vals"][1]

    #check if we passed the individual rules
    if not(char_max >= password.count(char) >= char_min):
        return False

    return True

def filtrar_senhas(lista: list) -> list:
    '''
    This function receives a list containing one or more dictionaries, and \
    returns a list alphabetically ordered with the names of users with the wrong passwords. 
    This function should verify the validity of it's argument by raising a ValueError \
    with the message 'filtrar_senhas: argumento invalido' in case it's argument isn't valid.

    PARAMETERS
    ----------
    - lista: list
    \n\tList containing the dictionaries

    RETURN
    ------
    - sorted_names: list
    \n\tList that contain the names that are wrong, alphabetically ordered

    EXAMPLES
    --------
    [{"name":"john.doe", "pass":"aabcde", "rule":{"vals":(1,3), "char":"a"}}, {"name":"jane.doe", "pass":"cdefgh", "rule":{"vals":(1,3), "char":"b"}}, {"name":"jack.doe", "pass":"cccccc", "rule":{"vals":(2,9), "char":"c"}}] -> ["jack.doe", "jane.doe"]
    '''

    if type(lista) != list or len(lista) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")

    #check if we have any wrong dictionary in this list
    for dictionary in lista:
        if not eh_utilizador(dictionary):
            raise ValueError("filtrar_senhas: argumento invalido")

    #loop through the dictionaries and get the name of the ones that have wrong passwords
    names = [dictionary["name"] for dictionary in lista if not eh_senha_valida(dictionary["pass"], dictionary["rule"])]

    #ordenate the names by alphabetic order
    sorted_names = sorted(names)

    return sorted_names

#---------------------------#