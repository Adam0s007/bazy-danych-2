import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Train} from "../../models/train.model";
import {TrainsService} from "../../services/trains.service";

@Component({
  selector: 'app-train-details',
  templateUrl: './train-details.component.html',
  styleUrls: ['./train-details.component.css']
})
export class TrainDetailsComponent {
  @Input() train!: Train;
  @Output() closeComponentEVent = new EventEmitter<boolean>();

  seatDetails: number = -1;

  public constructor(private trainsService: TrainsService) {
  }


  exit() {
    this.closeComponentEVent.emit(true);
  }
}
