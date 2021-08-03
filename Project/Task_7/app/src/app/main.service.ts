import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MainService {
  state_clicked:boolean = false;
  restaurants_by_state:object = {};
  active_state: string = '';
  arizona = {}
  wisconsin = {}
  nevada = {}
  arizona_cats = []
  wisconsin_cats = []
  nevada_cat = []

  constructor(private http:HttpClient) { 
    this.getRestaurantsByState().subscribe(data => {
      this.restaurants_by_state = data;
      //@ts-ignore
      this.arizona_cats = Object.keys(this.restaurants_by_state['AZ'])
      //@ts-ignore
      this.wisconsin_cats = Object.keys(this.restaurants_by_state['WI'])
      //@ts-ignore
      this.nevada_cats = Object.keys(this.restaurants_by_state['NV'])

    })
  }

  getRestaurantsByState():Observable<any> {
    return this.http.get('../assets/data/restaurant_by_state.json');
  }
}
