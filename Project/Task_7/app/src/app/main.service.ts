import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MainService {
  state_clicked:boolean = false;
  restaurants_by_state:object = {};

  constructor(private http:HttpClient) { 
    this.getRestaurantsByState().subscribe(data => {
      this.restaurants_by_state = data;
      console.log(this.restaurants_by_state)
    })
  }

  getRestaurantsByState():Observable<any> {
    return this.http.get('../assets/data/restaurant_by_state.json');
  }
}
