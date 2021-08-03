import { Component, OnInit, ViewChild } from '@angular/core';
import { MainService } from './main.service';
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
  model: any;
  
  @ViewChild('instance', {static: true}) instance!: NgbTypeahead;
  focus$ = new Subject<string>();
  click$ = new Subject<string>();

  constructor(public ms:MainService) {

  }

  ngOnInit() {
    
  }

  search: OperatorFunction<string, readonly string[]> = (text$: Observable<string>) => {
    const debouncedText$ = text$.pipe(debounceTime(200), distinctUntilChanged());
    console.log(this.instance)
    //@ts-ignore
    const clicksWithClosedPopup$ = this.click$.pipe(filter(() => !this.instance.isPopupOpen()));
    const inputFocus$ = this.focus$;
    
    return merge(debouncedText$, inputFocus$, clicksWithClosedPopup$).pipe(
      map(term => (term === '' ? (this.ms.active_state == 'AZ' ? this.ms.arizona_cats : (this.ms.active_state == 'WI' ? this.ms.wisconsin_cats : this.ms.nevada_cat))
      //@ts-ignore
        : (this.ms.active_state == 'AZ' ? this.ms.arizona_cats : (this.ms.active_state == 'WI' ? this.ms.wisconsin_cats : this.ms.nevada_cat)).filter(v => v.toLowerCase().indexOf(term.toLowerCase()) > -1)).slice(0, 10))
    );
  }
}

