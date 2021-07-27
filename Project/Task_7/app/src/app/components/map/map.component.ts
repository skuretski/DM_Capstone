import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import * as topojson from "topojson-client";
@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  svg: any;
  data_businesses: any;
  data_states: any;
  path: any;
  projection: any;
  map: any;

  width: number = 1000;
  height: number = 1000;


  constructor() { }

  ngOnInit(): void {
  }

  async ngAfterViewInit() {
    this.svg = d3.select("#mapviz")
      .append("svg")
      .attr("width", this.width)
      .attr("height", this.height);

    this.projection = d3.geoAlbersUsa().scale(1000);
    this.path = d3.geoPath().projection(this.projection)

    await Promise.all([
      d3.json('../../../assets/data/states.json'),
      d3.json('../../../assets/data/geojson.json')
    ]).then(([data1, data2]) => {
      this.data_states = data1
      this.data_businesses = data2
      this.svg.append("g")
      this.makeMap()
    })
  }

  makeMap() {
    this.svg.select("g")
      .style("fill", "#fff")
      .style("stroke", "aaa")
      .style("stroke-width", "1px")
      .append('path')
      .datum(topojson.feature(this.data_states, this.data_states.objects.usStates))
      .attr('d', this.path)
  }

}
