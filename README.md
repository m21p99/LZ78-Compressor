# A Python LZ78-Compressor

A simplified implementation of the LZ78 compression algorithm in python.

## Dependencies

```bash
$ pip install bitarray
```

## Implementation

The design of data storage format:

| prefixIndex | character |
| ----------- | --------- |
| 12 bits     | 8 bits    |

The **prefixIndex** occupy 12 bits space and **character** occupy 8 bits space.

If character has not been added into table, we set the prefixIndex to 0, and then add the character after prefixIndex. If character/substring has existed in table, we continue to search the substring until find a new substring which has not been added, then record the index of last existing substring in prefixIndex and set the character as the last character of the new substring. If data string has been searched to the end and the substring/character is still existing, then we record the index of existing substring in prefixIndex to make a link to point to it, and leave the character segment empty.

## Result

`source_data.txt`, a file containing some test text (size: *14455 bytes*)

`compressed_data.lz78`, a compressed output of `source_data.txt` using LZ78 algorithm (size: *9138 bytes*, compression rate is about **36.7831200277%**)

`decompressed_data.txt`, the decompressed file back to its original form (size: *14455 bytes*)

**The partial output of compression description:**

```bash
<0, I>
<0, n>
<0, t>
<0, r>
<0, o>
<0, d>
<0, u>
<0, c>
<3, i>
<5, n>
<0,  >
<3, o>
<11, d>
<0, a>
<3, a>
<11, c>
<5, m>
<0, p>
<4, e>
<0, s>
<20, i>
<0, \n>
<23, I>
<2,  >
<3, h>
<0, e>
<11, l>
<14, s>
<3,  >
<6, e>
<8, a>
<32, ,>
<11, w>
<28,  >
<0, h>
<14, v>
<36, b>
<28, e>
<26, w>
<0, i>
<3, n>
<28, s>
<21, n>
<0, g>
<11, a>
<11, t>
<4, a>
<2, s>
<0, f>
<5, r>
<0, m>
<14, t>
<42, o>
...
```

## Reference

*[1] Ziv, Jacob, and Abraham Lempel. "Compression of individual sequences via variable-rate coding." IEEE transactions on Information Theory 24.5 (1978): 530-536.*

*[2\] [LZ78算法原理及实现](http://www.cnblogs.com/en-heng/p/6283282.html)*

*[3\] [A Python LZ77-Compressor](https://github.com/manassra/LZ77-Compressor/)*