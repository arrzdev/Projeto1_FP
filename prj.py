'''
In this project I coded some functions to fix the problems in\
Buggy Data Base (BDB).
I made a total of 15 functions (3 functions for each problem).

André Filipe Silva Santos
andrefssantos@tecnico.ulisboa.pt
ist1103597

https://github.com/arrzdev
'''

# -- Correção de documentação -- #

def corrigir_palavra(segment: str) -> str: 
    '''
    This function receives a string of characters that represents a word (potentially\
    modified by an outbreak of letters) and returns the string that corresponds\
    to the application of the sequence of reductions.

    segment caracters → segment caracters
    '''

    letter_index = 0

    #the last letter don't need to be checked
    while letter_index < len(segment)-1:
        
        current_letter = segment[letter_index]
        next_letter = segment[letter_index+1]

        #ascii code difference between the same letter but different cases (upper and lower)
        if abs(ord(current_letter) - ord(next_letter)) == ord("a") - ord("A"):
            letters_to_remove = current_letter + next_letter
            segment = segment.replace(letters_to_remove, "")
            
            #clean possible created pattern after removing something ex:(ABba)
            letter_index -= 1
        else:
            letter_index += 1
    
    return segment

def eh_anagrama(segment1: str, segment2: str) -> bool:
    '''
    This function receives two strings of characters corresponding to two words\
    and returns True if and only if one is anagram of the other, that is, if the\
    words are constituted by the same letters, ignoring differences between upper\
    and lowercase and the order between characters.

    segment caracters × segment caracters → boolean
    '''

    segment1 = segment1.lower()
    segment2 = segment2.lower()
    
    return sorted(segment1) == sorted(segment2)

def corrigir_doc(string: str) -> str:
    '''
    This function receives a string that represents the errored text of the BDB\
    documentation and returns the string of characters filtered with the\
    corrected words and the anagrams removed, leaving only their first\
    occurrence. Anagrams are evaluated after word correction and only anagrams\
    that correspond to different words are removed (sequence of characters other\
    than previous words ignoring case differences). 
    This function check the validity of its argument by raising a\
    ValueError with the message "correct doc: argumento invalido" if its\
    argument isn't valid.

    segment caracters → segment caracters
    '''

    def eh_anagrama_diferente(segment1, segment2):
        '''
        Auxiliar function
        returns True if we have a "true" anagram (same letters and corresponding)\
        occurence, except if the segments are the same. 
        '''
        return eh_anagrama(segment1, segment2) and segment1.lower() != segment2.lower()


    #string.count("  ") is True for a number != 0
    if type(string) != str or len(string) == 0 or string.count("  "):
        raise ValueError("corrigir_doc: argumento invalido")

    bugged_segments = string.split()
    clean_segments = []

    for bugged_segment in bugged_segments:
        if not bugged_segment.isalpha():
            raise ValueError("corrigir_doc: argumento invalido")

        clean_current_segment = corrigir_palavra(bugged_segment)

        '''Check if there is any word in the clean segments that is an anagram \
        and is different from the word that we are checking, add it to the list of\
        clean segments if not'''

        if not any(eh_anagrama_diferente(clean_segment, clean_current_segment) for clean_segment in clean_segments):
            clean_segments.append(clean_current_segment)

    cleaned_string = " ".join(clean_segments)

    return cleaned_string

#--------------------------------#


# -- Descoberta do PIN -- #

def obter_posicao(movement: str, position: int) -> int:
    '''
    This function receives a string of characters containing only one character\
    that represents the direction of a single movement ("C", "B", "E" or "D") and\
    an integer representing the current position (1, 2, 3, 4, 5, 6, 7, 8 or 9);\
    and returns the integer that corresponds to the new position after movement.  
    
    segment caracters × int → int
    '''

    new_position = position

    C_limit = (1,2,3)
    B_limit = (7,8,9)
    E_limit = (1,4,7)
    D_limit = (3,6,9)

    #3 is the difference between a number and the number that is above/under
    if movement == "C" and position not in C_limit:
        new_position = position - 3
    elif movement == "B" and position not in B_limit:
        new_position = position + 3

    #1 is the difference between a number and the number that is on is right/left
    elif movement == "E" and position not in E_limit:
        new_position = position - 1
    elif movement == "D" and position not in D_limit:
        new_position = position + 1

    return new_position

def obter_digito(sequence: str, position: int) -> int:
    '''
    This function receives a string containing a sequence of one or more movements\
    and an integer representing the starting position, and returns the integer that\
    corresponds to the digit to be marked after finishing all movements. 

    segment caracters × int → int 
    '''
 
    for movement in sequence:
        position = obter_posicao(movement, position)

    return position

