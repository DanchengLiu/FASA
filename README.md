# FASA installation
pip install -r requirements.txt 

pip install git+https://github.com/m-bain/whisperx.git@78dcfaab51005aa703ee21375f81ed31bc248560

# ASR-UI Installation
node version: 16.14.0

Angular CLI: 10.2.1

steps to setup Angular project:

navidate to ASR-UI folder:

npm install

ng build --prod

Note that the authors are aware difficulties setting up the web UI. If this really does not work out, modify main a little bit by deleteing the checking module.


# FASA Usage
FASA toolkit for ASR dataset alignment

usage: main.py [-h] -i INPUT_DATA -o OUTPUT_DATA -inter INTERMEDIATE [-t TRASH] [-delete_inter {True,False}] [-pre {True,False}] [-pre_loc PREPROCESS_OUTPUT_LOCATION]
               [-m {whisper,whisperx}] [-s {large-v1,large-v2,large-v3}] [-HF HF] [-d DEVICE] [-p {float16,int8}] [-word {True,False}] [-ts {True,False}] [-wer_K WER_KEEP_SEGMENT]
               [-wer_C WER_CHECK_SEGMENT] [-err_R ERROR_REPEAT_SEGMENT] [-c {True,False}] [-r {True,False}]

FASA Toolkit v1.3

optional arguments:
  -h, --help            show this help message and exit
  
  -i INPUT_DATA, --input_data INPUT_DATA
                        input file or input dataset directory

  -o OUTPUT_DATA, --output_data OUTPUT_DATA
                        output file or output dataset directory

  -inter INTERMEDIATE, --intermediate INTERMEDIATE
                        specify the path to store intermediate files here

  -t TRASH, --trash TRASH
                        specify the path to keep trash files (in case you need them)

  -delete_inter {True,False}, --delete_intermediate {True,False}
                        whether to keep the intermediate files (default to True)

  -pre {True,False}, --preprocess {True,False}
                        preprocess the dataset using RegEx (default to False)

  -pre_loc PREPROCESS_OUTPUT_LOCATION, --preprocess_output_location PREPROCESS_OUTPUT_LOCATION
                        specify the path to store the preprocessed transcriptions. If not specified, preprocess with overwrite the original files

  -m {whisper,whisperx}, --model {whisper,whisperx}
                        select model used in the pipeline (default to whisperX)

  -s {large-v1,large-v2,large-v3}, --size {large-v1,large-v2,large-v3}
                        select model size (default to large-v2)

  -HF HF                HF token required by diarization model (suppressed)

  -d DEVICE, --device DEVICE
                        device used by the model(default to cuda)

  -p {float16,int8}, --precision {float16,int8}
                        precision used by the model (default to float16)

  -word {True,False}, --word_level_alignment {True,False}
                        output the word level alignment timestamps from prediction (default to True)

  -ts {True,False}, --timestamp {True,False}
                        keep the timestamps of the segmented outputs in the original audio (default to False)

  -wer_K WER_KEEP_SEGMENT, --wer_keep_segment WER_KEEP_SEGMENT
                        WER threshold to keep the segment when comparing from the provided transcription without need to check (default to 0.1)

  -wer_C WER_CHECK_SEGMENT, --wer_check_segment WER_CHECK_SEGMENT
                        WER threshold to keep the segment when comparing from the provided transcription, but with checking (default to 0.3)

  -err_R ERROR_REPEAT_SEGMENT, --error_repeat_segment ERROR_REPEAT_SEGMENT
                        length error threshold for repeated verification in case model has some problems in the first iteration (default to 1.0)

  -c {True,False}, --check {True,False}
                        launch the checking interface after segmentation is done (default to True)
                        
  -r {True,False}, --repeat {True,False}
                        lconduct repeated checking to make sure model is doing correct things (default to True)



# Example Usage
python -u main.py -i ./test/raw/ -o ./test/outx -inter ./test/tmpx -c False -m whisperx -d cuda

# A note to the users
There were some merge conflicts, and we are not sure if everything is correct with this branch on GitHub. If there are any issues, let us know.
