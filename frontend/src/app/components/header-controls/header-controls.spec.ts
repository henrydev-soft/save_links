import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HeaderControls } from './header-controls';

describe('HeaderControls', () => {
  let component: HeaderControls;
  let fixture: ComponentFixture<HeaderControls>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeaderControls]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HeaderControls);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
