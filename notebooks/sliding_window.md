# Sliding Window Interview Questions (Easy → Medium)

A curated set of 20 common (easy to medium) sliding window problems you should know for graduate-level software engineering / data interviews. Ordered roughly from foundational fixed-size patterns to more advanced variable-size and frequency/map-based patterns.

---
## 1. Maximum Sum of a Subarray of Size K (Difficulty: Easy)
Given an integer array and an integer K, find the maximum sum of any contiguous subarray of size K.

Pattern: Fixed-size window; slide by subtracting outgoing element and adding incoming.

Time: O(n)  | Space: O(1)

Example 1:
Input: nums = [2, 1, 5, 1, 3, 2], k = 3  
Output: 9  
Explanation: Window [5,1,3] has sum 9 (max).

Example 2:
Input: nums = [1, 2, 3, 4, 5], k = 2  
Output: 9  
Explanation: Window [4,5] → sum 9.

---
## 2. Average of All Subarrays of Size K (Difficulty: Easy)
Return a list containing the average of each contiguous subarray of size K.

Pattern: Fixed-size window; reuse running sum.

Time: O(n) | Space: O(n) (for result)

Example 1:
Input: nums = [1, 3, 2, 6, -1, 4, 1, 8, 2], k = 5  
Output: [2.2, 2.8, 2.4, 3.6, 2.8]  
Explanation: First window sum = 1+3+2+6-1 = 11 → 11/5 = 2.2.

Example 2:
Input: nums = [5, 5, 5, 5], k = 2  
Output: [5.0, 5.0, 5.0]

---
## 3. Minimum Size Subarray Sum ≥ Target (Difficulty: Easy)
Given an array of positive integers and a target S, find the minimal length of a contiguous subarray with sum ≥ S. Return 0 if none.

Pattern: Variable-size shrinking window; expand right until condition met, then shrink left.

Time: O(n) | Space: O(1)

Example 1:
Input: target = 7, nums = [2,3,1,2,4,3]  
Output: 2  
Explanation: [4,3] has length 2.

Example 2:
Input: target = 15, nums = [1,2,3,4,5]  
Output: 5  
Explanation: Whole array sums to 15.

---
## 4. Longest Substring Without Repeating Characters (Difficulty: Easy)
Return length (or substring) of the longest substring with all distinct characters.

Pattern: Variable-size window; use map of last positions or counts.

Time: O(n) | Space: O(k) (k = alphabet size)

Example 1:
Input: s = "abcabcbb"  
Output: 3 ("abc")

Example 2:
Input: s = "bbbbb"  
Output: 1 ("b")

---
## 5. Longest Substring with At Most K Distinct Characters (Difficulty: Easy-Medium)
Find the length (and optionally the substring) of the longest substring containing at most K distinct characters.

Pattern: Variable-size with frequency map; shrink when distinct count exceeds K.

Time: O(n) | Space: O(k)

Example 1:
Input: s = "eceba", k = 2  
Output: 3  
Explanation: "ece" length 3.

Example 2:
Input: s = "aa", k = 1  
Output: 2 ("aa")

---
## 6. Longest Substring with Exactly K Distinct Characters (Difficulty: Medium)
Return the length of the longest substring containing exactly K distinct characters.

Pattern: Use at most K twice or maintain two windows (atMostK(k) - atMostK(k-1)).

Time: O(n) | Space: O(k)

Example 1:
Input: s = "aabacbebebe", k = 3  
Output: 7 ("cbebebe")

Example 2:
Input: s = "aaabb", k = 2  
Output: 5 ("aaabb")

---
## 7. Fruit Into Baskets (At Most 2 Distinct) (Difficulty: Easy)
Given a list of tree types, pick the longest subarray containing at most 2 distinct values.

Pattern: At most K distinct where K = 2.

Time: O(n) | Space: O(1) (since K=2)

Example 1:
Input: trees = [1,2,1]  
Output: 3

Example 2:
Input: trees = [0,1,2,2]  
Output: 3 (subarray [1,2,2])

---
## 8. Permutation in String (Contains An Anagram) (Difficulty: Easy-Medium)
Given strings s1 and s2, return true if s2 contains a permutation (anagram) of s1.

Pattern: Fixed-size char frequency comparison; sliding updates.

Time: O(n) | Space: O(1) (fixed alphabet)

Example 1:
Input: s1 = "ab", s2 = "eidbaooo"  
Output: true ("ba")

Example 2:
Input: s1 = "ab", s2 = "eidboaoo"  
Output: false

---
## 9. Count Occurrences of Anagrams (Difficulty: Medium)
Given pattern p and text s, count how many substrings of s are an anagram of p.

