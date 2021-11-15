/**
 * Created by Arman Samiei on 3/9/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './video.css'
class Videos extends Component {
    state = {};

    componentDidMount() {
        backend.get(`api/videos/video/${this.props.match.params.videoid}`)
            .then(r => {
                this.setState({
                    title: r.data.title,
                    content: r.data.content,
                    players: r.data.players_label,
                    teams: r.data.teams_label,

                })

            })
    }

    render() {
        if (this.state.title == null)
            return null;
        return <div className="video-container">
                <video className="video" autoPlay="true" controls><source src={`${backendUrl}${this.state.content}`}/>this.state.content</video>
                <p className="video-title">{this.state.title}</p>
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
export default Videos;