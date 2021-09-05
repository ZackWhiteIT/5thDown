# Fifthdown
Data behind the blocking and tackling

## About the Project

Fifthdown is a data analytics project to research Division I football programs. The hope is to identify trends and key metrics within college football.

### Key Features

- Data scraper
- [Elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system)
- Visualizations

### A Little More About Elo

The fine folks at Staturdays have a great explainer on [building Elo ratings](https://staturdays.com/2020/08/11/introducing-college-football-elo-ratings/) for college football. Their work is an inspiration for this project, but the scope of the their efforts and Fifthdown differ:
1. Staturday's focus is on breadth of various stats related to FBS teams (although they do have some ratings for FCS). Fifthdown's purpose is depth of Elo ratings across all divisions of college football (and eventually high school football).
2. Fifthdown has a pure web spider to retrieve team-level data for teams not currently in free college football APIs (at least those known to the devs).

## Installation
`python setup.py install`

or if you prefer virtualenv...

```
virtualenv venv
source venv/bin/activate
python setup.py install
```

## Dependencies

- [Requests](https://docs.python-requests.org/en/master/index.html)
- [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
- [College Football Data API](https://www.collegefootballdata.com/)
- [Jupyter](https://jupyter.org/)
- [GitHub Flat Data](https://next.github.com/projects/flat-data)
- [Click](https://click.palletsprojects.com/en/8.0.x/)
- [Records](https://github.com/kennethreitz/records)
- [Seaborn](https://seaborn.pydata.org/)

### Additional Setup

- [Setting Up Jupyter Notebooks with VS Code](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)


## Usage
`fifthdown --help`

## Future Research

- [High School Football Advance Stats](https://www.footballstudyhall.com/2018/8/24/17706048/advanced-stats-football-high-school-questions)

## Author(s)

[Zack White](https://github.com/ZackWhiteIT)

## License

This software is licensed under The MIT License (MIT). See the [LICENSE](LICENSE) file in the top distribution directory for the full license text.
