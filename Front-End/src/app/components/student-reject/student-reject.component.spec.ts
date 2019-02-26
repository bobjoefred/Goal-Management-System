import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StudentRejectComponent } from './student-reject.component';

describe('StudentRejectComponent', () => {
  let component: StudentRejectComponent;
  let fixture: ComponentFixture<StudentRejectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StudentRejectComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StudentRejectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component)
      .toBeTruthy();
  });
});
