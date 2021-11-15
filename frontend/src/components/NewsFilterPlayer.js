/**
 * Created by Arman Samiei on 3/2/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './NewsFilterSearch.css'
class NewsFilterPlayer extends Component {
    state = {news: [], videos: []}

    componentDidMount() {

        backend.get(`api/newsfilterplayer/${this.props.match.params.playerId}`)
            .then(r => {
                this.setState({
                    news: r.data.news,
                    videos: r.data.videos
                })

            })
    }

    render() {
        if (this.state.news.length == 0 && this.state.videos.length == 0)
            return null;
        return <div>
            {this.state.news.map(e => {
                return <Link className="filtered-news-item" to={`/newsdetail/${e.id}`}><img src={backendUrl + e.image}/>
                    <h5>{e.title}</h5></Link>
            })}
            {this.state.videos.map(e => {
                return <Link className="filtered-videos-item" to={`/videos/video/${e.id}`}><img
                    src={backendUrl + e.image}/><h5>{e.title}(ویدئو)</h5></Link>
            })}
        </div>
    }
}
export default NewsFilterPlayer;