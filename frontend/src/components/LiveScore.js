/**
 * Created by Arman Samiei on 3/3/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './LiveScore.css'

class LiveScore extends Component {
    state = {matches: [], showTodayMatches: true}
    interval = null

    componentDidMount() {
        this.getMatches();
        this.interval = setInterval(() => {
            this.getMatches();
        }, 10000)


    }

    groupBy = (objectArray, property) => {
        return objectArray.reduce((acc, obj) => {
            const key = obj[property];
            if (!acc[key]) {
                acc[key] = [];
            }
            // Add object to list for given key's value
            acc[key].push(obj);
            return acc;
        }, {});
    }

    getMatches = () => {
        backend.get(`api/livescore`)
            .then(r => {
                console.log(r.data.matches)
                this.setState({matches: r.data.matches})
            })
    }
    showTodayMatches = () => {
        this.setState({showTodayMatches: true})
    }

    showYesterdayMatches = () => {
        this.setState({showTodayMatches: false})
    }

    renderMatches = () => {
        let matchesToShow = null;
        if (this.state.showTodayMatches == true) {
            matchesToShow = this.state.matches.filter(e => {
                return e.today == true
            })
        }
        else {
            matchesToShow = this.state.matches.filter(e => {
                return e.today == false
            })
        }
        matchesToShow = this.groupBy(matchesToShow, 'League')
        console.log(matchesToShow);
        return (
            <React.Fragment>
                {Object.entries(matchesToShow).map(([key, value]) => {
                    console.log(value);
                    return <React.Fragment>
                        <div className="league">{key}</div>
                        {value.map(e => {
                            return <div>
                                <span>{e.match_date}</span>
                                <span>{e.time}</span>
                                <span>{e.host}</span>
                                <span>{e.host_score}</span>
                                <span> - </span>
                                <span>{e.guest}</span>
                                <span>{e.guest_score}</span>
                                {e.finished ? <span>نتیجه نهایی</span> : null}
                            </div>

                        })}
                    </React.Fragment>
                })}
            </React.Fragment>)


    }

    componentWillUnmount() {
        window.clearInterval(this.interval)
    }

    render() {
        if (this.state.matches.length == 0)
            return null;
        return <div className="livescore-container">
            <button onClick={this.showTodayMatches} type="button">بازی های امروز</button>
            <button onClick={this.showYesterdayMatches} type="button">بازی های دیروز</button>
            {this.renderMatches()}
        </div>
    }
}
export default LiveScore;