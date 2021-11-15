/**
 * Created by Arman Samiei on 3/29/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'

class FavoriteTeam extends Component {
    state = {teams: [], favoriteTeam: null};

    componentDidMount() {
        backend.get('api/teams')
            .then(r => {
                this.setState({teams: r.data.teams, favoriteTeam: r.data.teams[0].id})

            })
    }

    handleSubmit = (e) => {
        e.preventDefault()
        backend.post('api/users/favoriteteam', {
            favoriteTeam: this.state.favoriteTeam
        }, {
            headers: {Authorization: 'Token ' + localStorage.getItem('token')}
        })
    }

    handleChange = (e) => {
        this.setState({favoriteTeam: e.target.value})
    }

    render() {
        if (this.state.teams.length == 0)
            return null;
        return <form className="Favorite-team-selection" onSubmit={this.handleSubmit}>
            <select className="teams-option" value={this.state.favoriteTeam} onChange={this.handleChange}>
                {this.state.teams.map(e => {
                    return <option value={e.id}>{e.name}</option>
                })}
            </select>
            <input type="submit" value="ارسال"/>
        </form>
    }
}
export default FavoriteTeam;