import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentIndividualComponent } from './student-individual.component';

describe('StudentIndividualComponent', () => {
  let component: StudentIndividualComponent;
  let fixture: ComponentFixture<StudentIndividualComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StudentIndividualComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudentIndividualComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component)
      .toBeTruthy();
  });
});
