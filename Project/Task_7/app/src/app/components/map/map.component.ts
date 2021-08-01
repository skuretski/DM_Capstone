import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { MainService } from 'src/app/main.service';
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
  color:any;
  
  // Positioning and Size
  centered: any;
  width: number = 800;
  height: number = 600;


  constructor(public ms: MainService) { }

  ngOnInit(): void {
  }

  async ngAfterViewInit() {
    let data = await Promise.all([
      d3.json('../../../assets/data/states.json'),
      d3.json('../../../assets/data/geojson.json')
    ])
    let data1:any = data[0]
    let data2:any = data[1]

    this.data_states = data1
    this.data_businesses = data2

    this.svg = d3.select("svg")
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", "0 0 800 600")
      .attr("preserveAspectRatio", "xMidYMid meet")
      .style("margin", "auto")

    this.projection = d3.geoAlbersUsa().scale(800).translate([this.width/2, this.height/2])
    this.path = d3.geoPath().projection(this.projection)
    this.color = d3.scaleLinear()
      .domain([1, 50])
      //@ts-ignore
      .range(['#fff', '#409A99']);
    this.makeMap()
  }

  makeMap() {
    this.g = this.svg.append('g')
    this.map = this.g.append('g').classed('map-layer', true)
    this.map.selectAll('path')
      .data(this.data_states.features)
      .enter().append('path')
      .on('click', (e:any, d:any) => this.clicked(e,d))
      .attr('d', this.path)
        .style('fill', '#495057')
        .style('stroke', '#fff')
        .style('stroke-width','1px')
        .attr('class', 'states')

    console.log(this.data_businesses.features)

    this.map.selectAll('.cities')
      .data(this.data_businesses.features)
      .enter()
      .append('path')
        .attr('d', this.path.pointRadius(1))
        .style('fill', 'red')
        .attr('class', 'cities')
  }

  clicked(e:any, d:any) {
    this.ms.state_clicked = !this.ms.state_clicked;
    let x, y, k;
    // Compute centroid of the selected path
    if (d && this.centered !== d) {
      let centroid = this.path.centroid(d);
      x = centroid[0];
      y = centroid[1];
      k = 4;
      this.centered = d;
    } else {
      x = this.width / 2;
      y = this.height / 2;
      k = 1;
      this.centered = null;
    }
    console.log(d.properties.NAME)
    // Highlight the clicked province
    this.map.selectAll('path')
      .style('fill', (d:any) => {return this.centered && d===this.centered ? '#D5708B' : '#495057'});
  
    // Zoom
    this.g.transition()
      .duration(500)
      .attr('transform', 'translate(' + Number(this.width / 2) + ',' + Number(this.height / 2) + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
  }

  nameFn(d:any){
    return d && d.properties ? d.properties.NAME : null;
  }

}
