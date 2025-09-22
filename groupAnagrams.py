"""
Given an array of strings strs, group all anagrams together into sublists. 
You may return the output in an order. 

Input: strs = ["act","pots","tops","cat","stop","hat"]

Output: [["hat"],["act", "cat"],["stop", "pots", "tops"]]
"""
from collections import defaultdict
class Solution:
    def anagram(self, strs: list[str]) -> list[list[str]]:
        res = defaultdict(list)

        for s in strs:
            count = [0]*26
            for c in s:
                count[ord(c) - ord("a")] += 1
            res[tuple(count)].append(s)
        return list(res.values())
    
sol = Solution()
print(sol.anagram(["act","pots","tops","cat","stop","hat"]))
