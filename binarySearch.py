"""
You are given an array of distinct integers nums, sorted in ascending order, and an integer target.

Implement a function to search for target within nums. If it exists, then return its index, otherwise, return -1.

Your solution must run in 
O
(
l
o
g
n
)
O(logn) time.

Example 1:

Input: nums = [-1,0,2,4,6,8], target = 4

Output: 3
"""

# recursive binary search

class Solution:
    def search(self, nums: list[int], target: int) -> int:
        return self.binary_search(0, len(nums) - 1, nums, target)
    
    def binary_search(self, l, r, nums, target):
        if l > r:
            return -1
        m = l + (r - l) // 2
        if nums[m] == target:
            return m
        if nums[m] < target:
            return self.binary_search(m+1, r, nums, target)
        return self.binary_search(l, m - 1, nums, target)


# iterative binary search

class Solution:
    def search(self, nums, target) -> int:
        l, r = 0, len(nums)-1
        
        while(l<=r):
            m = l + (r - l) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return -1
    