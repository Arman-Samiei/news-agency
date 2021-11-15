/**
 * Created by Arman Samiei on 3/9/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './LeagueMatches.css'
import './Standings.css'

class Standings extends Component {
    state = {teams: [], league: 'premierLeague'};

    leaguesPersianToEnglish = {
        'لیگ برتر انگلیس': 'premierLeague',
        'بوندسلیگا': 'bundesliga',
        'لالیگا': 'laliga',
        'سری آ': 'serieA'
    }

    componentDidMount() {
        backend.get('api/standings')
            .then(r => {
                this.setState({teams: r.data.teams})

            })

    }



    renderTeams = () => {
        var rank = 1;
        this.state.teams = this.state.teams
            .sort((a, b) => a.score > b.score ? -1 : 1)

        // this.state.teams.sort();
        return <table className="teams">
            {this.state.teams.map(team => {
                if (this.leaguesPersianToEnglish[team.league] != this.state.league)
                    return null;
                return <tr>

                    <td className="teams-score">{team.score}</td>
                    <td className="teams-name">{team.name}</td>
                    <td className="teams-rank">{rank++}</td>
                </tr>
            })}
        </table>


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
        if (this.state.teams.length == 0)
            return null;
        return <div className="League-matches-teams-container">
            {this.renderLeagues()}
            {this.renderTeams()}
        </div>
    }
}
export default Standings;