#TODO: retirar aquelas identeções que o stor disse

# -- Correção de documentação -- #

def corrigir_palavra(segment: str) -> str: 
    '''
    Function to clean a segment
    
    This function receives a segment of caracters with some "errors" and cleans it

    Parameters
    ----------
    - segment: str
    \n\tsegment/word that are incorrect and need to be fixed
    Examples
    --------
    "cCdatabasacCADde" -> "database"
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
    Function to check if two segments of caracters are anagrams
    
    This function returns a boolean.
    True if the segment1 and segment2 are anagrams, False other wise.
    This function is case insensitive.


    Parameters
    ----------
    - segment: str
    \n\tsegment/word that are incorrect and need to be fixed
    Examples
    --------
    "cCdatabasacCADde" -> "database"
    '''
    
    '''
    This function returns a boolean, True if the segment1 and segment2 are anagrams, False other wise.
    This function is case insensitive.

    Example: "Caso", "Saco" -> True; "saco", "sacos" -> False 
    '''

    #convert all letters of both segments to lower case letters
    segment1 = segment1.lower()
    segment2 = segment2.lower()

    if segment1 != segment2:
    #use the built-in sorted method to "create" a sorted list of the letters and compare the lists 
        return sorted(segment1) == sorted(segment2)
    else:
        return False

def corrigir_doc(string: str) -> str:
    '''
    This function receives a string containing segments separated by a space. This segments can contain trash so we "send" each segment to the function corrigir_palavra() and after cleaning all of the segments join them together (basically removing all the trash in the received string), we exclude from the segments that will be joined the ones that are anagrams of any segment that is present before them (we dont consider equal segments anagrams).

    Example: "JlLjbaoOsuUeYy cChgGvValLCwMmWBbclLsNn" -> "base has"
    '''

    #string check

    #AQUI deixo assim, ou tiro aquilo lá de dentro e mudo a identeção?
    if type(string) == str and len(string) > 0:

        bugged_segments = string.split()

        #--Professor: esta verificaçãio não está a ser realizada em nenhum teste no mooshak? é suposto manter?

        #check if the segments are separated by 1 or more white spaces and raise Error if that happen

        #AQUI meto if string.count("  ") ou deixo assim?
        if string.count("  ") > 0: 
            raise ValueError("corrigir_doc: argumento invalido")
            
        for bugged_segment in bugged_segments:
            if not bugged_segment.isalpha():
                raise ValueError("corrigir_doc: argumento invalido")
    
    else:
        raise ValueError("corrigir_doc: argumento invalido")

    clean_segments = []

    for bugged_segment in bugged_segments:
        clean_current_segment = corrigir_palavra(bugged_segment)

        #TOADD
        if not any([eh_anagrama(clean_segment, clean_current_segment) for clean_segment in clean_segments]):
            clean_segments.append(clean_current_segment)

    #join the cleaned segments and build the cleaned string
    cleaned_string = " ".join(clean_segments)

    return cleaned_string
#--------------------------------#


# -- Descoberta do PIN -- #

