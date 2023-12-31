import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilesTranscriptionsComponent } from './files-transcriptions.component';

describe('FilesTranscriptionsComponent', () => {
  let component: FilesTranscriptionsComponent;
  let fixture: ComponentFixture<FilesTranscriptionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FilesTranscriptionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FilesTranscriptionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
