import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AvailableTrainsComponent } from './containers/available-trains/available-trains.component';
import {HttpClientModule} from "@angular/common/http";
import { TrainDetailsComponent } from './containers/train-details/train-details.component';
import { SeatDetailsComponent } from './components/seat-details/seat-details.component';
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [
    AppComponent,
    AvailableTrainsComponent,
    TrainDetailsComponent,
    SeatDetailsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