def obter_posicao(movement: str, position: int) -> int:
    '''
    This function receives a position and a movement and returns the position after "moving", here we consider "C" as going Up, "B" as going down, "E" as going left and "D" as going right. If we are on the edge of the board we stay in the same place.
    Example: "C", 5 -> 2

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
    Example: "CEE", 5 -> 1

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
    Example: "CEE", "DDBBB", "ECDBE", "CCCCB" -> (1, 9, 8, 5)

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

def eh_entrada(entry: tuple) -> bool:
    '''
    This function receives a tuple and return a boolean, False if the entry have something wrong, True otherwise.
    Example: ("a-b-c-d-e-f-g-h", "[xxxxx]", (950,300)), -> True; ("a-b-c-d-e-f-g-h-2", "[abcde]", (950,300)) -> False

    - param tuple entry: tuple that contain the information that we are going to check
    '''

    if type(entry) != tuple or len(entry) != 3:
        return False

    #initialize variables
    cifra = entry[0]
    checksum = entry[1]
    tuplo = entry[2]


    segments = cifra.split("-")

    #I am using step=2 so we skip the slashes that divide the letters
    if type(cifra) == str: #AQUI: ainda que o enunciado nao tenha pedido eu achei por bem colocar esta verificação
        for segment in segments:
            #here I am checking if the segment in the cifra only contain letters and is lower case
            #this also verify's if the segment is "", this would happen if there is two slashes "--" in a row
            if not segment.isalpha() or not segment.islower():
                return False
    else:
        return False

    #checksum check
    if type(checksum) == str and len(checksum) == 7 and checksum[0] == "[" and checksum[-1] == "]":
        #get the caracters inside the "[", "]"
        control_caracters = checksum[1:-1]

        #check if that caracters are letters and are in lower case
        if not control_caracters.isalpha() or not control_caracters.islower():
            return False
    else:
        return False

    #tuplo check
    if type(tuplo) == tuple and len(tuplo) >= 2:
        #check if every element of the tuple is an positive intenger
        for elemento in tuplo:
            if type(elemento) != int or elemento < 0:
                return False
    else:
        return False

    #otherwise
    return True 

def validar_cifra(cifra:str, checksum:str) -> bool:
    '''
    This function returns a boolean, True if the control caracters on the checksum correspond to the first 5 letters sorted by number of occurence and undrawing by alphabetic order
    Example: "a-b-c-d-e-f-g-h", "[abcde]" -> True; "a-b-c-d-e-f-g-h", "[xxxxx]" -> False

    - param str cifra: string that we are going to run the sort algorithm on
    - param str checksum: contains the control caracters inside "[]" 
    '''


    #get the control caracters [xxxxxx]
    control_caracters = checksum[1:-1]

    #AQUI: substitui isto e anda de 2 em 2 no for loop?!?!?!
    joined_cifra = cifra.replace("-", "")

    #initialize an empty list to save the "best" letters in the cifra
    ordered = []

    #we want the 5 letters that are the most common and undraw by alphabetic order
    for _ in range(5):
        #start by defining a list that contains on the index 0 the best letter and on the index 1 the number of times that the letter appeared
        #0 because any letter that we are going throught will appear at least 1 time so we are just initializing this 
        best = ["", 0]

        for letter in joined_cifra:
            #number of times the letter we are testing appear on the string
            letter_count = joined_cifra.count(letter)

            #check if the letter appeared more times than the current best    
            if letter_count > best[1]:
                best = [letter, letter_count]
            
            #if the number of ocurrences of the current letter is equal to the best letter undraw by alphabetic order
            elif letter_count == best[1]:
                if ord(letter) < ord(best[0]):
                    best = [letter, letter_count]

        #add to the list the best caracter 
        ordered.append(best[0])

        #remove the letter from the joined_cifra so we do not need to go through that letter  again since we already ordenated it (increasing the performance of the algorithm)
        joined_cifra =  joined_cifra.replace(best[0], "")


    ordered_string = "".join(ordered)

    #check if the control list correspond to the best order list and return boolean
    result = control_caracters == ordered_string

    return result

def filtrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing "entries" and return a list containing the ones that had wrong cifras (based on the checksum).
    Example: [("aaaaa-bbb-zx-yz-xy", "[abxyz]", (950,300)), ("a-b-c-d-e-f-g-h", "[abcde]", (124,325,7)), ("entry-muito-errada", "[abcde]", (50,404))] -> [("entry-muito-errada", "[abcde]", (50,404))]
    '''

    #verify if "entries" is a list and if his len is greater than 0  
    if type(entries) == list and len(entries) > 0:
        #go through the entries and check if they are correct, if there is any incorrect raise the ValueError
        for entry in entries:
            if not eh_entrada(entry):
                raise ValueError("filtrar_bdb: argumento invalido")
    else:
        raise ValueError("filtrar_bdb: argumento invalido")

    filtered_list = [entry for entry in entries if not validar_cifra(entry[0], entry[1])]

    return filtered_list

#----------------------------#


# -- Desencriptação de dados -- #

def obter_num_seguranca(tuplo: tuple) -> int:
    '''
    This function receive a tuple containing positive intengers and return a intenger that correspond to the lowest number possibly achievable by subtracting a number in the tuple by other number in the tuple (except it self).
    Example: (2223,424,1316,99) -> 325
    '''

    #start by defining security number has +infinit so that we can for sure have anything lower than +inf
    security_number = float("+inf")

    #AQUI: é melhor usar range e dentro do loop tirar os valores dos numeros ou usar enumerate é a forma mais performatica visto que assim tenho logo o index e o numero

    #go through the numbers in the tuplo and get their index and 
    for index, number in enumerate(tuplo):
        #go once again through the numbers in the tuplo, this time this is to "calculate" all the possible subtractions with the number we are iterating in the above loop
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

def decifrar_texto(cifra: str, security: int) -> str:
    '''
    This function receives a cifra and a security number and decrypts it returning the decrypted string.
    Example: "qgfo-qutdo-s-egoes-wzegsnfmjqz", 325 -> "esta cifra e quase inquebravel"
    '''

    #replace the slash with a space in the cifra
    cifra = cifra.replace("-", " ")

    #create a list containing all the caracters of the cifra, starting all encrypted they will get decrypted from the start to the end 
    decrypted_list = list(cifra)

    for index_caracter, caracter in enumerate(cifra):

        #if the caracter is a whitespace or any other non alphabetic caracter skip iteration
        if not caracter.isalpha():
            continue

        #convert the letter to a number (ASCII CODE) and subtract 96 to get a (1 to 26) order
        alphabet_number = ord(caracter) - ord("a")

        #if the caracter is in a even index in the string add 1 otherwise subtract 1
        if index_caracter % 2 == 0:
            alphabet_number += 1
        else:
            alphabet_number -= 1

        #add security code
        alphabet_number += security

        #"cycle" through the alphabet and get a number between 0-25
        alphabet_number %= 26 #cycle throught the alphabet

        #add 96 to get the alphabet number to the correct ascii code and then convert back to the correspondent letter
        new_caracter = chr(alphabet_number + ord("a"))

        #update/decrypt the letter in the list
        decrypted_list[index_caracter] = new_caracter

    #join the caracters of the list again
    decrypted_string = "".join(decrypted_list)

    return decrypted_string

