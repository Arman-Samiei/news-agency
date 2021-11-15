/**
 * Created by Arman Samiei on 3/5/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './LeagueMatches.css'

class LeagueMatches extends Component {
    state = {
        matches: [],
        league: 'premierLeague',
        fixture: {'premierLeague': 1, 'bundesliga': 1, 'laliga': 1, 'serieA': 1}
    };

    leaguesPersianToEnglish = {
        'لیگ برتر انگلیس': 'premierLeague',
        'بوندسلیگا': 'bundesliga',
        'لالیگا': 'laliga',
        'سری آ': 'serieA'
    }

    componentDidMount() {
        backend.get('api/leagueMatches')
            .then(r => {
                this.setState({matches: r.data.matches})

            })
        backend.get('api/max_fixture_leagues')
            .then(r => {
                console.log(r.data)
                this.setState({fixture: r.data})

            })
    }


    renderMatches = () => {

        return <div className="Matches">
            {this.state.matches.map(match => {
                if (this.leaguesPersianToEnglish[match.League] != this.state.league || match.week != this.state.fixture[this.leaguesPersianToEnglish[match.League]])
                    return null
                return <div>
                    {match.host} {match.finished ? match.host_score : null} - {match.guest} {match.finished ? match.guest_score : null}
                </div>
            })}
        </div>


    }

    renderFixtures = () => {
        // let matches = this.groupBy(this.state.matches, 'week')
        // let fixtures = Object.entries(matches).length
        let fixtures = 38;
        if (this.state.league == 'bundesliga')
            fixtures = 34;
        let fixtures_arr = new Array(fixtures);
        for (let i = 0; i < fixtures; i++) {
            fixtures_arr[i] = i + 1
        }
        let englishLeague = this.state.league;
        let stateFixture = {...this.state.fixture};

        return <select className="fixture-option"
                       onChange={(e) => {
                            stateFixture[englishLeague] = e.target.value;
                            this.setState({fixture: {...stateFixture}})
                        }}
                       value={this.state.fixture[englishLeague]}>
            {fixtures_arr.map(e => {
                return <option value={e}>هفته {e}</option>
            })}
        </select>
    }

    renderLeagues = () => {
        return <select className="league-option" onChange={(e) => {
            this.setState({league: e.target.value})
        }} value={this.state.league} name="league" id="league">
            <option value="premierLeague">لیگ برتر انگلیس</option>
            <option value="serieA">سری آ</option>
            <option value="bundesliga">بوندسلیگا</option>
            <option value="laliga">لالیگا</option>
        </select>
    }

    render() {
        if (this.state.matches.length == 0)
            return null;
        return <div className="League-matches-teams-container">
            {this.renderLeagues()}
            {this.renderFixtures()}
            {this.renderMatches()}
        </div>
    }
}
export default LeagueMatches;