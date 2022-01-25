# Running the code

---

Clone the project and edit test case in `Line 20 & 21` as the shown below

```python
wordList = ["ab","ab"]
target = "abab"
```

After edited test case. Use the following command for running the code.

```shell
python solve.py
```

The result will be printed to terminal as the picture below.\
\
![Screenshot 2022-01-15 212003](https://user-images.githubusercontent.com/52927525/149624969-33155578-1f0a-46ba-aa7f-c4dcf29b10fc.png)

# Time Complexity Analysis

---
Given m is wordList length , n is a number of target characters

Using dictionary as the data structure. Find/Edit in dictionary cost O(1). Loop all target characters,  

So that,

Time Complexity in Time : O(n) * O(1) = O(n)  
Time Complexity in Space : O(m) * O(1) = O(m)