import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import './NewsDetail.css'
import {Link} from 'react-router-dom'

class booleanSearchResults extends Component {
    state = {news: [], videos: []}

    getNews = () => {
        console.log('hei')
        backend.post('api/booleansearch', {
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
        console.log('hrillll')
        this.getNews()
    }

    componentDidUpdate(prevProps) {
        console.log('heilll')
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

export default booleanSearchResults
