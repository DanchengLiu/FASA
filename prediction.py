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
# return the word-level timestamps of an audio file
'''
model takes: ['whisper','whisperx']
'''
def predict_one_file(audio_file_path, out_dir, model_type='whisperx', model_size='large-v2',
                    HF_token=None, device = 'cuda', precision = "float16", LANG = ['en'],
                    sentence_level=True, word_level=True, **args):
    if model_type =='whisperx':
        model = whisperx.load_model(model_size, device, compute_type=precision)
        
        
        
        audio_file = audio_file_path
        text_file = audio_file_path.split('.mp3')[0]+'.txt'
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=1)
        
        # prediction
        if result['language'] in LANG:
            model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
            result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
            
            sentence_level_alignment = []
            word_level_alignment = []
            # out dir full path
            segment_root = out_dir
            if os.path.exists(segment_root):
                shutil.rmtree(segment_root)
            os.makedirs(segment_root)
            # copy provided GT over
            shutil.copyfile(text_file, os.path.join(segment_root,os.path.basename(text_file)))
            shutil.copyfile(audio_file, os.path.join(segment_root,os.path.basename(audio_file)))
            for segment in result['segments']:
            
                sentence_level_alignment.append(segment['text']+'\t'+str(segment['start'])+'\t'+str(segment['end']))
                
                for word in segment['words']:
                    
                    # it should be noted that on rare cases, a word does not have alignment (e.g $5)
                    if 'start' in word.keys() and 'end' in word.keys():
                        word_level_alignment.append(word['word']+'\t'+str(word['start'])+'\t'+str(word['end']))
                    
            

            if sentence_level:
                fd = open(os.path.join(segment_root, 'sentence_pred_timestamp'), "w")
                for l in sentence_level_alignment:
                    fd.write(l+'\n')
                fd.close()
            if word_level:
                fd = open(os.path.join(segment_root, 'word_pred_timestamp'), "w")
                for l in word_level_alignment:
                    fd.write(l+'\n')
                fd.close()   

def predict_dataset(audio_folder_path, out_dir, model_type='whisperx', model_size='large-v2',
                    HF_token=None, device = 'cuda', precision = "float16", LANG = ['en'],
                    sentence_level=True, word_level=True, **args):
    # first, obtain audio and text lists
    audio_file_list = []
    text_file_list = []
    tmp = os.listdir(audio_folder_path)
    for f in tmp:
        if f.endswith(".mp3"):
            name = f.split('.mp3')[0]
            if name+'.txt' in tmp:
                audio_file_list.append(f)
                text_file_list.append(name+'.txt')
                
                
    if model_type =='whisperx':
        model = whisperx.load_model(model_size, device, compute_type=precision)
        
        
        for item in range(len(audio_file_list)):
            audio_file = audio_file_list[item]
            text_file = text_file_list[item]
            audio = whisperx.load_audio(os.path.join(audio_folder_path,audio_file))
            result = model.transcribe(audio, batch_size=1)
            
            # prediction
            if result['language'] in LANG:
                model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
                result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
                
                sentence_level_alignment = []
                word_level_alignment = []
                # out dir full path
                segment_root = os.path.join(out_dir,audio_file.split('.mp3')[0])
                if os.path.exists(segment_root):
                    shutil.rmtree(segment_root)
                os.makedirs(segment_root)
                # copy provided GT over
                shutil.copyfile(os.path.join(audio_folder_path,audio_file.split('.mp3')[0]+'.txt'), os.path.join(segment_root,audio_file.split('.mp3')[0]+'.txt'))
                shutil.copyfile(os.path.join(audio_folder_path,audio_file), os.path.join(segment_root,audio_file))
                for segment in result['segments']:
                
                    sentence_level_alignment.append(segment['text']+'\t'+str(segment['start'])+'\t'+str(segment['end']))
                    
                    for word in segment['words']:
                        
                        # it should be noted that on rare cases, a word does not have alignment (e.g $5)
                        if 'start' in word.keys() and 'end' in word.keys():
                            word_level_alignment.append(word['word']+'\t'+str(word['start'])+'\t'+str(word['end']))
                        
                

                if sentence_level:
                    fd = open(os.path.join(segment_root, 'sentence_pred_timestamp'), "w")
                    for l in sentence_level_alignment:
                        fd.write(l+'\n')
                    fd.close()
                if word_level:
                    fd = open(os.path.join(segment_root, 'word_pred_timestamp'), "w")
                    for l in word_level_alignment:
                        fd.write(l+'\n')
                    fd.close()                
                
    elif model_type =='whisper':
        model = stable_whisper.load_model("large", device)
        #model = stable_whisper.load_faster_whisper('large',device=device)
        #model.to(device)
        
        
        for item in range(len(audio_file_list)):
            audio_file = audio_file_list[item]
            text_file = text_file_list[item]
            result = model.transcribe(os.path.join(audio_folder_path,audio_file), max_instant_words=0.8)
            #result = model.transcribe(os.path.join(audio_folder_path,audio_file))
            #adjust max number of words here for length purposes (max_words=)
            result = result.merge_by_gap(2.0,max_words=15, is_sum_max=True)
            
            # prediction
            if result.language in LANG:
                ###
                
                sentence_level_alignment = []
                word_level_alignment = []
                # out dir full path
                segment_root = os.path.join(out_dir,audio_file.split('.mp3')[0])
                if os.path.exists(segment_root):
                    shutil.rmtree(segment_root)
                os.makedirs(segment_root)
                # copy provided GT over
                shutil.copyfile(os.path.join(audio_folder_path,audio_file.split('.mp3')[0]+'.txt'), os.path.join(segment_root,audio_file.split('.mp3')[0]+'.txt'))
                shutil.copyfile(os.path.join(audio_folder_path,audio_file), os.path.join(segment_root,audio_file))
                for segment in result.segments:
                
                    sentence_level_alignment.append(segment.text+'\t'+str(segment.start)+'\t'+str(segment.end))
                    
                    for word in segment.words:
                        
                        # it should be noted that on rare cases, a word does not have alignment (e.g $5)
                        try:
                        
                            word_level_alignment.append(word.word+'\t'+str(word.start)+'\t'+str(word.end))
                        except:
                            print("a word does not have start or end.")
                        
                

                if sentence_level:
                    fd = open(os.path.join(segment_root, 'sentence_pred_timestamp'), "w")
                    for l in sentence_level_alignment:
                        fd.write(l+'\n')
                    fd.close()
                if word_level:
                    fd = open(os.path.join(segment_root, 'word_pred_timestamp'), "w")
                    for l in word_level_alignment:
                        fd.write(l+'\n')
                    fd.close()   
    else:
        raise Exception("Sorry, model requested not supported")
                
                