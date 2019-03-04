import React from 'react';
import ScatterPlot from './ScatterPlot';

export default class LinearGraph extends React.Component {
  render() {
    return <ScatterPlot data={this.props.data} title={this.props.title} />;
  }
}
