CREATE TABLE `stats` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`team`	TEXT NOT NULL,
	`year`	INTEGER NOT NULL,
	`off_def`	TEXT NOT NULL,
	`points`	INTEGER DEFAULT 0,
	`points_per_game`	REAL DEFAULT 0,
	`points_off_turnovers`	INTEGER DEFAULT 0,
	`first_downs`	INTEGER DEFAULT 0,
	`rush_first_downs`	INTEGER DEFAULT 0,
	`pass_first_downs`	INTEGER DEFAULT 0,
	`penalty_first_downs`	INTEGER DEFAULT 0,
	`rush_yards`	INTEGER DEFAULT 0,
	`rush_yards_gained`	INTEGER DEFAULT 0,
	`rush_yards_lost`	INTEGER DEFAULT 0,
	`rush_attempts`	INTEGER DEFAULT 0,
	`rush_yards_per_attempt`	REAL DEFAULT 0,
	`rush_yards_per_game`	REAL DEFAULT 0,
	`rush_td`	INTEGER DEFAULT 0,
	`pass_yards`	INTEGER DEFAULT 0,
	`pass_attempts`	INTEGER DEFAULT 0,
	`pass_completions`	INTEGER DEFAULT 0,
	`interceptions`	INTEGER DEFAULT 0,
	`pass_yards_per_attempt`	REAL DEFAULT 0,
	`pass_yards_per_completion`	REAL DEFAULT 0,
	`pass_td`	INTEGER DEFAULT 0,
	`yards`	INTEGER DEFAULT 0,
	`plays`	INTEGER DEFAULT 0,
	`yards_per_play`	REAL DEFAULT 0,
	`fumbles`	INTEGER DEFAULT 0,
	`fumbles_lost`	INTEGER DEFAULT 0,
	`penalties`	INTEGER DEFAULT 0,
	`penalty_yards`	INTEGER DEFAULT 0,
	`kickoff_attempts`	INTEGER DEFAULT 0,
	`kickoff_yards`	INTEGER DEFAULT 0,
	`kickoff_yards_per_attempt`	REAL DEFAULT 0,
	`kickoff_net_yards_per_attempt`	REAL DEFAULT 0,
	`time_of_possession_per_game`	INTEGER DEFAULT 0,
	`third_down_attempts`	INTEGER DEFAULT 0,
	`third_down_conversions`	INTEGER DEFAULT 0,
	`third_down_pct`	REAL DEFAULT 0,
	`fourth_down_attempts`	INTEGER DEFAULT 0,
	`fourth_down_conversions`	INTEGER DEFAULT 0,
	`fourth_down_pct`	REAL DEFAULT 0,
	`sacks_by`	INTEGER DEFAULT 0,
	`sacks_yards`	INTEGER DEFAULT 0,
	`yards_misc`	INTEGER DEFAULT 0,
	`touchdowns`	INTEGER DEFAULT 0,
	`red_zone_attempts`	INTEGER DEFAULT 0,
	`red_zone_scores`	INTEGER DEFAULT 0,
	`red_zone_score_pct`	REAL DEFAULT 0,
	`red_zone_touchdowns`	INTEGER DEFAULT 0,
	`red_zone_td_pct`	REAL DEFAULT 0,
	`kick_return_attempts`	INTEGER DEFAULT 0,
	`kick_return_yards`	INTEGER DEFAULT 0,
	`punt_return_attempts`	INTEGER DEFAULT 0,
	`punt_return_yards`	INTEGER DEFAULT 0,
	`int_return_attempts`	INTEGER DEFAULT 0,
	`int_return_yards`	INTEGER DEFAULT 0,
	`kick_return_yards_per_attempt`	REAL DEFAULT 0,
	`punt_return_yards_per_attempt`	REAL DEFAULT 0,
	`int_return_yards_per_attempt`	REAL DEFAULT 0,
	`punt_attempts`	INTEGER DEFAULT 0,
	`punt_yards`	INTEGER DEFAULT 0,
	`punt_yards_per_attempt`	REAL DEFAULT 0,
	`punt_net_yards_per_attempt`	REAL DEFAULT 0,
	`field_goal_attempts`	INTEGER DEFAULT 0,
	`field_goal_makes`	INTEGER DEFAULT 0,
	`onside_kick_attempts`	INTEGER DEFAULT 0,
	`onside_kick_makes`	INTEGER DEFAULT 0,
	`pat_attempts`	INTEGER DEFAULT 0,
	`pat_makes`	INTEGER DEFAULT 0,
	`pat_pct`	REAL DEFAULT 0,
	`attendance`	INTEGER DEFAULT 0,
	`games`	INTEGER DEFAULT 0,
	`attendance_per_game`	REAL DEFAULT 0,
	`games_neutral`	INTEGER DEFAULT 0,
	`games_neutral_attendance_per_game`	REAL DEFAULT 0
);
