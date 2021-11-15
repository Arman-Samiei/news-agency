/**
 * Created by Arman Samiei on 3/1/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import './NewsDetail.css'
import {Link} from 'react-router-dom'

class NewsDetail extends Component {
    state = {}

    componentDidMount() {

        backend.get(`api/newsdetail/${this.props.match.params.newsid}`)
            .then(r => {
                this.setState({
                    title: r.data.title,
                    image: r.data.image,
                    text: r.data.text,
                    players: r.data.players_label,
                    teams: r.data.teams_label
                })

            })


    }

    render() {
        if (this.state.title == null)
            return null;
        return <div>
            <h1>{this.state.title}</h1>
            <img src={`${backendUrl}${this.state.image}`}/>
            <p>{this.state.text}</p>
            <div className="filters">
                {this.state.players.map(e => {
                    return <Link className="filter" to={`/newsfilterplayer/${e.id}`}>{e.name}</Link>
                })}
                {this.state.teams.map(e => {
                    return <Link className="filter" to={`/newsfilterteam/${e.id}`}>{e.name}</Link>
                })}
            </div>
        </div>
    }
}
export default NewsDetail;