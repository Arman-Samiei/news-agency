/**
 * Created by Arman Samiei on 8/3/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import './NewsDetail.css'
import {Link} from 'react-router-dom'

class RankedRetrieval extends Component {
    state = {news: [], videos: []}

    getNews = () => {
        backend.post('api/rankedretrieval', {
            query: this.props.match.params.query,
        })
            .then(r => {
                this.setState({news: r.data.news})
            })
            .catch(res => {
                this.setState({error: true, news: []})
            })
    }

    componentDidMount() {
        this.getNews()
    }

    componentDidUpdate(prevProps) {
        if (this.props.match.params.query == prevProps.match.params.query) {
            return
        }

        this.getNews()
    }

    render() {
        if (!this.state.news)
            return null
        return <div>
            {this.state.news.map(e => {
                return <Link className="searched-news-item" to={`/newsdetail/${e.id}`}><img src={backendUrl + e.image}/><h5>{e.title}</h5></Link>

            })}

        </div>
    }
}

export default RankedRetrieval
