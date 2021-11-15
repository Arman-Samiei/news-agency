/**
 * Created by Arman Samiei on 3/9/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './Videos.css'
class Videos extends Component {
    state = {videos: []};

    componentDidMount() {
        backend.get('api/videos')
            .then(r => {
                this.setState({videos: r.data.videos})

            })
    }

    render() {
        if (this.state.videos.length == 0)
            return null;
        return <div className="videos">
            {this.state.videos.map(e => {
                return <div>< Link to={`video/${e.id}`}><img
                    src={`${backendUrl}${e.image}`}
                    name="image0"/>
                    <p>{e.title}</p></Link>
                </div>
            })}
        </div>

    }

}
export default Videos;