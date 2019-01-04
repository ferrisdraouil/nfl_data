import pandas as pd
import numpy as np

# Team Methods

data = pd.read_pickle('2018.pkl')


class Team:
    """Methods for returning data on one team"""

    def __init__(self, team):
        self.team = team

    def __repr__(self):
        return f"Team is {self.team}"

    @classmethod
    def all(cls):
        teams = [
            'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE', 'DAL',
            'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC', 'LA', 'LAC', 'MIA',
            'MIN', 'NE', 'NO', 'NYG', 'NYJ', 'OAK', 'PHI', 'PIT', 'SEA', 'SF',
            'TB', 'TEN', 'WAS'
        ]
        return teams

    def query_generator(self, kwargs):
        """Dynamic query generator from kwargs"""

        query_addition = ""

        if "quarter" in kwargs:
            query_addition += f" & qtr == {kwargs['quarter']}"
        if "down" in kwargs:
            query_addition += f" & down == {kwargs['down']}"
        if "half" in kwargs:
            query_addition += f" & game_half == 'Half{kwargs['half']}'"
        if "close" in kwargs:
            if kwargs['close'] is True:
                query_addition += f" & score_differential >= -12 & score_differential <= 12"
            else:
                query_addition += f" & (score_differential < -12 | score_differential > 12)"
        if "rz" in kwargs:
            if kwargs['rz'] is True:
                query_addition += f" & yardline_100 <= 25"
            else:
                query_addition += f" & yardline_100 > 25"
        if "where" in kwargs:
            if kwargs['where'] is 'home':
                query_addition += f" & home_team == '{self.team}'"
            else:
                query_addition += f" & away_team == '{self.team}'"
        if "play" in kwargs:
            if kwargs['play'] is 'run':
                query_addition += f" & rush_attempt == 1"
            else:
                query_addition += f" & pass_attempt == 1"
        if "since" in kwargs:
            if kwargs['since'] is 'sep':
                query_addition += f" & (game_date.str.slice(5, 7) == '09' | game_date.str.slice(5, 7) == '10' | game_date.str.slice(5, 7) == '11' | game_date.str.slice(5, 7) == '12')"
            elif kwargs['since'] is 'oct':
                query_addition += f" & (game_date.str.slice(5, 7) == '10' | game_date.str.slice(5, 7) == '11' | game_date.str.slice(5, 7) == '12')"
            elif kwargs['since'] is 'nov':
                query_addition += f" & (game_date.str.slice(5, 7) == '11' | game_date.str.slice(5, 7) == '12')"
            else:
                query_addition += f" & game_date.str.slice(5, 7) == '12'"

        return query_addition

    # Validators for args and kwargs

    def validate_kwargs(self, kwargs):
        """Validate optional kwargs"""

        valid_kwargs = ('down', 'quarter', 'half', 'play', 'close', 'rz',
                        'where', 'since')
        valid_downs = (1, 2, 3, 4)
        valid_quarters = (1, 2, 3, 4, 5)
        valid_halves = (1, 2)
        valid_plays = ('run', 'pass')
        valid_close = (True, False)
        valid_rz = (True, False)
        valid_where = ('home', 'away')
        valid_since = ('sep', 'oct', 'nov', 'dec')

        for key in kwargs:
            if key not in valid_kwargs:
                raise ValueError(
                    f"'{key}' not valid. Optional arguments must be one of {valid_kwargs}"
                )
            if key == 'down' and kwargs['down'] not in valid_downs:
                raise ValueError(
                    f"'{kwargs['down']}' not valid. 'down' must be one of {valid_downs}"
                )
            if key == 'quarter' and kwargs.get('quarter') not in valid_quarters:
                raise ValueError(
                    f"'{kwargs['quarter']}' not valid. 'quarter' must be one of {valid_quarters}"
                )
            if key == 'half' and kwargs.get('half') not in valid_halves:
                raise ValueError(
                    f"'{kwargs['half']}' not valid. 'half' must be one of {valid_halves}"
                )
            if key == 'play' and kwargs.get('play') not in valid_plays:
                raise ValueError(
                    f"'{kwargs['play']}' not valid. 'play' must be one of {valid_plays}"
                )
            if key == 'close' and kwargs.get('close') not in valid_close:
                raise ValueError(
                    f"'{kwargs['close']}' not valid. 'close' must be one of {valid_close}"
                )
            if key == 'rz' and kwargs.get('rz') not in valid_rz:
                raise ValueError(
                    f"'{kwargs['rz']}' not valid. 'rz' must be one of {valid_rz}"
                )
            if key == 'where' and kwargs.get('where') not in valid_where:
                raise ValueError(
                    f"'{kwargs['where']}' not valid. 'where' must be one of {valid_where}"
                )
            if key == 'since' and kwargs.get('since') not in valid_since:
                raise ValueError(
                    f"'{kwargs['since']}' not valid. 'since' must be one of {valid_since}"
                )
        if kwargs.get('half') and kwargs.get('quarter'):
            raise ValueError(f"Do not select both 'quarter' and 'half'.")

    def validate_args(self, operation, stat):
        """Validate mandatory 'operation' and 'stat' keywords when applicable"""

        valid_stats = ('epa', 'wpa', 'air_epa', 'air_wpa')
        valid_operations = ('mean', 'median', 'std')

        if operation not in valid_operations:
            raise ValueError(
                f"'{operation}' not valid. Operations must be one of {valid_operations}"
            )
        if stat not in valid_stats:
            raise ValueError(
                f"'{stat}' not valid. Operations must be one of {valid_stats}")

    # Offensive methods

    def stat_per_play_off(self, operation, stat, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns stat per play for combination of 'quarter', 'down', 'half', and 'play' and calculates based on operation.
        """

        self.validate_args(operation, stat)
        self.validate_kwargs(kwargs)

        query = f"posteam == '{self.team}' & play_type != 'no_play'"
        query += self.query_generator(kwargs)

        df = data.query(query)[stat]

        if operation == 'mean':
            return round(df.mean(), 3)
        elif operation == 'median':
            return round(df.median(), 3)
        else:
            return round(df.std(), 3)

    def positive_play_percentage_offense(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays that increased team's expected points.
        """

        self.validate_kwargs(kwargs)

        pos_query = f"posteam == '{self.team}' & play_type != 'no_play' & epa > 0"
        all_query = f"posteam == '{self.team}' & play_type != 'no_play'"

        pos_query += self.query_generator(kwargs)
        all_query += self.query_generator(kwargs)

        pos_plays = data.query(pos_query)
        all_plays = data.query(all_query)
        percentage = len(pos_plays) / len(all_plays)

        return round(percentage, 3)

    def qb_pressure_offense(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays where qb was either hit or sacked.
        """

        self.validate_kwargs(kwargs)

        hit_query = f"posteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & qb_hit == 1"
        sack_query = f"posteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & qb_hit == 0 & sack == 1"
        all_pass_query = f"posteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1"

        hit_query += self.query_generator(kwargs)
        sack_query += self.query_generator(kwargs)
        all_pass_query += self.query_generator(kwargs)

        passes = data.query(all_pass_query).shape[0]
        hits_and_sacks = data.query(hit_query).shape[0] + data.query(
            sack_query).shape[0]
        percentage = hits_and_sacks / passes
        return round(percentage, 3)

    def interceptions_per_pass_off(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of intercepted passes.
        """

        self.validate_kwargs(kwargs)

        int_query = f"posteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & interception == 1"
        all_pass_query = f"posteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1"

        int_query += self.query_generator(kwargs)
        all_pass_query += self.query_generator(kwargs)

        interceptions = data.query(int_query).shape[0]
        passes = data.query(all_pass_query).shape[0]

        return round(interceptions / passes, 3)

    # Defensive methods

    def stat_per_play_def(self, operation, stat, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns stat per play for combination of 'quarter', 'down', 'half', and 'play' and calculates based on operation.
        """

        self.validate_args(operation, stat)
        self.validate_kwargs(kwargs)

        query = f"defteam == '{self.team}' & play_type != 'no_play'"

        query += self.query_generator(kwargs)

        df = data.query(query)[stat]

        if operation == 'mean':
            return round(df.mean(), 3)
        elif operation == 'median':
            return round(df.median(), 3)
        else:
            return round(df.std(), 3)

    def positive_play_percentage_defense(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays that increased team's expected points.
        """

        self.validate_kwargs(kwargs)

        pos_query = f"defteam == '{self.team}' & play_type != 'no_play' & epa < 0"
        all_query = f"defteam == '{self.team}' & play_type != 'no_play'"

        pos_query += self.query_generator(kwargs)
        all_query += self.query_generator(kwargs)

        pos_plays = data.query(pos_query)
        all_plays = data.query(all_query)
        percentage = len(pos_plays) / len(all_plays)

        return round(percentage, 3)

    def qb_pressure_defense(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays where qb was either hit or sacked.
        """

        self.validate_kwargs(kwargs)

        hit_query = f"defteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & qb_hit == 1"
        sack_query = f"defteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & qb_hit == 0 & sack == 1"
        all_pass_query = f"defteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1"

        hit_query += self.query_generator(kwargs)
        sack_query += self.query_generator(kwargs)
        all_pass_query += self.query_generator(kwargs)

        passes = data.query(all_pass_query).shape[0]
        hits_and_sacks = data.query(hit_query).shape[0] + data.query(
            sack_query).shape[0]
        percentage = hits_and_sacks / passes
        return round(percentage, 3)

    def interceptions_per_pass_def(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of intercepted passes.
        """

        self.validate_kwargs(kwargs)

        int_query = f"defteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & interception == 1"
        all_pass_query = f"defteam == '{self.team}' & play_type != 'no_play' & pass_attempt == 1"

        int_query += self.query_generator(kwargs)
        all_pass_query += self.query_generator(kwargs)

        interceptions = data.query(int_query).shape[0]
        passes = data.query(all_pass_query).shape[0]

        return round(interceptions / passes, 3)

    # Combination methods

    def margin_for_stat(self, operation, stat, side, **kwargs):
        """
        Accepts a required str value 'operation', either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts a required str value 'side', either 'o' or 'd'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns margin between offensive and defensive performance per play for combination of 'quarter', 'down', 'half', and 'play'.
        If side == 'o', then defense subtracted from offense and vice versa.
        Calculated pased on operation
        """

        if side != 'o' and side != 'd':
            raise ValueError(f"'side' was {side}. Must be 'o' or 'd'")

        o_stat = self.stat_per_play_off(operation, stat, **kwargs)
        d_stat = self.stat_per_play_def(operation, stat, **kwargs)

        if side == 'o':
            margin = round(o_stat - d_stat, 3)
        else:
            margin = round(d_stat - o_stat, 3)

        return margin

    def cumulative_for_stat(self, operation, stat, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns sum offensive and defensive performance per play for combination of 'quarter', 'down', 'half', and 'play'.
        Calculated pased on operation.
        """

        o_stat = self.stat_per_play_off(operation, stat, **kwargs)
        d_stat = self.stat_per_play_def(operation, stat, **kwargs)
        margin = round(o_stat + d_stat, 3)

        return margin

    def qb_pressure_margin(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns margin between defenseive and offensive qb pressure percentage.
        """

        d_stat = self.qb_pressure_defense(**kwargs)
        o_stat = self.qb_pressure_offense(**kwargs)
        margin = round(d_stat - o_stat, 3)

        return margin

    def positive_play_percentage(self, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays that increased team's expected points.
        """

        self.validate_kwargs(kwargs)

        pos_o = f"posteam == '{self.team}' & play_type != 'no_play' & epa > 0"
        all_o = f"posteam == '{self.team}' & play_type != 'no_play'"
        pos_d = f"defteam == '{self.team}' & play_type != 'no_play' & epa < 0"
        all_d = f"defteam == '{self.team}' & play_type != 'no_play'"

        pos_o += self.query_generator(kwargs)
        all_o += self.query_generator(kwargs)
        pos_d += self.query_generator(kwargs)
        all_d += self.query_generator(kwargs)

        pos_o_plays = data.query(pos_o)
        all_o_plays = data.query(all_o)
        pos_d_plays = data.query(pos_d)
        all_d_plays = data.query(all_d)
        percentage = (len(pos_o_plays) + len(pos_d_plays)) / (
            len(all_d_plays) + len(all_o_plays))

        return round(percentage, 3)

    def grid(self, side, stat, **kwargs):
        """
        Accepts a required str value stat, either 'epa', 'wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns dict of team performance for every valid combination of pass location/length and run location/gap.
        """

        self.validate_kwargs(kwargs)

        if side != 'offense' and side != 'defense':
            raise ValueError(f"'side' was {side}. Must be 'offense' or 'defense'")
        if side != 'offense' and side != 'defense':
            raise ValueError(f"'side' was {side}. Must be 'offense' or 'defense'")

        if side == 'offense':
            side_of_ball = 'posteam'
        else:
            side_of_ball = 'defteam'

        all_play_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & (rush_attempt == 1 | pass_attempt == 1)"

        deep_left_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & pass_location == 'left' & pass_length == 'deep'"
        deep_middle_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & pass_location == 'middle' & pass_length == 'deep'"
        deep_right_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & pass_location == 'right' & pass_length == 'deep'"
        short_left_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & pass_location == 'left' & pass_length == 'short'"
        short_middle_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & pass_location == 'middle' & pass_length == 'short'"
        short_right_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & pass_attempt == 1 & pass_location == 'right' & pass_length == 'short'"

        run_middle_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'middle'"
        run_left_guard_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'left' & run_gap == 'guard'"
        run_left_tackle_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'left' & run_gap == 'tackle'"
        run_left_end_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'left' & run_gap == 'end'"
        run_right_guard_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'right' & run_gap == 'guard'"
        run_right_tackle_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'right' & run_gap == 'tackle'"
        run_right_end_query = f"{side_of_ball} == '{self.team}' & play_type != 'no_play' & rush_attempt == 1 & run_location == 'right' & run_gap == 'end'"

        all_play_query += self.query_generator(kwargs)

        deep_left_query += self.query_generator(kwargs)
        deep_middle_query += self.query_generator(kwargs)
        deep_right_query += self.query_generator(kwargs)
        short_left_query += self.query_generator(kwargs)
        short_middle_query += self.query_generator(kwargs)
        short_right_query += self.query_generator(kwargs)

        run_middle_query += self.query_generator(kwargs)
        run_left_guard_query += self.query_generator(kwargs)
        run_left_tackle_query += self.query_generator(kwargs)
        run_left_end_query += self.query_generator(kwargs)
        run_right_guard_query += self.query_generator(kwargs)
        run_right_tackle_query += self.query_generator(kwargs)
        run_right_end_query += self.query_generator(kwargs)

        all_plays = data.query(all_play_query)

        deep_left_passes = data.query(deep_left_query)
        deep_middle_passes = data.query(deep_middle_query)
        deep_right_passes = data.query(deep_right_query)
        short_left_passes = data.query(short_left_query)
        short_middle_passes = data.query(short_middle_query)
        short_right_passes = data.query(short_right_query)

        runs_middle = data.query(run_middle_query)
        runs_left_guard = data.query(run_left_guard_query)
        runs_left_tackle = data.query(run_left_tackle_query)
        runs_left_end = data.query(run_left_end_query)
        runs_right_guard = data.query(run_right_guard_query)
        runs_right_tackle = data.query(run_right_tackle_query)
        runs_right_end = data.query(run_right_end_query)

        grid_dict = {
            "runs": {
                "left": {
                    "guard": {
                        stat: 0,
                        "percentage": 0
                    },
                    "tackle": {
                        stat: 0,
                        "percentage": 0
                    },
                    "end": {
                        stat: 0,
                        "percentage": 0
                    }
                },
                "middle": {
                    stat: 0,
                    "percentage": 0
                },
                "right": {
                    "guard": {
                        stat: 0,
                        "percentage": 0
                    },
                    "tackle": {
                        stat: 0,
                        "percentage": 0
                    },
                    "end": {
                        stat: 0,
                        "percentage": 0
                    }
                }
            },
            "passes": {
                "left": {
                    "short": {
                        stat: 0,
                        "percentage": 0
                    },
                    "deep": {
                        stat: 0,
                        "percentage": 0
                    }
                },
                "middle": {
                    "short": {
                        stat: 0,
                        "percentage": 0
                    },
                    "deep": {
                        stat: 0,
                        "percentage": 0
                    }
                },
                "right": {
                    "short": {
                        stat: 0,
                        "percentage": 0
                    },
                    "deep": {
                        stat: 0,
                        "percentage": 0
                    }
                }
            }
        }

        grid_dict["runs"]["middle"][stat] = round(runs_middle[stat].mean(), 4)
        grid_dict["runs"]["middle"]["percentage"] = round(len(runs_middle) / len(all_plays), 4)
        grid_dict["runs"]["left"]["guard"][stat] = round(runs_left_guard[stat].mean(), 4)
        grid_dict["runs"]["left"]["guard"]["percentage"] = round(len(runs_left_guard) / len(all_plays), 4)
        grid_dict["runs"]["left"]["tackle"][stat] = round(runs_left_tackle[stat].mean(), 4)
        grid_dict["runs"]["left"]["tackle"]["percentage"] = round(len(runs_left_tackle) / len(all_plays), 4)
        grid_dict["runs"]["left"]["end"][stat] = round(runs_left_end[stat].mean(), 4)
        grid_dict["runs"]["left"]["end"]["percentage"] = round(len(runs_left_end) / len(all_plays), 4)
        grid_dict["runs"]["right"]["guard"][stat] = round(runs_right_guard[stat].mean(), 4)
        grid_dict["runs"]["right"]["guard"]["percentage"] = round(len(runs_right_guard) / len(all_plays), 4)
        grid_dict["runs"]["right"]["tackle"][stat] = round(runs_right_tackle[stat].mean(), 4)
        grid_dict["runs"]["right"]["tackle"]["percentage"] = round(len(runs_right_tackle) / len(all_plays), 4)
        grid_dict["runs"]["right"]["end"][stat] = round(runs_right_end[stat].mean(), 4)
        grid_dict["runs"]["right"]["end"]["percentage"] = round(len(runs_right_end) / len(all_plays), 4)

        grid_dict["passes"]["left"]["short"][stat] = round(short_left_passes[stat].mean(), 4)
        grid_dict["passes"]["left"]["short"]["percentage"] = round(len(short_left_passes) / len(all_plays), 4)
        grid_dict["passes"]["left"]["deep"][stat] = round(deep_left_passes[stat].mean(), 4)
        grid_dict["passes"]["left"]["deep"]["percentage"] = round(len(deep_left_passes) / len(all_plays), 4)
        grid_dict["passes"]["middle"]["short"][stat] = round(short_middle_passes[stat].mean(), 4)
        grid_dict["passes"]["middle"]["short"]["percentage"] = round(len(short_middle_passes) / len(all_plays), 4)
        grid_dict["passes"]["middle"]["deep"][stat] = round(deep_middle_passes[stat].mean(), 4)
        grid_dict["passes"]["middle"]["deep"]["percentage"] = round(len(deep_middle_passes) / len(all_plays), 4)
        grid_dict["passes"]["right"]["short"][stat] = round(short_right_passes[stat].mean(), 4)
        grid_dict["passes"]["right"]["short"]["percentage"] = round(len(short_right_passes) / len(all_plays), 4)
        grid_dict["passes"]["right"]["deep"][stat] = round(deep_right_passes[stat].mean(), 4)
        grid_dict["passes"]["right"]["deep"]["percentage"] = round(len(deep_right_passes) / len(all_plays), 4)

        return grid_dict


# League methods


class League:
    """Methods for returning league-wide information"""

    @classmethod
    def stat_per_play_off(cls, operation, stat, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns Expected Points Added per play for combination of 'quarter', 'down', and 'play' and calculates based on operation.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team,
                                x.stat_per_play_off(operation, stat,
                                                    **kwargs)))
        return league_data

    @classmethod
    def stat_per_play_def(cls, operation, stat, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns Expected Points Added per play for combination of 'quarter', 'down', and 'play' and calculates based on operation.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team,
                                x.stat_per_play_def(operation, stat,
                                                    **kwargs)))
        return league_data

    @classmethod
    def positive_play_percentage_offense(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays that increased team's expected points
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team,
                                x.positive_play_percentage_offense(**kwargs)))
        return league_data

    @classmethod
    def positive_play_percentage_defense(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays that increased team's expected points
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team,
                                x.positive_play_percentage_defense(**kwargs)))
        return league_data

    @classmethod
    def qb_pressure_offense(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays where qb was either hit or sacked.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team, x.qb_pressure_offense(**kwargs)))
        return league_data

    @classmethod
    def qb_pressure_defense(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of plays where qb was either hit or sacked.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team, x.qb_pressure_defense(**kwargs)))
        return league_data

    @classmethod
    def interceptions_per_pass_off(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of passes intercepted.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team, x.interceptions_per_pass_off(**kwargs)))
        return league_data

    @classmethod
    def interceptions_per_pass_def(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns percentage of passes intercepted.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team, x.interceptions_per_pass_def(**kwargs)))
        return league_data

    @classmethod
    def margin_for_stat(cls, operation, stat, side, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns margin between offensive and defensive performance per play for combination of 'quarter', 'down', 'half', and 'play'.
        Calculated pased on operation.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team,
                                x.margin_for_stat(operation, stat, side,
                                                  **kwargs)))
        return league_data

    @classmethod
    def cumulative_for_stat(cls, operation, stat, **kwargs):
        """
        Accepts a required str value operation, either 'mean', 'median', or 'std'.
        Accepts a required str value stat, either 'epa', 'wpa', 'air_epa', or 'air_wpa'.
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns cumulative of offensive and defensive performance per play for combination of 'quarter', 'down', 'half', and 'play'.
        Calculated pased on operation.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team,
                                x.cumulative_for_stat(operation, stat,
                                                      **kwargs)))
        return league_data

    @classmethod
    def qb_pressure_margin(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns margin between defenseive and offensive qb pressure percentage.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team, x.qb_pressure_margin(**kwargs)))
        return league_data

    @classmethod
    def positive_play_percentage(cls, **kwargs):
        """
        Accepts an optional int value for 'down' 1-4 inclusive.
        Accepts an optional int value for 'quarter' 1-5 inclusive.
        Accepts an optional str value for 'play', either 'run', or 'pass'.
        Accepts an optional str value for 'where', either 'home', or 'away'.
        Accepts an optional str value for 'since', one of: 'sep', 'oct', 'nov', or 'dec'.
        Accepts an optional bool value for 'close', True, or False.
        Accepts an optional bool value for 'rz', True, or False.
        Accepts an optional int value for 'half', either 1 or 2.
        Returns margin between defenseive and offensive qb pressure percentage.
        """

        teams = Team.all()
        league_data = []
        for team in teams:
            x = Team(team)
            league_data.append((team, x.positive_play_percentage(**kwargs)))
        return league_data

    @classmethod
    def outliers(cls, ls):
        """
        Takes a list of tuples, or a list of lists of all team values for a given statistic.
        Sub lists or tuples must take the form ('TEAM', statistic), where 'TEAM' is a string and statistic an int or float.
        Calculates the mean and standard deviation.
        Returns a dict of the outliers.
        """

        outliers = {"above": {}, "below": {}}
        nums = []

        for x in ls:
            if str(x[1]).lower() != 'nan':
                nums.append(x[1])

        std = np.std(nums)
        mean = np.mean(nums)

        outliers["mean"] = round(mean, 3)
        outliers["std"] = round(std, 3)

        for x in ls:
            if x[1] > mean + std:
                outliers["above"][x[0]] = x[1]
            if x[1] < mean - std:
                outliers["below"][x[0]] = x[1]
        return outliers

    @classmethod
    def grid(cls, side, stat, **kwargs):
        final_dict = {
            "runs": {
                "left": {
                    "guard": {
                        stat: 0,
                        "percentage": 0
                    },
                    "tackle": {
                        stat: 0,
                        "percentage": 0
                    },
                    "end": {
                        stat: 0,
                        "percentage": 0
                    }
                },
                "middle": {
                    stat: 0,
                    "percentage": 0
                },
                "right": {
                    "guard": {
                        stat: 0,
                        "percentage": 0
                    },
                    "tackle": {
                        stat: 0,
                        "percentage": 0
                    },
                    "end": {
                        stat: 0,
                        "percentage": 0
                    }
                }
            },
            "passes": {
                "left": {
                    "short": {
                        stat: 0,
                        "percentage": 0
                    },
                    "deep": {
                        stat: 0,
                        "percentage": 0
                    }
                },
                "middle": {
                    "short": {
                        stat: 0,
                        "percentage": 0
                    },
                    "deep": {
                        stat: 0,
                        "percentage": 0
                    }
                },
                "right": {
                    "short": {
                        stat: 0,
                        "percentage": 0
                    },
                    "deep": {
                        stat: 0,
                        "percentage": 0
                    }
                }
            }
        }
        teams = Team.all()
        for team in teams:
            x = Team(team)
            team_dict = x.grid(side, stat, **kwargs)

            final_dict["runs"]["middle"]["percentage"] += team_dict["runs"]["middle"]["percentage"]
            final_dict["runs"]["middle"][stat] += team_dict["runs"]["middle"][stat]

            for play in team_dict:
                for direction in team_dict[play]:
                    if not (play == 'runs' and direction == 'middle'):
                        for location in team_dict[play][direction]:
                            for number in team_dict[play][direction][location]:
                                final_dict[play][direction][location][number] += team_dict[play][direction][location][number]

        final_dict["runs"]["middle"]["percentage"] = round(final_dict["runs"]["middle"]["percentage"] / 32, 4)
        final_dict["runs"]["middle"][stat] = round(final_dict["runs"]["middle"][stat] / 32, 4)

        for play in final_dict:
            for direction in team_dict[play]:
                if not (play == 'runs' and direction == 'middle'):
                    for location in team_dict[play][direction]:
                        for number in team_dict[play][direction][location]:
                            final_dict[play][direction][location][number] = round(final_dict[play][direction][location][number] / 32, 4)

        return final_dict


# Matchup methods

class Matchup:
    """Methods for returning matchup data"""

    def __init__(self, home, away):
        self.home = home
        self.away = away

    def __repr__(self):
        return f"Home team is {self.home}, away team is {self.away}."

    @classmethod
    def generate(cls, home, away, operation, stat, **kwargs):
        """Return full matchup info"""

        x = Matchup(home, away)

        home_on_offense = x.home_off_away_def_stat(operation, stat, **kwargs)
        away_on_offense = x.away_off_home_def_stat(operation, stat, **kwargs)

        return {
            f"Margin {home} on offense":
            home_on_offense,
            f"Margin {away} on offense":
            away_on_offense,
            f"{home} overall":
            round(home_on_offense - away_on_offense, 3),
            f"{away} overall":
            round(away_on_offense - home_on_offense, 3)
        }

    def home_off_away_def_stat(self, operation, stat, **kwargs):
        """Home offense versus away defense"""

        home = Team(self.home)
        away = Team(self.away)

        home_o = home.stat_per_play_off(
            operation, stat, where='home', **kwargs)
        away_d = away.stat_per_play_def(
            operation, stat, where='away', **kwargs)

        margin = home_o + away_d

        return round(margin, 3)

    def away_off_home_def_stat(self, operation, stat, **kwargs):
        """Home defense versus away offense"""

        away = Team(self.away)
        home = Team(self.home)

        away_o = away.stat_per_play_off(
            operation, stat, where='away', **kwargs)
        home_d = home.stat_per_play_def(
            operation, stat, where='home', **kwargs)

        margin = away_o + home_d

        return round(margin, 3)