import React, { Component } from 'react';
import './App.css';
import ScatterPlot from './ScatterPlot';

class App extends Component {
  render() {
    const { winsVsAts, downOneQuarterFourCloseTrue } = this.props;
    const winsVsDownOneQuarterFourCloseTrue = winsVsAts.map((elem, idx) => {
      return [elem[0], downOneQuarterFourCloseTrue[idx]];
    });
    const atsWinsVsDownOneQuarterFourCloseTrue = winsVsAts.map((elem, idx) => {
      return [elem[1], downOneQuarterFourCloseTrue[idx]];
    });
    return (
      <div className="App" id="container">
        <header className="one">
          <h1>Winning Situations</h1>
        </header>
        <b className="two">
          Understanding and visualizing key moments that affect a team's ability
          to win on the field and against the spread in the NFL.
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
          <ScatterPlot
            data={this.props.winsVsAts}
            title={'Wins vs Wins Against the Spread'}
          />
          But before going deeper into any results and statistics, lets take a
          look at the tools, methodology, and inputs used to derive them.
          <hr />
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
        <header className="eight">
          <h1>The Game's Mosts Important Situation</h1>
          <hr />
        </header>
        <section className="nine">
          <p>
            To both teams and gamblers alike, there is one situation which
            correlates with success more than any other. A team's Win
            Probability Added per play on{' '}
            <b>First Down in the Fourth Quarter of close games</b>. Here, close
            is defined as a score differential less than or equal to 12 points.
            The raw correlation to wins is <b>0.78</b> and to against the spread
            wins it is <b>0.54</b>. Both of those numbers are the highest in
            their respective categories.
          </p>
          <ScatterPlot
            data={winsVsDownOneQuarterFourCloseTrue}
            title="Wins vs WPA Down One, Quarter Four, Close Game"
          />
          <ScatterPlot
            data={atsWinsVsDownOneQuarterFourCloseTrue}
            title="ATS Wins vs WPA - Down One, Quarter Four, Close Game"
          />
          <p>
            If you're a diehard football fan, as I am, this is somewhat
            surprisng to find out. The common sense states that third is the
            King of downs, and the best teams are the best because they dial up
            their performance when it's either succeed or vacate the field of
            play.
          </p>
          <p>
            In fact, third down does not appear to be nearly as important as the
            first two. Take, for example,{' '}
            <b>third down in the fourth quarter of close games</b>. If you had
            asked me to make a hypothesis about which situation would correlate
            most strongly with a team's win-loss record, then this would have
            been the one I chose. As it turns out, the correlation coefficient
            is <b>0.42</b>, which is respectable, but to put it in context,
            there are fifty game states that are more strongly correlated to
            wins. Further extending the weirdness, of those fifty, only five
            involve third down -- the rest are all tied to either first or
            second down.
          </p>
          <p>
            For the curious, the top five in order are:
            <ol>
              <li>First Down, Fourth Quarter, Close Game</li>
              <li>First Down, Second Half, Close Game</li>
              <li>
                First Down, Third Quarter, Close Game, Outside the Red Zone
              </li>
              <li>
                First Down, Second Quarter, Close Game, Outside the Red Zone
              </li>
              <li>
                First Down, First Quarter, Close Game, Outside the Red Zone
              </li>
            </ol>
            <br />
            And for wins against the spread:
            <ol>
              <li>First Down, Fourth Quarter, Close Game</li>
              <li>Second Down, Second Half, Close Game</li>
              <li>Second Down, Second Half, Close Game, Inside the Red Zone</li>
              <li>
                Second Down, Second Quarter, Close Game, Inside the Red Zone
              </li>
              <li>
                Second Down, First Quarter, Close Game, Inside the Red Zone
              </li>
            </ol>
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
  ],
  downOneQuarterFourCloseTrue: [
    -0.01,
    0,
    0.004,
    0,
    -0.007,
    0.015,
    -0.005,
    0.008,
    0.004,
    -0.007,
    -0.009,
    -0.005,
    0.001,
    0.005,
    0.002,
    0.007,
    0.01,
    0.008,
    -0.004,
    -0.003,
    0.004,
    0.007,
    -0.003,
    -0.011,
    -0.011,
    0,
    0.003,
    -0.002,
    -0.006,
    -0.003,
    0.001,
    -0.004
  ]
};

export default App;
