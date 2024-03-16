import { Component, OnInit } from '@angular/core';
import { perPage } from 'src/app/constants/constants';
import { FileTranscriptionsService } from 'src/app/services/file-transcriptions.service';

@Component({
  selector: 'app-files-transcriptions',
  templateUrl: './files-transcriptions.component.html',
  styleUrls: ['./files-transcriptions.component.css']
})
export class FilesTranscriptionsComponent implements OnInit {
  mp3Files: any[] = [];
  page: number = 1;
  perPage: number = perPage;
  myAnswer:{[key:string]: string}[]=[];

  constructor(private fileTranscriptionsService: FileTranscriptionsService) { }

  ngOnInit(): void {
    this.loadMP3Files();
  }

  loadMP3Files(){
    this.fileTranscriptionsService.getMP3Files(this.page, this.perPage).subscribe((response) => {
      this.mp3Files = response; // Assuming the response is an array of MP3 files

      this.myAnswer = this.mp3Files.reduce((result, mp3File) => {
        // Check if the key already exists in the result object
        if (!result.hasOwnProperty(mp3File.mp3_file)) {
          result[mp3File.mp3_file] = ' ';
        }
        return result;
      }, {});

      console.log(this.mp3Files);
    }),(error) => {
      console.log(error);
    };
  };

  nextPage() {
    this.page++;
    this.loadMP3Files();
  }

  prevPage() {
    if (this.page > 1) {
      this.page--;
      this.loadMP3Files();
    }
  }


  saveTranscription(mp3_file: string) {
    console.log(this.myAnswer[mp3_file]);
      this.fileTranscriptionsService.saveTranscription(mp3_file, this.myAnswer[mp3_file]).subscribe(
        (response) => {
          if (response && response.message) {
            console.log('Server Message:', response.message);
          } else {
            console.log('Non-JSON Response:', response);
          }
          this.loadMP3Files(); // Refresh the page to reflect changes
        } ), (error) => {
          console.error('Failed to save transcription:', error);
          alert('Failed to save transcription.');
        }
     
  }

  getMP3FileUrl(mp3File: string): string {
    return this.fileTranscriptionsService.getMP3FileUrl(mp3File);
  }

  updateMyAnswerValue(mp3_file: string, myAnswer: string) {
    this.myAnswer[mp3_file] = myAnswer;
  }

  isAnyRadioChecked(file): boolean {
    return !file.transcription_lines.some(line => file.answer === line);
  }

  copyJsonToTranscription(){
    this.fileTranscriptionsService.copyJsonToTranscription().subscribe
    ((response) => {
        console.log('Server Message:', response.message);
    }), (error) => {
      console.error('Failed to save transcription:', error);
      alert('Failed to save transcription.');
    };
  }

}
