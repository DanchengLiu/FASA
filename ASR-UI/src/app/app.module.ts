import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FilesTranscriptionsComponent } from './views/files-transcriptions/files-transcriptions.component';
import { FileTranscriptionsService } from './services/file-transcriptions.service';
import { HttpClient, HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [
    AppComponent,
    FilesTranscriptionsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  providers: [FileTranscriptionsService],
  bootstrap: [AppComponent]
})
export class AppModule { }
