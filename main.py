import argparse
import os
import whisperx
import gc 

from prediction import predict_dataset, predict_one_file
from segmentation import segment_dataset, segment_from_prediction
from preprocess import preprocess_dataset, preprocess_txt
from user_intervention import run_user_intervention_app

parser = argparse.ArgumentParser(description='FASA Toolkit v1.0')


parser.add_argument('-i', '--input_data', required=True, help='input file or input dataset directory')
parser.add_argument('-o', '--output_data', required=True, help='output file or output dataset directory')


parser.add_argument('-inter', '--intermediate', required=True, help='specify the path to store intermediate files here')
parser.add_argument('-delete_inter', '--delete_intermediate', choices=['True', 'False'], required=False, default='False', help='whether to keep the intermediate files (default to True)')

parser.add_argument('-pre', '--preprocess', choices=['True', 'False'], required=False, default='False', help='preprocess the dataset using RegEx (default to False)')
parser.add_argument('-pre_loc', '--preprocess_output_location', required=False, help='specify the path to store the preprocessed transcriptions. If not specified, preprocess with overwrite the original files')
parser.add_argument('-m', '--model', choices=['whisper', 'whisperx'], required=False, default='whisperx', help='select model used in the pipeline (default to whisperX)')
parser.add_argument('-s', '--size', choices=['large-v1', 'large-v2', 'large-v3'], default='large-v2', required=False, help='select model size (default to large-v2)')
parser.add_argument('-HF', required=False, help='HF token required by diarization model (suppressed)')

parser.add_argument('-d', '--device', required=False, default='cuda', help='device used by the model(default to cuda)')
parser.add_argument('-p', '--precision', choices=['float16', 'int8'], default='float16', required=False, help='precision used by the model (default to float16)')

parser.add_argument('-word', '--word_level_alignment', choices=['True', 'False'], required=False, default='True', help='output the word level alignment timestamps from prediction (default to True)')

parser.add_argument('-ts', '--timestamp', choices=['True', 'False'], required=False, default='False', help='keep the timestamps of the segmented outputs in the original audio (default to False)')

parser.add_argument('-wer_K', '--wer_keep_segment', type=float, required=False, default=0.3, help='WER threshold to keep the segment when comparing from the provided transcription without need to check (default to 0.1)')
parser.add_argument('-wer_C', '--wer_check_segment', type=float, required=False, default=0.1, help='WER threshold to keep the segment when comparing from the provided transcription, but with checking (default to 0.3)')
parser.add_argument('-c', '--check', choices=['True', 'False'], required=False, default='True', help='launch the checking interface after segmentation is done (default to True)')



if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    
    
    #HF_token = "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"
    
    #audio_file = "../data/databank/Narrative/758.mp3"
    
    pred_out_dir = './pred_dataset'
    seg_out_dir = './processed_dataset'
    
    device = "cuda" 
    word_level_alignment = True
    timestamp=True
    check=True 
    delete_intermediate=True
    if args.word_level_alignment=='False':
        word_level_alignment = False
    if args.timestamp=='False':
        timestamp = False    
  
    if args.delete_intermediate=='False':
        delete_intermediate = False   
    '''
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    WARNING: do not call preprocess on languages other than English!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    '''
    #preprocess
    in_files = args.input_data
    
    if os.path.isdir(in_files):
        if args.preprocess=='True':
            if args.preprocess_output_location != None:
                preprocess_dataset(args.input_data, in_place=False, out_folder = args.preprocess_output_location)
                in_files = args.preprocess_output_location
            else:
                preprocess_dataset(args.input_data, in_place=True, out_folder = None)
        
        #prediction
        #predict_dataset(in_files, args.intermediate, model_type=args.model, HF_token=args.HF, 
        #                device=args.device, precision=args.precision, word_level=word_level_alignment)
        
        #alignment
        #segment_dataset(args.intermediate,args.output_data, delete_intermediate=delete_intermediate, 
        #                keep_timestamp=timestamp, export_word_timestamp=word_level_alignment, 
        #                wer_keep_threshold=args.wer_keep_segment, wer_check_threshold=args.wer_check_segment)
        
        #checking
        if args.check=='True':
            run_user_intervention_app(args.output_data)
        
        
    elif os.path.isfile(in_files):
        if args.preprocess=='True':
            if args.preprocess_output_location != None:
                preprocess_txt(args.input_data, in_place=False, out_path = args.preprocess_output_location)
                in_files = args.preprocess_output_location
            else:
                preprocess_txt(args.input_data, in_place=True, out_path = None)
        
        #prediction
        predict_one_file(in_files, args.intermediate, model_type=args.model, HF_token=args.HF, 
                        device=args.device, precision=args.precision, word_level=word_level_alignment)
        
        #alignment
        segment_from_prediction(args.intermediate,args.output_data, delete_intermediate=delete_intermediate, 
                        keep_timestamp=timestamp, export_word_timestamp=word_level_alignment, 
                        wer_keep_threshold=args.wer_keep_segment, wer_check_threshold=args.wer_check_segment)
        
        #checking
        if args.check=='True':
            run_user_intervention_app(args.output_data)
