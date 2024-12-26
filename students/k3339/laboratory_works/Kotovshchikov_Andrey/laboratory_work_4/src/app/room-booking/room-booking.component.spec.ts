import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoomBookingComponent } from './room-booking.component';

describe('RoomBookingComponent', () => {
  let component: RoomBookingComponent;
  let fixture: ComponentFixture<RoomBookingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RoomBookingComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RoomBookingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
