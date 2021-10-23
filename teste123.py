
def num_occ_lista(lista, num):
    times = 0


    for element in lista:
        if type(element) == list:
            times += num_occ_lista(element, num)
        else:
            if element == num:
                times += 1

    print(times)


num_occ_lista([1, 2, 3, 4, 3], 3)