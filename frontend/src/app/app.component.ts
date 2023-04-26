import { Component } from '@angular/core';
import {Train} from "./models/train.model";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'train-system';

  trainDetails?: Train;

  seeDetails(train: Train) {
    this.trainDetails = train;
  }

}