Pattern: Sliding window frequency + match count.

Time: O(n) | Space: O(1)

Example 1:
Input: s = "cbaebabacd", p = "abc"  
Output: 2 ("cba", "bac")

Example 2:
Input: s = "abab", p = "ab"  
Output: 3 (positions 0,1,2)

---
## 10. First Negative Number in Every Window of Size K (Difficulty: Easy)
Return the first negative number in each contiguous window of size K (or 0 / None if none).

Pattern: Fixed-size with deque storing indices of negatives.

Time: O(n) | Space: O(k) (worst)

Example 1:
Input: arr = [12, -1, -7, 8, -15, 30, 16, 28], k = 3  
Output: [-1, -1, -7, -15, -15, 0]

Example 2:
Input: arr = [5, 10, 15], k = 2  
Output: [0, 0]

---
## 11. Distinct Elements in Every Window of Size K (Difficulty: Medium)
Return a list containing the number of distinct elements for each window of size K.

Pattern: Fixed-size with hashmap of counts.

Time: O(n) | Space: O(k)

Example 1:
Input: arr = [1,2,1,3,4,2,3], k = 4  
Output: [3,4,4,3]

Example 2:
Input: arr = [1,1,1,1], k = 2  
Output: [1,1,1]

---
## 12. Sliding Window Maximum (Difficulty: Medium)
Given an array and window size K, return the maximum for each window.

Pattern: Monotonic deque storing decreasing indices.

Time: O(n) | Space: O(k)

Example 1:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3  
Output: [3,3,5,5,6,7]

Example 2:
Input: nums = [9,8,7,6,5], k = 2  
Output: [9,8,7,6]

---
## 13. Number of Subarrays with Sum Exactly K (Positive Integers) (Difficulty: Medium)
Given an array of positive integers and target K, count contiguous subarrays summing to K.

Pattern: Variable window; shrink when sum ≥ K; careful counting for positives only.

Time: O(n) | Space: O(1)

Example 1:
Input: nums = [1,1,1], k = 2  
Output: 2 ([1,1] at indices (0,1) and (1,2))

Example 2:
Input: nums = [2,3,5,1,1], k = 5  
Output: 2 ([5], [2,3])

---
## 14. Binary Subarrays With Sum (Difficulty: Medium)
Binary array nums and integer goal; count subarrays with sum = goal.

Pattern: At most sum technique: count(atMost(goal)) - count(atMost(goal-1)).

Time: O(n) | Space: O(1)

Example 1:
Input: nums = [1,0,1,0,1], goal = 2  
Output: 4

Example 2:
Input: nums = [0,0,0,0], goal = 0  
Output: 10 (all subarrays)

---
## 15. Longest Ones After Flipping At Most K Zeros (Difficulty: Medium)
Return the length of the longest subarray containing only 1s after flipping at most K zeros.

Pattern: Variable window; track zero count; shrink when zeros > K.

Time: O(n) | Space: O(1)

Example 1:
Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2  
Output: 6

Example 2:
Input: nums = [0,0,1,1,0,1,1,1,0], k = 3  
Output: 9

---
## 16. Longest Repeating Character Replacement (Difficulty: Medium)
Given a string s and integer k, you can replace at most k characters to make all chars in the window identical. Return max length.

Pattern: Track max frequency in window; shrink when window_size - max_freq > k.

Time: O(n) | Space: O(1)

Example 1:
Input: s = "ABAB", k = 2  
Output: 4

Example 2:
Input: s = "AABABBA", k = 1  
Output: 4 ("AABA" or "ABBA")

---
## 17. Minimum Window Substring (Difficulty: Medium)
Given strings s and t, return the smallest substring of s containing all characters of t (with multiplicity). If none, return "".

Pattern: Expand to satisfy all required counts; shrink to minimize.

Time: O(n) | Space: O(k)

Example 1:
Input: s = "ADOBECODEBANC", t = "ABC"  
Output: "BANC"

Example 2:
Input: s = "a", t = "aa"  
Output: "" (impossible)

---
## 18. Subarrays with K Different Integers (Difficulty: Medium)
Count subarrays with exactly K distinct integers.

Pattern: atMost(K) - atMost(K-1)

Time: O(n) | Space: O(k)

Example 1:
Input: nums = [1,2,1,2,3], k = 2  
Output: 7

Example 2:
Input: nums = [1,2,1,3,4], k = 3  
Output: 3 ([1,2,1,3], [2,1,3], [1,3,4])

---
## 19. Count of Subarrays with At Most K Distinct (Helper Pattern) (Difficulty: Medium)
Return the number of subarrays containing at most K distinct elements (often used as helper for Exactly-K problems).

