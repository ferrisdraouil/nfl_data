// Scatterplot template original from https://github.com/isaaguilar/

import React from 'react';
import { scaleLinear, max, min, axisLeft, axisBottom } from 'd3';
import Circles from './Circles';
import TrendLine from './TrendLine';
import Axis from './Axis';

export default class ScatterPlot extends React.Component {
  render() {
    const margin = { top: 20, right: 15, bottom: 60, left: 60 };
    const width = 800 - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;
    const data = this.props.data;

    const x = scaleLinear()
      .domain([
        Math.min(
          min(data, function(d) {
            return d[0];
          }),
          0
        ),
        max(data, function(d) {
          return d[0];
        })
      ])
      .range([0, width]);

    const y = scaleLinear()
      .domain([
        Math.min(
          min(data, function(d) {
            return d[1];
          }),
          0
        ),
        max(data, function(d) {
          return d[1];
        })
      ])
      .range([height, 0]);

    return (
      <div>
        <h3> {this.props.title} </h3>
        <svg
          className="chart"
          viewBox={`0, 0, ${width + margin.right + margin.left}, ${height +
            margin.top +
            margin.bottom}`}
        >
          <g
            transform={'translate(' + margin.left + ',' + margin.top + ')'}
            width={width}
            height={height}
            className="main"
          >
            <Circles data={data} scale={{ x, y }} />
            <TrendLine data={data} scale={{ x, y }} />
            <Axis
              axis="x"
              transform={'translate(0,' + height + ')'}
              scale={axisBottom().scale(x)}
            />
            <Axis
              axis="y"
              transform="translate(0,0)"
              scale={axisLeft().scale(y)}
            />
          </g>
        </svg>
      </div>
    );
  }
}
