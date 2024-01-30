import stable_whisper
import whisper_at as whisper
import os
import numpy as np

#import tensorflow

import torch
import pandas as pd

import torchaudio

DEVICE = "cuda:2" if torch.cuda.is_available() else "cpu"
model = stable_whisper.load_model("large")
model.to(DEVICE)
result = model.transcribe( '../test/tmp/RSR_0096/RSR_0096.mp3', max_instant_words=0.8)
print(result.segments[0].text)
#result.to_tsv('../test/tmp/RSR_0096/RSR_stable_seg.tsv', segment_level=True, word_level=False)
#result.to_tsv('../test/tmp/RSR_0096/RSR_stable_word.tsv', segment_level=False, word_level=True)
'''

file = open('../test/tmp/RSR_0096/RSR_stable_word.tsv')
lines = file.readlines()
pauses = []
prev = 1830

for i in range(0,len(lines),2):
    l=lines[i]
    s = float(l.strip().split('\t')[0])
    e = float(l.strip().split('\t')[1])
    if s > prev+500:
        pauses.append((l.strip().split('\t')[2], s, s-prev))
    prev=e
for p in pauses:
    print(p)

audio_tagging_time_resolution = 10

model = whisper.load_model("base")
# for large, medium, small models, we provide low-dim proj AT models to save compute.
# model = whisper.load_model("large-v1", at_low_compute=Ture)
result = model.transcribe("../test/tmp/RSR_0096/RSR_0096.mp3", at_time_res=audio_tagging_time_resolution, word_timestamps=True)
#print(result)

segments = result['segments']
for s in segments:
    print(s)

'''