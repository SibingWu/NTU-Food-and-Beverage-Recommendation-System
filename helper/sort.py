def merge(list_left, list_right, index):
    list_merged = []

    # while left and right list both have elements
    while list_left and list_right:
        if list_left[0][index]<list_right[0][index]:
            list_merged.append(list_left[0])
            list_left.pop(0)
        else:
            list_merged.append(list_right[0])
            list_right.pop(0)

    # append the contents to the end of the merged list
    if list_left:
        list_merged.extend(list_left)
    else:
        list_merged.extend(list_right)

    return list_merged


def mergesort(list, index):
    list_len = len(list)
    if list_len<2:
        return list
    else:
        list_left = mergesort(list[:list_len//2], index)
        list_right = mergesort(list[list_len//2:], index)
        return merge(list_left, list_right, index)


# sort a list of lists based on the at the index position
def listsort(list, index):
    return mergesort(list, index)