def obter_pin(sequences: tuple) -> tuple:
    '''
    This function receives a tuple containing between 4 and 10 sequences of\
    movements and returns a tuple of integers containing the pin according to\
    the tuple containing the movements.
    
    tuple → tuple
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

        position = digito

        pin += (digito,)

    return pin

#-------------------------#


# -- Verificação de dados -- #

#Auxiliar
def obter_digitos_controlo(checksum):
    '''
    Auxiliar function
    returns the digits between the square brackets in the checksum ("[", "]")
    '''
    return checksum[1:-1]

def eh_entrada(entry: tuple) -> bool:
    '''
    This function receives an argument of any type and returns True if and only\
    if its argument corresponds to an entry from BDB (potentially corrupted), this is\
    a tuple with 3 fields: a cipher, a control sequence, and a security code.

    universal → boolean
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

    control_characters = obter_digitos_controlo(checksum)

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
    This function receives a string of characters containing a cipher and another\
    chain of characters containing a control sequence, and returns True if and only\
    the sequence is consistent with the cipher as described. 

    segment caracters × segment caracters → boolean
    '''

    control_characters = obter_digitos_controlo(checksum)

    ordered = []

    #we want the 5 letters that are the most common and undraw by alphabetic order
    for _ in range(5):

        '''
        start by defining a list that contains on the index 0 the best letter\
        and on the index 1 the number of times that letter appeared 
        '''
        best = ["", 0]

        for caracter in cifra:
            if caracter == "-":
                continue

            letter_count = cifra.count(caracter)
    
            if letter_count > best[1]:
                best = [caracter, letter_count]
            
            elif letter_count == best[1]:
                #undraw alphabetically
                if ord(caracter) < ord(best[0]):
                    best = [caracter, letter_count]

        #add to the ordered list the "best" caracter of this iteration
        ordered.append(best[0])

        #remove the choosen caracter from the cifra so we do not get that again
        cifra =  cifra.replace(best[0], "")

    #get the 5 best letters as a string again
    ordered_string = "".join(ordered)

    result = control_characters == ordered_string

    return result

def filtrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing one or more BDB entries and returns\
    a list containing the entries in which the checksum isn't consistent\
    with the corresponding cipher, in the same order as the original list.
    This function verify's the validity of the its argument by raising a\
    ValueError with the message 'filtrar_bdb: argumento invalido'\
    if it's argument isn't valid.

    list → list
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

#print(validar_cifra("lorem-ipsum-dolor-sit-amet-consectetur-adipiscing-elit-sed-do-eiusmod-tempor-incididunt-ut-labore-et-dolore-magna-aliqua-ut-enim-ad-minim-veniam-quis-nostrud-exercitation-ullamco-laboris-nisi-ut-aliquip-ex-ea-commodo-consequat-duis-aute-irure-dolor-in-reprehenderit-in-voluptate-velit-esse-cillum-dolore-eu-fugiat-nulla-pariatur-excepteur-sint-occaecat-cupidatat-non-proident-sunt-in-culpa-qui-officia-deserunt-mollit-anim-id-est-laborum", "[ietao]"))
# -- Desencriptação de dados -- #

def obter_num_seguranca(tuplo: tuple) -> int:
    '''
    This function receives a tuple of positive integers and returns the security\
    number, that is, the smallest positive difference between any\
    pair of numbers.  
    
    tuple → int
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
    This function receives a string of characters containing a cipher and a\
    security number and returns the decyphred text as described. 

    segment caracters × int → segment caracters
    '''

    '''create a list that will start with all the cifra characters encrypted and\
    will be decrypted from the start to the end'''
    decrypted_characters = []

    for index_caracter, caracter in enumerate(cifra):
        if caracter == "-":
            decrypted_characters.append(" ")
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
        decrypted_characters.append(new_caracter)


    decrypted_cifra = "".join(decrypted_characters)

    return decrypted_cifra

def decifrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing one or more BDB entries and returns\
    a list of equal size, containing the text of the entries decrypted in the\
    same order.
    This function verify's the validity of it's argument by raising a ValueError\
    with the message 'decifrar_bdb: argumento invalido' in case it's argument isn't\
    valid.

    list → list
    '''

    if type(entries) != list or len(entries) == 0: 
        raise ValueError("decifrar_bdb: argumento invalido")

    decrypted_list = []

    for entry in entries:
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
    This function receives an argument of any kind and returns True if and only\
    if its argument corresponds to a dictionary containing the relevant user\
    information, this is, name, password and the individual rule. 
    Name and password must have lenght of at least 1 and can contain any caracter. 

    universal → boolean
    '''

    if type(dictionary) != dict or len(dictionary) != 3: 
        return False

    if "name" not in dictionary or "pass" not in dictionary or "rule" not in dictionary:
        return False

    if "char" not in dictionary["rule"] or "vals" not in dictionary["rule"]:
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
    This function receives a string of characters corresponding to a password\
    and a dictionary containing the individual password creation rule, returning True\
    if and only if the password complies with all rules (general and individual).

    segment caracters × dict → boolean
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

def filtrar_senhas(entries_list: list) -> list:
    '''
    This function receives a list containing one or more dictionaries, and\
    returns a list alphabetically ordered with the names of users with the wrong passwords. 
    This function should verify the validity of it's argument by raising a ValueError\
    with the message 'filtrar_senhas: argumento invalido' in case it's argument isn't valid.

    list → list
    '''

    if type(entries_list) != list or len(entries_list) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")

    #check if we have any wrong dictionary in this list
    for entry in entries_list:
        if not eh_utilizador(entry):
            raise ValueError("filtrar_senhas: argumento invalido")

    #loop through the dictionaries and get the name of the ones that have wrong passwords
    names = [entry["name"] for entry in entries_list if not eh_senha_valida(entry["pass"], entry["rule"])]

    #ordenate the names by alphabetic order
    sorted_names = sorted(names)

    return sorted_names

#---------------------------#