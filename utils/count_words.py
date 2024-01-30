import os

import os
wc = 0 
rd = '../test/out/760'
for file in os.listdir(rd):
    if file.endswith(".txt"):
        tmp = open(os.path.join(rd, file), "r")
        contents = tmp.read()
        tmp.close()

        word_list = contents.split()
        num_words = len(word_list)
        wc+=num_words
print(wc)