import React, { Component } from 'react';
import './App.css';
import LinearPlot from './LinearPlot';

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
        <h1 className="three">Which stats matter?</h1>
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
            record against the spread than their number of wins. Yet, even here
            its only a <b>59.05%</b> correlation.
          </p>
        </section>
        <section className="five">
          <LinearPlot
            data={this.props.winsVsAts}
            title={'Wins vs Wins Against the Spread'}
          />
          But before going deeper into any results and statistics, lets take a
          look at the tools, methodology, and inputs used to derive them.
        </section>
        <h1 className="six">Python, Pandas, and nflscrapR</h1>
        <section className="seven">
          <h3>
            Skip this section if you have no interest in the tools used to parse
            and generate data.
          </h3>
          <p>
            Data was taken from the{' '}
            <a href="https://github.com/ryurko/nflscrapR-data">nflscrapR</a>{' '}
            repo on Github. If you're interested in running your own analyses,
            more info can be found there. It is a massive collection of data on
            every play from the season that is meant to be used with the
            programming language R. However, the Python library Pandas provides
            a wealth of tools and functionality that allows you to perform the
            same sort of data manipulation and analysis that R does.
            <p>Getting up and running is pretty simple:</p>
            <pre>
              <code>import pandas as pd</code>
            </pre>{' '}
            and then if you have the CSV file locally:
            <pre>
              <code>data = pd.read_csv(file_path, low_memory=False)</code>
            </pre>
            or if your CSV in on the web:
            <pre>
              <code>data = pd.read_csv(url_path, low_memory=False)</code>
            </pre>
            A great Pandas startup guide can be found{' '}
            <a href="https://pandas.pydata.org/pandas-docs/version/0.22/10min.html">
              {' '}
              here{' '}
            </a>
            .
          </p>
          <br />
          <p>
            There are two key statistics that are registered on every play in
            nflscrapR -- <b>Expected Points and Win Probability.</b>
            <p>The way these are calculated is as follows:</p>
          </p>
          <p>
            Suppose that there is 11:39 left in the 3rd quarter. Team A has the
            ball on their own 43 yardline. The score is 20 - 14 in favor of Team
            A. <b>Expected Points</b> is derived by looking at every instance
            that a team has been in the exact same circumstances and returning
            an average of how many points they scored on that drive.{' '}
            <b>Win Probability</b> is derived by instead returning the
            percentage of games that that team went on to win. Sites like{' '}
            <a href="https://live.numberfire.com/nfl">numberFire</a> allow fans
            to look at these numbers live while watching a game.
          </p>
          <p>
            While interesting on their own, in the aggregate, they don't
            necessarily tell us a lot about what makes teams win, or win against
            the spread. But if we can look at these numbers on a per-play basis
            and seperate them by certain downs, distances, and game states, then
            they become very interesting.
          </p>
        </section>
      </div>
    );
  }
}

App.defaultProps = {
  winsVsAts: [
    [3, 7],
    [7, 5],
    [10, 8],
    [6, 7],
    [7, 7],
    [12, 12],
    [6, 9],
    [7, 10],
    [10, 9],
    [6, 6],
    [6, 9],
    [6, 6],
    [11, 7],
    [10, 8],
    [5, 5],
    [12, 9],
    [12, 9],
    [13, 7],
    [7, 8],
    [8, 8],
    [11, 9],
    [13, 10],
    [5, 8],
    [4, 5],
    [4, 6],
    [9, 7],
    [9, 8],
    [4, 5],
    [10, 9],
    [5, 7],
    [9, 8],
    [7, 9]
  ]
};

export default App;
