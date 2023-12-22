import re
from whisper.normalizers import EnglishTextNormalizer
import os
def preprocess_txt(file_path, in_place=True, out_path=None,normalize=True):
    file1 = open(file_path, 'r')
    Lines = file1.readlines()
    file1.close()
    
    L = []
    normalizer = EnglishTextNormalizer()
    for line in Lines:
        if '\x15' in line:
            line = line.split('\x15')[0]
        line = re.sub(r'\([^()]*\)', '', line)
        line = re.sub(r'<[^<>]*>', '', line)
        line = re.sub(r'\[[^\[\]]*\]', '', line)
        line = re.sub(r"^[a-zA-Z 0-9\.\,\'\"]","",line) 
        #normalize
        line = normalizer(line)
        
        L.append(line)
    if in_place:
        file1 = open(file_path,"w")
        for line in L:
            file1.writelines(L)
        file1.close()
    else:
        file1 = open(out_path,"w")
        for line in L:
            file1.writelines(L)
        file1.close()
            
def preprocess_dataset(folder_path, in_place=True, out_folder=None):
    # just iterate in the folder and call the individual preprocess for all txt files
    if os.path.exists(out_folder):
        shutil.rmtree(out_folder)
    os.makedirs(out_folder)  
    
    text_file_list = []
    tmp = os.listdir(folder_path)
    for f in tmp:
        if f.endswith(".txt"):
            text_file_list.append(f)
            
    for file in text_file_list:
        preprocess_txt(file, in_place=in_place, out_path=os.path.join(out_folder,file),normalize=True)