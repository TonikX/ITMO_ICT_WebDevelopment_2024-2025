import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CleaningScheduleComponent } from './cleaning-schedule.component';

describe('CleaningScheduleComponent', () => {
  let component: CleaningScheduleComponent;
  let fixture: ComponentFixture<CleaningScheduleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CleaningScheduleComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CleaningScheduleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
