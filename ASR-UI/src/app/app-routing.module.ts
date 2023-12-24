import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { FilesTranscriptionsComponent } from './views/files-transcriptions/files-transcriptions.component';

const routes: Routes = [
  {path:'', component:FilesTranscriptionsComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
