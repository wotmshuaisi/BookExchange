import { TestBed } from '@angular/core/testing';

import { DjangorestService } from './djangorest.service';

describe('DjangorestService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: DjangorestService = TestBed.get(DjangorestService);
    expect(service).toBeTruthy();
  });
});
