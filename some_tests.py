def corrigir_palavra(segment: str): 
    letter_index = 0

    #here we loop through the index's till len(segment) - 1 so we dont test the last letter since we don't have any letter after it
    while letter_index < len(segment)-1:
        

        current_letter = segment[letter_index]
        next_letter = segment[letter_index+1]

        if abs(ord(current_letter) - ord(next_letter)) == 32:
            letters_to_remove = current_letter + next_letter
            segment = segment.replace(letters_to_remove, "")
            letter_index -= 1
        else:
            letter_index += 1

    return segment


print(corrigir_palavra("olaaAaAbcDfFcsSaABAabaAsSCfFdCBaAaA"))









#possible to make in 9 lines but that makes the readability of the code garbage