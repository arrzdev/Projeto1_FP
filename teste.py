def eh_anagrama(segment1: str, segment2: str) -> bool:

    '''
    This function returns a boolean, True if the segment1 and segment2 are anagrams, False other wise.
    This function is case insensitive.

    Example: "Caso", "Saco" should return True; "saco", "sacos" should return False 
    '''

    #convert all letters of both segments to lower case letters
    segment1 = segment1.lower()
    segment2 = segment2.lower()

    if segment1 != segment2:
    #use the built-in sorted method to "create" a sorted list of the letters and compare the lists 
        return sorted(segment1) == sorted(segment2)
    else:
        return False

def corrigir_doc(string: str):
    cleaned = []
    fim = [cleaned.append(cleaned) for clean in cleaned if not eh_anagrama(segment, clean) for segment in string.split()]

    print(cleaned)
corrigir_doc("BuAaXOoxiIKoOkggyrFfhHXxR duJjUTtaCcmMtaAGga")