def decifrar_bdb(entries: list) -> list:
    '''
    This function receives a list containing entries each entry containing a cifra, a checksum and a tuple containing the digits that will be used to calculate the security code and return a list with all the correspondent cifras decrypted
    '''
    if type(entries) == list and len(entries) > 0: 
        #check if we have only entries
        for possible_entry in entries:
            if not eh_entrada(possible_entry):
                raise ValueError("decifrar_bdb: argumento invalido")
    else:
        raise ValueError("decifrar_bdb: argumento invalido")

    #initialize decrypted list where we are going to save our decrypted entries
    decrypted_list = []

    for entry in entries:

        #get the values from the entry
        cifra = entry[0]
        controlo = entry[1]
        security_segment = entry[2]

        #calculate the security code
        security_code = obter_num_seguranca(security_segment)

        #decrypt the cifra using the security code
        decrypted_cifra = decifrar_texto(cifra, security_code)

        #append the decrypted cifra to the list
        decrypted_list.append(decrypted_cifra)

    return decrypted_list

#-------------------------------#


# -- Depuração de senhas -- #

def eh_utilizador(dictionary: dict) -> bool:
    '''
    This function receives a dictionary and returns a boolean, True if the dictionary follow every rule, False othewise

    Example: [("qgfo-qutdo-s-egoes-wzegsnfmjqz", "[abcde]", (2223,424,1316,99)), ("lctlgukvzwy-ji-xxwmzgugkgw", "[abxyz]", (2388, 367, 5999)), ("nyccjoj-vfrex-ncalml", "[xxxxx]", (50, 404))] -> ["esta cifra e quase inquebravel", "fundamentos da programacao", "entrada muito errada"]
    '''

    #verify the type and len of the dictionary
    if type(dictionary) == dict or len(dictionary) == 3: 
        #get the keys of the dictionary
        dictionary_keys = dictionary.keys()
        
        #verify if we have the keys "name", "pass" and "rule"
        if "name" in dictionary_keys and "pass" in dictionary_keys and "rule" in dictionary_keys:

            #create the variables that I will use
            name = dictionary["name"]
            passw = dictionary["pass"]

            #get the rules keys
            dictionary_rule_keys = dictionary["rule"].keys()

            #check val and char
            if "char" in dictionary_rule_keys and "vals" in dictionary_rule_keys:
                #create the variables that will be used
                char = dictionary["rule"]["char"]
                vals = dictionary["rule"]["vals"]

            else:
                return False
            
        else:
            return False
    else:
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
    
    return True

def eh_senha_valida(password: str, rule: dict) -> bool:
    '''
    This function receives a password and a individual rule and checks if the password follows the general rules and the individual rules, returning a boolean.

    Example: "aabcde", {"vals": (1,3), "char":"a"} -> True
    '''

    vowels = ("a", "e", "i", "o", "u")

    #initialize variable that stores the number of vowels that are present in the password
    vowels_number = 0

    #initialize variable that stores a boolean, password have at least 1 letter that appears twice in a row or not
    two_followed = False

    for caracter in password:
        #count the vowels
        if caracter.islower() and caracter in vowels:
            vowels_number += 1

        #check if the caracter appears twice or more in a row int the password
        if not two_followed:
            if password.count(caracter*2) > 0:
                two_followed = True

    #general check
    if vowels_number < 3 or not two_followed:
        return False

    #define individual variables
    char = rule["char"]
    char_min = rule["vals"][0]
    char_max = rule["vals"][1]

    #individual check
    if not(char_max >= password.count(char) >= char_min):
        return False

    return True

def filtrar_senhas(lista: list) -> list:
    '''
    This function receives a list containing bdb entries (dicitonaries) and returns an alphabetic sorted list with the names of the users with wrong passwords

    Example: [{"name":"john.doe", "pass":"aabcde", "rule":{"vals":(1,3), "char":"a"}}, {"name":"jane.doe", "pass":"cdefgh", "rule":{"vals":(1,3), "char":"b"}}, {"name":"jack.doe", "pass":"cccccc", "rule":{"vals":(2,9), "char":"c"}}] -> ["jack.doe", "jane.doe"]
    '''

    if type(lista) == list and len(lista) > 0:
        #check if we have any wrong dictionary in this list
        for dictionary in lista:
            if not eh_utilizador(dictionary):
                raise ValueError("filtrar_senhas: argumento invalido")
    else:
        raise ValueError("filtrar_senhas: argumento invalido")

    #filter, remove the dictionaries that aren't wrong using list comprehension
    filtered_dictionaries = [dictionary for dictionary in lista if not eh_senha_valida(dictionary["pass"], dictionary["rule"])]

    #map, get only the names for each dictionary using list comprehension
    names = [dictionary["name"] for dictionary in filtered_dictionaries]

    #ordenate the names by alphabetic order
    sorted_names = sorted(names)

    return sorted_names

#---------------------------#