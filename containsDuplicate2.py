"""
You are given an integer array nums and an integer k, return true if there are two distinct indices i and j in the array such that nums[i] == nums[j] and abs(i - j) <= k, otherwise return false.

Example 1:

Input: nums = [1,2,3,1], k = 3

Output: true
"""
# two approaches below. Hash map and hash set

def hashmap(nums: list[int], k: int)-> bool:
    count = {}
    for i in range(len(nums)):
        if nums[i] in count and abs(count[nums[i]] - i) <= k:
            return True
        count[nums[i]] = i
    return False

def hashset(nums: list[int], k: int)-> bool:
    mp = set()
    L = 0
    for R in range(len(nums)):
        if R - L > k:
            mp.remove(nums[L])
            L += 1
        if nums[R] in mp:
            return True
        mp.add(nums[R])
    return False

        
