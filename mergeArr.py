"""
You are given two strings, word1 and word2. Construct a new string by merging them in alternating order, starting with word1 — take one character from word1, then one from word2, and repeat this process.

If one string is longer than the other, append the remaining characters from the longer string to the end of the merged result.

Return the final merged string.

Input: word1 = "abc", word2 = "xyz"

Output: "axbycz"
"""

def merge(s1: str, s2: str) -> str:
    len1, len2 = len(s1), len(s2)
    l1, l2 = 0, 0
    res = ""
    while l1< len1 and l2 <len2:
        res += s1[l1] + s2[l2]
        l1 +=1
        l2 +=1

    while l1< len1:
        res += s1[l1]
        l1 += 1
    while l2 < len2:
        res += s2[l2]
        l2 += 1
    return res

print(merge("ab", "abbxxc"))
