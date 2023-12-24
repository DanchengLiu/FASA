import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { FilesTranscriptionsComponent } from './views/files-transcriptions/files-transcriptions.component';

@NgModule({
  declarations: [
    AppComponent,
    FilesTranscriptionsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
