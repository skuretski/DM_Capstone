import { Component, OnInit, ViewChild } from '@angular/core';
import { MainService, Restaurant } from './main.service';
import {NgbTypeahead} from '@ng-bootstrap/ng-bootstrap';
import {Observable, Subject, merge, OperatorFunction} from 'rxjs';
import {debounceTime, distinctUntilChanged, filter, map} from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'Yelp Discovery';
  pageSize = 10;
  page = 1;
  isCollapsed: boolean[] = [];

  constructor(public ms:MainService) {

  }

  ngOnInit() {
    
  }

  onCollapse(i: number) {
    if(this.isCollapsed[i]) {
      this.isCollapsed[i] = false
    } else {
      if(this.isCollapsed.length > 0) {
        for(let i = 0; i < this.isCollapsed.length; i++) {
          this.isCollapsed[i] = false;
        }
      }
      this.isCollapsed[i]= true
    }
  }

}

