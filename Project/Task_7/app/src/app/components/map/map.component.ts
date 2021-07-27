import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  svg: any;
  data: any;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterViewInit() {
    this.svg = d3.select("#mapviz")
      .append("svg")
  }

}
