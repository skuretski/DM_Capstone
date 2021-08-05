import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MainService {


  state_clicked:boolean = false;
  city_clicked: boolean = false;
  restaurants:object = {};
  active_state: string = '';
  az_count: number = 0;
  wi_count: number = 0;
  nv_count: number = 0;
  az_restaurants: [Restaurant] = [new Restaurant('', '', '', '', '', 0, '', [''])]
  wi_restaurants: [Restaurant] = [new Restaurant('', '', '', '', '', 0, '', [''])]
  nv_restaurants: [Restaurant] = [new Restaurant('', '', '', '', '', 0, '', [''])]
  active_count: number = 0;
  active_restaurants: [Restaurant] = [new Restaurant('', '', '', '', '', 0, '', [''])]
  loaded: boolean = true;


  constructor(private http:HttpClient) {
    this.getRestaurants().subscribe(data => {
      //@ts-ignore
      this.restaurants = data.reduce(((acc,row) => {
        acc[row.state].push(row)
        return acc
      }),{NV:[], WI:[], AZ:[]})
      
      if(Object.keys(this.restaurants)) {
        //@ts-ignore
        this.az_count = this.restaurants['AZ'].length
        //@ts-ignore
        this.az_restaurants = this.restaurants['AZ']
        //@ts-ignore
        this.wi_count = this.restaurants['WI'].length
        //@ts-ignore
        this.wi_restaurants = this.restaurants['WI']
        //@ts-ignore
        this.nv_count = this.restaurants['NV'].length
        //@ts-ignore
        this.nv_restaurants = this.restaurants['NV']
        this.loaded = true;
      }
    })
  }

  getRestaurants():Observable<any> {
    return this.http.get('../assets/data/restaurant_list.json');
  }
}

export class Restaurant {
  name: string;
  latitude: string;
  longitude: string;
  state: string;
  rating: number;
  count: number;
  address: string;
  categories: string[];
  constructor(name: string, latitude: string, longitude: string, state: string, rating: string, count: number, address: string, categories: string[]) {
    this.name = name;
    this.latitude = latitude;
    this.longitude = longitude;
    this.state = state;
    this.rating = parseFloat(rating);
    this.count = count;
    this.address = address;
    this.categories = categories;
  }
}