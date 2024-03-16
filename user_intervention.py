import argparse
import webbrowser
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json
app = Flask(__name__, static_folder='./ASR-UI/dist/ASR-UI', static_url_path='/')
#CORS(app)

# dataset path as a global variable
dataset_path = None
output_data= None

def read_transcription_file(transcription_file_path):
    with open(transcription_file_path, 'r') as file:
        return file.read().splitlines()

def get_answers():
    # Read answers from ./dataset/answers.json
    answers_file_path = os.path.join(dataset_path, 'answers.json')
    if os.path.exists(answers_file_path):
        with open(answers_file_path, 'r') as answers_file:
            answers_data = json.load(answers_file)
        return answers_data
    else:
        return {}


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/play/<path:mp3_file>')
def play_mp3(mp3_file):
    mp3_path = os.path.join(dataset_path, mp3_file)
    if os.path.isfile(mp3_path):
        return send_from_directory(dataset_path, mp3_file)
    else:
        return "File not found", 404

@app.route('/save_transcription', methods=['POST'])
def save_transcription():
    data= request.json
    # Get typed answer from text input
    mp3_file = data.get('mp3_file', '')
    my_answer = data.get('myAnswer', '')

    # Read or initialize the answers JSON file
    answers_file_path = os.path.join(dataset_path, 'answers.json')
    try:
        with open(answers_file_path, 'r') as answers_file:
            answers = json.load(answers_file)
    except (json.JSONDecodeError, FileNotFoundError):
    # If the file is not found, create an empty dictionary
        answers = {}
        with open(answers_file_path, 'w') as new_file:
            json.dump(answers, new_file)

    # Update or add the answer for the current file
    answers[mp3_file] = my_answer

    # Save the updated answers back to the JSON file
    with open(answers_file_path, 'w') as answers_file:
        json.dump(answers, answers_file, indent=2)

    return jsonify({'message': 'Transcription saved successfully'}), 200


@app.route('/api/mp3_files')
def get_mp3_files(): 
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))

    mp3_files = []
    answers_data = get_answers()

    # Iterate through the dataset directory and collect MP3 files
    # dataset_path = '../dataset'
    for folder in os.listdir(dataset_path):
        folder_path = os.path.join(dataset_path, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('.mp3'):
                    mp3_file = os.path.join(folder, file)  # Include the folder in the path
                    transcription_file = file.replace('.mp3', '.txt')
                    transcription_file_path = os.path.join(folder_path, transcription_file)
                    transcription_lines = read_transcription_file(transcription_file_path)
                    answer = answers_data.get(mp3_file, '')

                    mp3_files.append({
                        'mp3_file': mp3_file,
                        'transcription_lines': transcription_lines,
                        'answer': answer
                    })

    start_index = (page - 1) * per_page
    end_index = page * per_page
    return jsonify(mp3_files[start_index:end_index])

#code for writing back to transcription files
def write_answer_to_transcription(answer, transcription_file_path):
    print(os.path.join(dataset_path,transcription_file_path))
    print(os.path.join(output_data, transcription_file_path))
    os.rename(os.path.join(dataset_path,transcription_file_path) , os.path.join(output_data, transcription_file_path))
    print(os.path.join(output_data, transcription_file_path)[:-4]+'.txt')

    with open( os.path.join(output_data, transcription_file_path)[:-4]+'.txt', 'w') as file:
        #content = file.read()
        #if answer.strip() not in content:
        file.write(answer)
        
        os.remove(os.path.join(dataset_path,transcription_file_path)[:-4]+'.txt')   


@app.route('/jsonToTranscription', methods=['POST'])
def jsonToTranscription():
    answers_file_path = os.path.join(dataset_path, 'answers.json')

    # Read the answers JSON file
    with open(answers_file_path, 'r') as answers_file:
        answers_data = json.load(answers_file)

    '''
    # Iterate over dataset files
    for folder in os.listdir(output_data):
        folder_path = os.path.join(output_data, folder)
        
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith('.txt'):
                    transcription_file_path = os.path.join(folder_path, file)
                    answer = answers_data.get(os.path.join(folder, file).replace('.txt', '.mp3'), '')
                    if answer:
                        print("1111111111111111111111111")
                        write_answer_to_transcription(answer, transcription_file_path)
    '''
    for path in answers_data.keys():
        write_answer_to_transcription(answers_data[path], path)
    os.remove(answers_file_path)
    return jsonify({'message': 'JSON saved to transcription file successfully'}), 200


def run_user_intervention_app(output_data_path, app_started):
    global dataset_path
    global output_data
    output_data = output_data_path
    dataset_path = os.path.join(output_data_path, 'inspection')
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_data', required=True, help='Path to the output data directory')
    args = parser.parse_args()
    run_user_intervention_app(args.output_data,False)