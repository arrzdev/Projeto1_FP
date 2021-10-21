def corrigir_palavra(segment: str): 
    letter_index = 0

    #we don't need to test the last letter since we do not have anything after it that's why I am looping till len(segment)-1
    while letter_index < len(segment)-1:
        
        #store the current letter and the next letter into 2 variables
        current_letter = segment[letter_index]
        next_letter = segment[letter_index+1]

        #check if the difference between them are 32 or -32 (ASCII code)
        if abs(ord(current_letter) - ord(next_letter)) == 32:
            letters_to_remove = current_letter + next_letter
            segment = segment.replace(letters_to_remove, "")
            letter_index -= 1
        else:
            letter_index += 1

    return segment


#possible to make in 9 lines but that makes the readability of the code garbage