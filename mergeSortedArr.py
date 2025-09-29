"""
You are given two integer arrays nums1 and nums2, both sorted in non-decreasing order, along with two integers m and n, where:

m is the number of valid elements in nums1,
n is the number of elements in nums2.
The array nums1 has a total length of (m+n), with the first m elements containing the values to be merged, and the last n elements set to 0 as placeholders.

Your task is to merge the two arrays such that the final merged array is also sorted in non-decreasing order and stored entirely within nums1.
You must modify nums1 in-place and do not return anything from the function.

Example 1:

Input: nums1 = [10,20,20,40,0,0], m = 4, nums2 = [1,2], n = 2

Output: [1,2,10,20,20,40]
"""

def merge(nums1: list[int], nums2: list[int]) -> list[int]:
    len1, len2 = len(nums1), len(nums2)
    l, r = 0, 0
    arr = []
    while l < len1 and r < len2:
        if nums1[l] <= nums2[r]:
            arr.append(nums1[l])
            l += 1
        else:
            arr.append(nums2[r])
            r += 1
    
    while l < len1:
        arr.append(nums1[l])
        l += 1
    
    while r < len2:
        arr.append(nums2[r])
        r += 1
    return arr

print(merge([10,20,20,40], [1,2]))
