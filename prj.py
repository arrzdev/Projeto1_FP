
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
 
def eh_anagram(segment1: str, segment2: str):
    #This function returns True or False based on the segment1 and the segment2 being anagrams or not

    #the sorted method creates a list with ordenated caracters
    return sorted(segment1) == sorted(segment2)

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
            if eh_anagram(clean_segment, clean_current_segment) and clean_segment != clean_current_segment:
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
        position = obter_digito(sequence, position)
        digito = (position,)

        pin += digito

    return pin


#-------------------------#