"""
You are given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

You must write an algorithm with O(log n) runtime complexity.

Example 1:

Input: nums = [-1,0,2,4,6,8], target = 5

Output: 4
"""

class Solution:
    def searchInsert(self, nums, target)-> int:
        l,r = 0 , len(nums) -1

        while l<=r:
            m = l + (r - l) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m +1
            else:
                r = m - 1
        return l