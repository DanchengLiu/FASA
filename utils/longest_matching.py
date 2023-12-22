from Levenshtein import distance
'''
def longest_matching(str2,str1, match_score=2, mismatch_penalty=1, gap_penalty=1):
    # Initialize the scoring matrix
    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    
    # Initialize variables to keep track of the maximum score and its position
    max_score = 0
    max_i, max_j = 0, 0
    
    # Fill in the scoring matrix
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                score = matrix[i - 1][j - 1] + match_score
            else:
                score = max(
                    matrix[i - 1][j] + gap_penalty,
                    matrix[i][j - 1] + gap_penalty,
                    matrix[i - 1][j - 1] + mismatch_penalty,
                )
            
            matrix[i][j] = max(0, score)  # Ensure no negative scores
            if matrix[i][j] > max_score:
                max_score = matrix[i][j]
                max_i, max_j = i, j
    
    # Traceback to find the aligned substrings
    aligned_str1, aligned_str2 = [], []
    i, j = max_i, max_j
    while i > 0 and j > 0:
        if matrix[i][j] == matrix[i - 1][j - 1] + match_score and str1[i - 1] == str2[j - 1]:
            aligned_str1.append(str1[i - 1])
            aligned_str2.append(str2[j - 1])
            i -= 1
            j -= 1
        elif matrix[i][j] == matrix[i - 1][j - 1] + mismatch_penalty:
            aligned_str1.append(str1[i - 1])
            aligned_str2.append(str2[j - 1])
            i -= 1
            j -= 1
        elif matrix[i][j] == matrix[i - 1][j] + gap_penalty:
            aligned_str1.append(str1[i - 1])
            aligned_str2.append('-')
            i -= 1
        else:
            aligned_str1.append('-')
            aligned_str2.append(str2[j - 1])
            j -= 1

    # Extract the longest approximate matching substring
    longest_substring1 = ' '.join(reversed(aligned_str1))
    longest_substring2 = ' '.join(reversed(aligned_str2))
    
    return longest_substring1, longest_substring2
'''

def longest_fuzzy_matching(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)

    min_distance = float('inf')
    best_index = 0
    best_length = 0

    for i in range(len_str2):
        k = 0

        while i + k < len_str2 and k < len_str1:
            substring2 = str2[i:i + k + 1]

            # Calculate the edit distance between str1 and the current substring of str2
            current_distance = distance(str1, substring2)

            # Update the best index and length if the current distance is smaller
            if current_distance < min_distance:
                min_distance = current_distance
                best_index = i
                best_length = k + 1  # k + 1 is the length of the current substring

            k += 1

    return best_index, best_length


