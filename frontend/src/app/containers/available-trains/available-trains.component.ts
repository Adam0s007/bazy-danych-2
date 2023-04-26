import {Component, EventEmitter, Output} from '@angular/core';
import {TrainsService} from "../../services/trains.service";
import {Train} from "../../models/train.model";

@Component({
  selector: 'app-available-trains',
  templateUrl: './available-trains.component.html',
  styleUrls: ['./available-trains.component.css']
})
export class AvailableTrainsComponent {
  trains: Train[] = [];

  @Output() dataEvent = new EventEmitter<Train>();

  public constructor(private trainsService: TrainsService) {
    trainsService.allTrains().subscribe(value => {
      console.log(value)
      // @ts-ignore
      this.trains = value.map(t => t as Train);
      this.sendData(this.trains[0]);
    });
  }


  sendData(train: Train) {
    this.dataEvent.emit(train);
  }
}
