# Defensive File Scanner

## Concept

Scanner large files for excessive null bits.
Malware is getting around computer security by not scanning large files, but bloating them out with 0 bytes.
Find a way to predict the likelihood of a file being malware by the presence of these bytes without slowing down the pc.

## Approach

1. [x] Scan whole file.
1. [ ] Test random lines of code with a good spread of the program.
1. [ ] Determine the average sum of bits in a file for a given size.
1. [ ] Calculate the sum of the file.
1. [ ] Remove the null bits and check with virus total.

## Questions

- Do the SHASUM of bloated programs have some identifiable part?
- Can you read set parts of a program without reading the whole file?
- What is the quickest way to work out if it is shady?
- What is the ratio of `0x00` bytes that are not normal?

## Requirements

1. Time taken to assess large files <1ms.
1. Scan does not detonate the program.
1. True Positive > 90%
1. False positive < 10%
