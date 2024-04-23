# # Mergesort algorithm
# def MergeSort(lst):
# 	middle = len(lst) // 2
# 	left_half = lst[:middle]
# 	right_half = lst[middle:]
# 	sorted_left_half = MergeSort(left_half)
# 	sorted_right_half = MergeSort(right_half)
# 	return MergeLists(sorted_left_half, sorted_right_half)
#
#
# # Merging two sorted lists into one sorted list
# def MergeLists(left_half, right_half):
# 	full_list = []
# 	while left_half and right_half:
# 		if left_half[0] < right_half[0]:
# 			full_list.append(left_half.pop(0))
# 		else:
# 			full_list.append(right_half.pop(0))
# 	if left_half:
# 		full_list += left_half
# 	if right_half:
# 		full_list += right_half
# 	return full_list

def MergeSort(listToSort):
    if len(listToSort) <= 1:
        return listToSort

    midpoint = len(listToSort) // 2
    leftHalf = listToSort[:midpoint]
    rightHalf = listToSort[midpoint:]

    leftHalf = MergeSort(leftHalf)
    rightHalf = MergeSort(rightHalf)

    return MergeSortedHalves(leftHalf, rightHalf)

def MergeSortedHalves(leftHalf, rightHalf):
    sortedList = []
    i = j = 0

    while i < len(leftHalf) and j < len(rightHalf):
        if leftHalf[i] < rightHalf[j]:
            sortedList.append(leftHalf[i])
            i += 1
        else:
            sortedList.append(rightHalf[j])
            j += 1

    sortedList.extend(leftHalf[i:])
    sortedList.extend(rightHalf[j:])

    return sortedList

lst1 = [-3, 5, -1, 7, -2, 9, 1]
lst2 = [10, -2, 8, -6, 12, -4, 2]
lst2 = [1,2,3,4,5,6,7]
lst1 = MergeSort(lst1)
lst2 = MergeSort(lst2)
print(lst1, lst2)