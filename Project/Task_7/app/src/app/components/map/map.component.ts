import { Component, OnInit, Output, EventEmitter } from '@angular/core';
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
  width: number = 600;
  height: number = 600;

  // Event Emitters
  @Output() stateClicked: EventEmitter<any> = new EventEmitter();
  @Output() dotClicked: EventEmitter<any> = new EventEmitter();


  constructor(public ms: MainService) { }

  ngOnInit(): void {
  }

  async ngAfterViewInit() {
    let data = await Promise.all([
      d3.json('../../../assets/data/states.json'),
      d3.json('../../../assets/data/restaurants.json')
    ])
    let data1:any = data[0]
    let data2:any = data[1]

    this.data_states = data1
    this.data_businesses = data2

    this.svg = d3.select("svg")
      .attr("width", this.width)
      .attr("height", this.height)
      .attr("viewBox", "0 0 600 600")
      .attr("preserveAspectRatio", "xMidYMid meet")
      .style("margin", "auto")

    this.projection = d3.geoAlbersUsa().scale(800).translate([this.width/2, this.height/2])
    this.path = d3.geoPath().projection(this.projection)
    this.color = d3.scaleLinear()
      .domain([1, 50])
      //@ts-ignore
      .range(['#fff', '#004a6a']);
    this.makeMap()
  }

  makeMap() {
    this.g = this.svg.append('g')
    this.map = this.g.append('g').classed('map-layer', true)
    this.map.selectAll('path')
      .data(this.data_states.features)
      .enter().append('path')
      .classed('states', true)
      .on('click', (e:any, d:any) => this.onClickState(e,d))
      .attr('d', this.path)
        .style('fill', '#004a6a')
        .style('stroke', '#fff')
        .style('stroke-width','1px')
        .attr('class', 'states')
        .style('cursor', 'pointer')

    this.map.selectAll('.cities')
      .data(this.data_businesses.features)
      .enter()
      .append('path')
        .attr('d', this.path.pointRadius(4))
        .style('fill', '#e1ad01')
        .attr('class', 'cities')
  }

  onClickState(e:any, d:any) {

    let x, y, k;
    // Compute centroid of the selected path
    if (d && this.centered !== d) {
      let centroid = this.path.centroid(d);
      x = centroid[0];
      y = centroid[1];
      k = 4;
      this.centered = d;
      if(d.properties.NAME == 'Arizona' || d.properties.NAME == 'Wisconsin' || d.properties.NAME == 'Nevada') {
        if(d.properties.NAME == 'Arizona') {
          this.ms.active_count = this.ms.az_count
          this.ms.active_restaurants = this.ms.az_restaurants
          this.ms.active_state = 'AZ'
        }
        else if (d.properties.NAME == 'Wisconsin') {
          this.ms.active_state = 'WI'
          this.ms.active_restaurants = this.ms.wi_restaurants
          this.ms.active_count = this.ms.wi_count
        } 
        else if (d.properties.NAME == 'Nevada') {
          this.ms.active_state = 'NV'
          this.ms.active_count = this.ms.nv_count
          this.ms.active_restaurants = this.ms.nv_restaurants
        } 
      }
      this.ms.state_clicked = true;
    } else {
      x = this.width / 2;
      y = this.height / 2;
      k = 1;
      this.centered = null;
      this.ms.state_clicked = false;
      this.ms.active_state = '';
      this.ms.active_count = 0;
      //@ts-ignore
      this.ms.active_restaurants = undefined
    }

    // Highlight the state
    this.map.selectAll('.states')
      .style('fill', (d:any) => {return this.centered && d===this.centered ? '#5498b6' : '#004a6a'});
  
    // Zoom
    this.g.transition()
      .duration(500)
      .attr('transform', 'translate(' + Number(this.width / 2) + ',' + Number(this.height / 2) + ')scale(' + k + ')translate(' + -x + ',' + -y + ')');
    console.log(this.ms.active_state)
  }

  nameFn(d:any){
    return d && d.properties ? d.properties.NAME : null;
  }

}
