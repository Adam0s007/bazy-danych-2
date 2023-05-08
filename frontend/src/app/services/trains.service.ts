import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class TrainsService {
  private url = 'http://127.0.0.1:8000/trains';

  constructor(private httpClient: HttpClient) {
  }

  allTrains() {
    return this.httpClient.get(this.url);
  }

  reservationDetails(trainId: string, seatId: number) {
    const url = `http://127.0.0.1:8000/reservations/details?train_id=${trainId}&seat_id=${seatId}`;
    return this.httpClient.get(url);
  }


  reservationDelete(trainId: string, seatId: number) {
    const url = `http://127.0.0.1:8000/reservations/delete?train_id=${trainId}&seat_id=${seatId}`;
    this.httpClient.get(url).subscribe(value => console.log(value));
    console.log("DELETE", trainId, seatId);
  }

  buyTicket(client_id: number, train_id: string, seat_id: number) {
    const url = 'http://127.0.0.1:8000/reservations/make';
    const headers = new HttpHeaders()
      .set('accept', 'application/json')
      .set('Content-Type', 'application/json');

    const body = {
      client_id: client_id,
      train_id: train_id,
      seat: seat_id
    };

    this.httpClient.post(url, body, {headers})
      .subscribe(response => {
        console.log(response);
      });
  }
}
