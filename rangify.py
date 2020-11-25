def rangify(arr):
    if arr == []:
        return ''

    final_list = []
    ranger = []
    i = 0

    while i < len(arr):
        if ranger != [] and arr[i] != arr[i - 1] + 1:
            if len(ranger) > 1:
                final_list.append(f'{ranger[0]}-{ranger[-1]}')
            else:
                final_list.append(ranger[0])
            ranger = []
        ranger.append(str(arr[i]))
        i += 1

    if len(ranger) == 1:
        final_list.append(str(arr[-1]))
    else:
        final_list.append(f'{ranger[0]}-{ranger[-1]}')    

    return ', '.join(final_list)

   
# rangify([1, 3, 4, 5, 6, 8, 10, 11])
# '1, 3-6, 8, 10-11'





