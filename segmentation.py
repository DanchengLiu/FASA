from utils.longest_matching import longest_fuzzy_matching
import os
import shutil
import re
from whisper.normalizers import EnglishTextNormalizer
import jiwer
from pydub import AudioSegment
'''
expect output format:
folder
    -segment1
        -audio.MP3
        -transcription.txt
        -word timestamps.txt (or tsv or something)
    -segment2
    ...
'''
def segment_from_prediction(dataset_folder, output_dataset_folder, delete_intermediate=False,  
                    keep_timestamp=False, export_word_timestamp=True, 
                    wer_keep_threshold=0.1, wer_check_threshold=0.3):

    normalizer = EnglishTextNormalizer()

    # create dir
    segment_root = output_dataset_folder
    check_folder = os.path.join(output_dataset_folder, 'inspection')
    if os.path.exists(segment_root):
        shutil.rmtree(segment_root)
    os.makedirs(segment_root)    
    if os.path.exists(check_folder):
        shutil.rmtree(check_folder)
    os.makedirs(check_folder)    
    if export_word_timestamp:
        wts_folder = os.path.join(output_dataset_folder, 'word_time_stamp')
        if os.path.exists(wts_folder):
            shutil.rmtree(wts_folder)
        os.makedirs(wts_folder)      
        shutil.copyfile(os.path.join(dataset_folder,'word_pred_timestamp'), os.path.join(wts_folder,'word_pred_timestamp'))         
    # processing the intermediate output 
    files = os.listdir(dataset_folder)
    
    txt_file = ""
    audio_file = ""

    for f in files:
        
        if f.endswith('.mp3'):
            audio_file = f
            txt_file = f.split('.mp3')[0]+'.txt'
    
    word_level_separation_gt = ""
    gt_file = open(os.path.join(dataset_folder,txt_file), "r")
    lines = gt_file.readlines()
    for l in lines:
        word_level_separation_gt += (l.strip()+' ')
    # regex to remove multiple space
    word_level_separation_gt = re.sub(' +', ' ', word_level_separation_gt)
    word_level_separation_gt = normalizer(word_level_separation_gt)
    word_level_separation_gt = word_level_separation_gt.split(' ')

    gt_file.close()
    
    ts_file = open(os.path.join(dataset_folder, 'sentence_pred_timestamp'), "r")
    lines = ts_file.readlines()
    ts_file.close()
    
    # start segmenting
    err_flag = False
    try:
        sound = AudioSegment.from_mp3(os.path.join(dataset_folder,audio_file))
    except:
        err_flag = True
        print(str(os.path.join(dataset_folder,audio_file)) +" has problem!")
    if not err_flag:
        for l in lines:
            # info: sentence, start, end
            info = l.strip().split('\t')
            prediction_segment = normalizer(info[0]).split(' ')

            best_index, best_length = longest_fuzzy_matching(prediction_segment,word_level_separation_gt)
            matching = word_level_separation_gt[best_index:best_index + best_length]
            
            if len(prediction_segment)>0 and len(matching)>0:
                prediction_segment = ' '.join(prediction_segment)
                matching = ' '.join(matching)
                flag=True
                try:
                    WER_LINE = jiwer.wer(matching, prediction_segment)
                except:
                    print("in file: "+audio_file)
                    print("prediction is: "+prediction_segment)
                    print("matched segment is: "+matching)
                    print("This segment is aborted.")
                    flag=False
                if flag and WER_LINE < wer_check_threshold:
                    if WER_LINE < wer_keep_threshold:
                        if keep_timestamp:
                            fd = open(os.path.join(segment_root, info[1]+'_'+info[2]+'.txt'), "w")
                            fd.write(matching+'\t'+info[1]+'\t'+info[2])
                            fd.close()
                            audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                            audio_file = audio_seg.export(os.path.join(segment_root, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                            
                            audio_file.close()
                            
                        else:
                            fd = open(os.path.join(segment_root, info[1]+'_'+info[2]+'.txt'), "w")
                            fd.write(matching)
                            fd.close()
                            audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                            audio_file = audio_seg.export(os.path.join(segment_root, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                            
                            audio_file.close()
                    else:
                        if keep_timestamp:
                            fd = open(os.path.join(check_folder, info[1]+'_'+info[2]+'.txt'), "w")
                            fd.write(matching+'\t'+info[1]+'\t'+info[2]+'\n')
                            fd.write(prediction_segment+'\t'+info[1]+'\t'+info[2]+'\n')
                            fd.close()
                            audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                            audio_file = audio_seg.export(os.path.join(check_folder, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                            
                            audio_file.close()
                        else:
                            fd = open(os.path.join(check_folder, info[1]+'_'+info[2]+'.txt'), "w")
                            fd.write(matching+'\n')
                            fd.write(prediction_segment+'\n')
                            fd.close()            
                            audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                            audio_file = audio_seg.export(os.path.join(check_folder, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                            
                            audio_file.close()  

def segment_dataset(dataset_folder, output_dataset_folder, delete_intermediate=False,  
                    keep_timestamp=False, export_word_timestamp=True, 
                    wer_keep_threshold=0.3, wer_check_threshold=0.1):
    tmp = os.listdir(dataset_folder)
    normalizer = EnglishTextNormalizer()
    
    special_folder_names = ['trash']
    for folder in tmp:
        # create dir
        if folder not in special_folder_names:
            segment_root = os.path.join(output_dataset_folder, folder)
            check_folder = os.path.join(output_dataset_folder, 'inspection', folder)
            if os.path.exists(segment_root):
                shutil.rmtree(segment_root)
            os.makedirs(segment_root)    
            if os.path.exists(check_folder):
                shutil.rmtree(check_folder)
            os.makedirs(check_folder)    
            if export_word_timestamp:
                wts_folder = os.path.join(output_dataset_folder, 'word_time_stamp', folder)
                if os.path.exists(wts_folder):
                    shutil.rmtree(wts_folder)
                os.makedirs(wts_folder)      
                shutil.copyfile(os.path.join(dataset_folder,folder,'word_pred_timestamp'), os.path.join(wts_folder,'word_pred_timestamp'))    
            
            #copy metadata
            #shutil.copyfile(os.path.join(dataset_folder,folder,'metadata'), os.path.join(wts_folder,'metadata'))      
            # processing the intermediate output 
            files = os.listdir(os.path.join(dataset_folder,folder))
            
            txt_file = ""
            audio_file = ""

            for f in files:
                
                if f.endswith('.mp3'):
                    audio_file = f
                    txt_file = f.split('.mp3')[0]+'.txt'
            
            word_level_separation_gt = ""
            gt_file = open(os.path.join(dataset_folder,folder,txt_file), "r")
            lines = gt_file.readlines()
            for l in lines:
                word_level_separation_gt += (l.strip()+' ')
            # regex to remove multiple space
            word_level_separation_gt = re.sub(' +', ' ', word_level_separation_gt)
            word_level_separation_gt = normalizer(word_level_separation_gt)
            word_level_separation_gt = word_level_separation_gt.split(' ')

            gt_file.close()
            
            ts_file = open(os.path.join(dataset_folder,folder,'sentence_pred_timestamp'), "r")
            lines = ts_file.readlines()
            ts_file.close()
            
            # start segmenting

            err_flag = False
            try:
                sound = AudioSegment.from_mp3(os.path.join(dataset_folder,folder,audio_file))
            except:
                err_flag = True
                print(str(os.path.join(dataset_folder,folder,audio_file)) +" has problem!")
            if not err_flag:
                for l in lines:
                    # info: sentence, start, end
                    info = l.strip().split('\t')
                    prediction_segment = normalizer(info[0]).split(' ')

                    best_index, best_length = longest_fuzzy_matching(prediction_segment,word_level_separation_gt)
                    matching = word_level_separation_gt[best_index:best_index + best_length]
                    
                    if len(prediction_segment)>0 and len(matching)>0:
                        prediction_segment = ' '.join(prediction_segment)
                        matching = ' '.join(matching)
                        flag=True
                        try:
                            WER_LINE = jiwer.wer(matching, prediction_segment)
                            #print(prediction_segment+'\t'+str(WER_LINE))
                        except:
                            print("in file: "+audio_file)
                            print("prediction is: "+prediction_segment)
                            print("matched segment is: "+matching)
                            print("This segment is aborted.")
                            flag=False
                        if flag and WER_LINE < wer_keep_threshold:
                            if WER_LINE < wer_check_threshold:
                                if keep_timestamp:
                                    fd = open(os.path.join(segment_root, info[1]+'_'+info[2]+'.txt'), "w")
                                    fd.write(matching+'\t'+info[1]+'\t'+info[2])
                                    fd.close()
                                    audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                                    audio_file = audio_seg.export(os.path.join(segment_root, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                                    
                                    audio_file.close()
                                    
                                else:
                                    fd = open(os.path.join(segment_root, info[1]+'_'+info[2]+'.txt'), "w")
                                    fd.write(matching)
                                    fd.close()
                                    audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                                    audio_file = audio_seg.export(os.path.join(segment_root, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                                    
                                    audio_file.close()
                            else:
                                if keep_timestamp:
                                    fd = open(os.path.join(check_folder, info[1]+'_'+info[2]+'.txt'), "w")
                                    fd.write(matching+'\t'+info[1]+'\t'+info[2]+'\n')
                                    fd.write(prediction_segment+'\t'+info[1]+'\t'+info[2]+'\n')
                                    fd.close()
                                    audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                                    audio_file = audio_seg.export(os.path.join(check_folder, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                                    
                                    audio_file.close()
                                else:
                                    fd = open(os.path.join(check_folder, info[1]+'_'+info[2]+'.txt'), "w")
                                    fd.write(matching+'\n')
                                    fd.write(prediction_segment+'\n')
                                    fd.close()            
                                    audio_seg = sound[float(info[1])*1000:float(info[2])*1000]
                                    audio_file = audio_seg.export(os.path.join(check_folder, info[1]+'_'+info[2]+'.mp3'), format="mp3") 
                                    
                                    audio_file.close()        
                    
            
            

        
        