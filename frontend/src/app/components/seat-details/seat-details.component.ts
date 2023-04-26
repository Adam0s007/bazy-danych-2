import {ApplicationRef, Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from '@angular/core';
import {Train} from "../../models/train.model";
import {TrainsService} from "../../services/trains.service";
import {Reservation} from "../../models/reservation.model";

@Component({
  selector: 'app-seat-details',
  templateUrl: './seat-details.component.html',
  styleUrls: ['./seat-details.component.css']
})
export class SeatDetailsComponent implements OnChanges {
  @Input() train!: Train;
  @Input() seat_id!: number;
  free?: number;

  reservationDetails?: Reservation;

  user_full_name: string = "";

  @Output() closeComponentEVent = new EventEmitter<boolean>();

  public constructor(private trainsService: TrainsService, private appRef: ApplicationRef) {
  }

  ngOnChanges(changes: SimpleChanges): void {
    if ('train' in changes || 'seat_id' in changes) {
      this.free = this.train.free_seats[this.seat_id];
      if (!this.free) {
        this.trainsService.reservationDetails(this.train._id, this.seat_id).subscribe(value => {
          console.log("RESERVATION-DETAILS")
          console.log(value)
          this.reservationDetails = value as Reservation;
        });
      }
    }
  }

  async makeReservation(user_full_name: string) {
    this.trainsService.buyTicket(user_full_name, this.train._id, this.seat_id);
    await new Promise(f => setTimeout(f, 1000));
    window.location.reload();
  }

  async deleteReservation() {
    this.trainsService.reservationDelete(this.train._id, this.seat_id);
    console.log(this.train._id + " " + this.seat_id);
    await new Promise(f => setTimeout(f, 1000));
    window.location.reload();
  }

  closeButtonHandler() {
    this.closeComponentEVent.emit(true);
  }
}