Pattern: Maintain map of counts; result accumulates window length each step.

Time: O(n) | Space: O(k)

Example 1:
Input: nums = [1,2,1,2,3], k = 2  
Output: 12

Example 2:
Input: nums = [1,2,3], k = 1  
Output: 3 ([1],[2],[3])

---
## 20. Maximum Sum of Distinct Subarray of Length K (Difficulty: Medium)
Given an integer array and K, find the maximum sum among all subarrays of size K that contain only distinct elements. If a window contains duplicates, skip it.

Pattern: Fixed-size + frequency map; if duplicate appears, shrink from left until unique or window broken; track sum only when window size == K with distinctness.

Time: O(n) | Space: O(k)

Example 1:
Input: nums = [5,2,3,5,4,3], k = 3  
Output: 12  
Explanation: Window [5,2,3] sum=10, [2,3,5] sum=10, [3,5,4] sum=12 (valid, distinct). [5,4,3] also 12.

Example 2:
Input: nums = [1,1,1,1], k = 2  
Output: 0  
Explanation: No window of size 2 has distinct elements.

---
## Core Patterns Summary
- Fixed-size window: maintain sum / frequency; move both ends together.
- Variable-size expanding/shrinking: expand right, shrink left on violation.
- Frequency maps + distinct constraints: at most / exactly K distinct (helper decomposition). 
- Deques: monotonic queue for max/min per window.
- Prefix / combinational counting: transform exactly-K into atMost(K) - atMost(K-1).

Mastering these lets you tackle most sliding window interview problems efficiently.

---
Happy practicing! Add implementations next to each to solidify understanding.

---
## Added (Requested) Problems & Clarifications

The following items address specific problems you asked to verify / include:

### A. Find All Anagrams in a String (Already Included)
Covered as: 9. Count Occurrences of Anagrams — same core task (find/count all anagram substrings). If you also need a pure boolean variant ("does at least one exist?"), that is Problem 8 (Permutation in String).

### B. Longest Substring with At Most K Distinct Characters (Already Included)
Covered as: 5. Longest Substring with At Most K Distinct Characters.

### C. Count Number of Nice Subarrays (NEW) (Difficulty: Medium)
Problem: Given nums (integers) and k, return the number of subarrays with exactly k odd numbers.

Pattern: Transform into atMost(k) - atMost(k-1), where atMost(x) counts subarrays with at most x odds. Identical pattern to "subarrays with exactly K distinct" but using a counter of odds instead of a hashmap.

Time: O(n) | Space: O(1)

Example 1:
Input: nums = [1,1,2,1,1], k = 3  
Odds windows with 3 odds → 2 (subarrays [1,1,2,1], [1,2,1,1])  
Output: 2

Example 2:
Input: nums = [2,2,2,1,2], k = 1  
Output: 4  
Explanation: Each subarray containing exactly one odd (the single 1) in each possible window around it.

### D. Max Consecutive Ones II (Explicit Variant) (Difficulty: Easy-Medium)
Problem: Given a binary array, return the maximum number of consecutive 1s if you can flip at most one 0.

Relation: This is a special case of Problem 15 (Longest Ones After Flipping At Most K Zeros) with K = 1. Listing separately for clarity since it's a common standalone LeetCode question.

Time: O(n) | Space: O(1)

Example 1:
Input: nums = [1,0,1,1,0]  
Output: 4  
Explanation: Flip the second 0 → [1,0,1,1,1] or flip first 0 for similar stretch.

Example 2:
Input: nums = [0,0,0,1]  
Output: 2 (flip one of the zeros adjacent to the 1 forming [0,1] or [1,0])

### E. Sliding Window Median (Advanced) (Difficulty: Hard Edge of Medium)
Problem: Given an array nums and window size k, return the median of each sliding window.

Why Included: Although beyond the original easy→medium scope, it's a classic extension introducing balanced multisets / two-heaps with deletion support.

Approach Patterns:
- Two Heaps (max-heap for lower half, min-heap for upper half) + delayed deletion hash.
- Balanced BST / multiset (languages with ordered multiset support).
- Order Statistics Tree / Indexed Balanced Structure.

Time: O(n log k) | Space: O(k)

Example 1:
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3  
Output: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]  
Explanation: Medians of each window.

Example 2:
Input: nums = [5,2,2,7,3,7,9,0,2,3], k = 2  
Output: [3.5,2.0,4.5,5.0,5.0,8.0,4.5,1.0,2.5]

---
If you’d like, we can now add Python reference implementations for any subset (e.g., Nice Subarrays or Sliding Window Median). Let me know which to prioritize.
