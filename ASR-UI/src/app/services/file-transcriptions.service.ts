import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { apiURL } from '../constants/constants';

@Injectable({
  providedIn: 'root'
})
export class FileTranscriptionsService {

  constructor(private http: HttpClient) { }

  getMP3Files(page: number, perPage: number): Observable<any[]> {
    console.log(`${apiURL}/api/mp3_files?page=${page}&per_page=${perPage}`);
    return this.http.get<any[]>(`${apiURL}/api/mp3_files?page=${page}&per_page=${perPage}`);
  }

  saveTranscription(mp3_file: string, myAnswer: string): Observable<any> {
    return this.http.post(`${apiURL}/save_transcription`,{mp3_file:mp3_file, myAnswer:myAnswer});
  }
  getMP3FileUrl(mp3File: string): string {
    return `${apiURL}/play/${mp3File}`;
  }

  copyJsonToTranscription(): Observable<any> {
    return this.http.post(`${apiURL}/jsonToTranscription`,{});
  }
}
