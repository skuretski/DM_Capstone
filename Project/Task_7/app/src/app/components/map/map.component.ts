import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import * as topojson from "topojson-client";
@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  data_businesses: any;
  data_states: any;
  
  // D3 Component Variables
  svg: any;
  path: any;
  projection: any;
  map: any;
  g: any;
  
  // Positioning and Size
  centered: any;
  width: number = 800;
  height: number = 600;


  constructor() { }

  ngOnInit(): void {
  }

  async ngAfterViewInit() {
    let data = await Promise.all([
      d3.json('../../../assets/data/states.json'),
      d3.json('../../../assets/data/geojson.json')
    ])
    let data1:any = data[0]
    let data2:any = data[1]
    let features = data2.features.filter((b:any) => b.properties.state != "ON")
    data2.features = features
    this.data_states = data1
    this.data_businesses = data2

    this.svg = d3.select("#mapviz")
      .append("svg")
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", "0 0 800 600")
      .attr("preserveAspectRatio", "xMidYMid meet")
      .style("margin", "auto")

    this.projection = d3.geoAlbersUsa().scale(600)
    this.path = d3.geoPath().projection(this.projection)
    this.makeMap()
  }

  makeMap() {
    this.svg.append('path')
      .datum(topojson.feature(this.data_states, this.data_states.objects.usStates))
        .attr('d', this.path)
        .style('fill', '#495057')
        .style('stroke', '#fff')
        .style('stroke-width','1px')
        .attr('class', 'states');
    this.svg.selectAll('.cities')
      .data(this.data_businesses.features)
      .enter()
      .append('path')
      .attr('d', this.path.pointRadius(5))
      .attr('class', 'cities')
  }

  getName(d:any){
    return d && d.properties ? d.properties.STATE_ABBR : null;
  }

  getNameLength(d:any){
    let n = this.getName(d)
    return n ? n.length : 0
  }

  fillColor(d:any){
    let color = d3.scaleLinear<string>()
      .domain([1, this.data_states.objects.usStates.geometries.length])
      .range(['red', 'green'])
      .clamp(true)
    return color(this.getNameLength(d))
  }

  clicked(d:any) {
    let x, y, k
    console.log(d)
    // Compute centroid of the selected path
    if (d && this.centered !== d) {
      var centroid = this.path.centroid(d)
      x = centroid[0]
      y = centroid[1]
      k = 4;
      this.centered = d
    } else {
      x = this.width / 2
      y = this.height / 2
      k = 1;
      this.centered = null
    }
  
    // Highlight the clicked province
    this.map.selectAll('path')
      .style('fill', (d:any) => this.centered && this.centered === d ? '#D5708B' : '#000')
  
    // Zoom
    this.g.transition()
      .duration(750)
      .attr('transform', 'translate(' + this.width / 2 + ',' + this.height / 2 + ')scale(' + k + ')translate(' + -x + ',' + -y + ')')
  }
}
