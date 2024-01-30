import os
import shutil
import numpy as np


import torch
import pandas as pd
import whisper
import torchaudio

from pydub import AudioSegment
import re
import heapq
import math

import whisperx
import stable_whisper
import gc 

import re
from whisper.normalizers import EnglishTextNormalizer
import jiwer


def repeated_verification(dataset_folder,model_type='whisperx', model_size='large-v2',
                    HF_token=None, device = 'cuda', precision = "float16",ERROR_thresh=1, trash_dir='./trash'):
    
    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir) 
    #if model_type =='whisperx':
    # for speed, always use whisperx
    model = whisperx.load_model(model_size, device, compute_type=precision)
    
    
    tmp = os.listdir(dataset_folder)
    normalizer = EnglishTextNormalizer()
    
    special_folder_names = ['inspection','word_time_stamp']
    for folder in tmp:
        if folder not in special_folder_names:
            trash_folder = os.path.join(trash_dir,folder)
            if os.path.exists(trash_folder):
                shutil.rmtree(trash_folder)
            os.makedirs(trash_folder) 
            files = os.listdir(os.path.join(dataset_folder,folder))
            
            txt_file = ""
            audio_file = ""
            for f in files:
                text = ""
                if f.endswith('.mp3'):
                    audio_file = f
                    txt_file = f.split('.mp3')[0]+'.txt'
                    try:
                        audio = whisperx.load_audio(os.path.join(dataset_folder,folder,audio_file))
                        gt_file = open(os.path.join(dataset_folder,folder,txt_file), "r")
                        gt = gt_file.readlines()[0]
                        result = model.transcribe(audio, batch_size=1)
                    
                        text = normalizer(result['segments'][0]['text'])
                    except:
                        pass
                    ERROR=ERROR_thresh+1
                    if not text == "":
                        ERROR = np.abs(len(text.split(' '))-len(gt.split(' ')))
                    if ERROR > ERROR_thresh:
                        shutil.move(os.path.join(dataset_folder,folder,audio_file), trash_folder)
                        shutil.move(os.path.join(dataset_folder,folder,txt_file), trash_folder)
                        print("a file is removed!!!")
                        print(os.path.join(dataset_folder,folder,audio_file))
                        
                        

                    
        
'''
repeated_verification('test/out',model_type='whisperx', model_size='large-v2',
                    HF_token=None, device = 'cuda', precision = "float16",WER_thresh=0.7)    
'''