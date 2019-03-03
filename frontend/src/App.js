import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App" id="container">
        <header className="one">
          <h1>Winning in the NFL</h1>
        </header>
        <b className="two">
          Visualizing key metrics that affect a team's ability to win on the
          field and against the spread.
          <hr />
        </b>
        <h3 className="three">Which stats matter?</h3>
        <section className="four">
          <p>
            It's a question that matters to teams, players, coaches, fans, and
            especially gamblers. Some are more obvious than others. Turnovers
            play an outsize role in the outcome of every game. If a team can
            take the ball away two more times than it gives it away, they win{' '}
            <b>81.6%</b> of the time.
          </p>
          <p>
            Logically it follows that smart teams devote their time an energy to
            winning the turnover battle and smart gamblers bet on those teams.
            Well thats not exactly the worst strategy. Of all of the numbers
            we're going to take a look at, none correlate more to a team's
            record against the spread than their Win-Loss record.
          </p>
        </section>
      </div>
    );
  }
}

export default App;
