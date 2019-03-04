import React from 'react';

export default class RenderCircles extends React.Component {
  render() {
    let renderCircles = this.props.data.map((coords, i) => (
      <circle
        cx={this.props.scale.x(coords[0])}
        cy={this.props.scale.y(coords[1])}
        r="8"
        style={{ fill: '#1e656d' }}
        key={i}
      />
    ));
    return <g>{renderCircles}</g>;
  }
}
