# League of Legends Analytics

League of Legends Analytics is a planned application that helps players choose item builds and runes based on their champion and the champions on both teams.

## Project Goal

The goal is to help players make more informed decisions during champion selection. The application will use champion, item, rune, and match data to generate recommendations suited to the selected matchup and team compositions.

## MVP Scope

The first usable version will focus on:

- Allowing users to enter their champion and both teams’ champion selections.
- Retrieving the game data needed to support recommendations.
- Processing relevant statistics to recommend item builds and rune setups.
- Displaying the recommendations in a simple interface.

The MVP will use manual champion input. Automatic champion detection is outside the initial scope.

## Future Plans

After completing the MVP, planned features include:

- **Team composition suggestions:** Help users identify strengths, weaknesses, and gaps in their team’s composition.
- **Champion suggestions based on playstyle:** Recommend champions that fit a player’s preferred role and style of play.

Flash timers and other summoner spell trackers are outside the project’s planned scope.

## Tech Stack

- **Python:** Main programming language.
- **Riot Games Data Dragon:** JSON files providing champion, item, and rune information.
- **Riot Games API:** Retrieve match histories and individual match statistics for analysis.
- **RiotWatcher:** Python wrapper for Riot’s API, with built-in rate-limit handling.
- **lcu-driver:** Communicate with the local League Client API to read champion selection information.
- **SQLite:** Store collected match data and calculated statistics.
- **pandas and NumPy:** Process match data, calculate win rates, and support item and rune recommendations.
- **CustomTkinter:** Build the desktop interface for entering information and displaying recommendations.
- **Git and GitHub:** Track development progress and host the project.

## Design Documents

The `docs/` folder will contain:

- The Eisenhower Matrix defining project priorities.
- The System Diagram showing the program’s workflow.

## Development Status

This project is currently in the planning stage. Implementation will proceed in manageable stages: data retrieval, data processing, recommendation logic, and interface development. Each completed stage will be recorded through incremental Git commits.
