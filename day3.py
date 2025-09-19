"""
Valid Anagram:
Given two strings s and t, return true if the two string s are anagrams of each other, otherwise return false
"""
# solution with sorted()
# class Solution:
#     def anagrams(self, s: str, t: str) -> bool:
#         if len(s) != len(t):
#             return False
#         return sorted(s) == sorted(t)
    
# sol = Solution()
# print(sol.anagrams("racecar", "carrace"))
# this solution is O(nlogn + mlogm) 

class Solution:
    def anagrams(self, s: str, t: str) -> bool:
        countS, countT = {},{}

        if len(s) != len(t):
            return False
        for i in range(len(s)):
            countS[s[i]] = 1 + countS.get(s[i], 0)
            countT[t[i]] = 1 + countT.get(t[i], 0)
        
        return countS == countT
    
