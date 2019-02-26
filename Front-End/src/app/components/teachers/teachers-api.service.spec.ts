import { TestBed } from '@angular/core/testing';

import { TeachersApiService } from './teachers-api.service';

describe('TeachersApiService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TeachersApiService = TestBed.get(TeachersApiService);
    expect(service)
      .toBeTruthy();
  });
});
