/**
 * Created by Arman Samiei on 2/27/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import left_arrow from '../images/left_arrow.png'
import right_arrow from '../images/right_arrow.png'
import LeagueMatches from './LeagueMatches'
import Standings from './Standings'
class Home extends Component {
    state = {news: [], hottest_news: [], counter: 0, favoriteTeamNews: [], favoriteTeam:''};

    componentDidMount() {
        backend.get('api/news')
            .then(r => {
                this.setState({news: r.data.news})

            })
        backend.get('api/hottestnews')
            .then(r => {
                console.log(r.data.news);
                this.setState({hottest_news: r.data.news})

            })

        if (localStorage.getItem('token')) {
            backend.get('api/users/favoriteteamnews', {
                headers: {Authorization: 'Token ' + localStorage.getItem('token')}
            }).then(r => {
                console.log(r.data.news, 'llllllllllllllll')
                this.setState({favoriteTeamNews: r.data.news, favoriteTeam:r.data.favoriteTeam})
            })
        }

    }

    leftArrowClicked = () => {
        let counter = (this.state.counter + 1) % this.state.hottest_news.length;
        console.log(counter)
        this.setState({counter: counter});
    }
    rightArrowClicked = () => {
        let counter = this.state.counter - 1;
        if (counter === -1)
            counter = this.state.hottest_news.length - 1;
        this.setState({counter: counter});
    }
    handleThumbnailClick = (index) => {
        this.setState({counter: index})
    }
    renderFavoriteTeam = () =>{
        if(this.state.favoriteTeam != ''){
            return <div className="favorite-team-news">
                <h1>اخبار تیم {this.state.favoriteTeam}</h1>
                {this.state.favoriteTeamNews.map(e => {
                    return <Link className="news-titles" to={`newsdetail/${e.id}`}>{e.title}</Link>
                })}
            </div>
        }
    }
    render() {
        if (this.state.hottest_news.length == 0)
            return null;
        return <div>
            <div className="hottest">
                <div className="hottest-gallery">

                    <div className="hottest-gallery-main-img">
                        <Link to={`newsdetail/${this.state.hottest_news[this.state.counter].id}`}><img
                            src={`${backendUrl}${this.state.hottest_news[this.state.counter].image}`}
                            name="image0"/></Link>
                        <p>{this.state.hottest_news[this.state.counter].title}</p>
                        <div className="hottest-gallery-buttons">
                            <div>
                                <div onClick={this.leftArrowClicked} className="left-arrow">
                                    <img src={left_arrow}/>
                                </div>
                                <div onClick={this.rightArrowClicked} className="right-arrow">
                                    <img src={right_arrow}/>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="hottest-gallery-thumbnails-container">
                        {this.state.hottest_news.map((e, index) => {
                            return <div onClick={this.handleThumbnailClick.bind(this, index)} className="thumbnail"
                                        id="thumbnail0">
                                <img src={`${backendUrl}${e.image}`}/>
                                <p>{e.title}</p>
                                <div className="thumbnail-middle">
                                    <div className="thumbnail-text"><span className="svg-icon block" data-v-638cc802=""><svg
                                        viewBox="0 0 22 13"
                                        version="1.1"
                                        fill="" width="22px"
                                        height="13px"
                                        className="svg-icon"
                                        data-v-638cc802=""><g
                                        stroke="none" strokeWidth="1" fill="none" fill-rule="evenodd"><g
                                        id="Tour-Detail-[if-select-2room]---Desktop"
                                        transform="translate(-1095.000000, -1777.000000)" fill="currentColor"
                                        fillRule="nonzero"><g
                                        id="Group-13" transform="translate(607.000000, 1532.000000)"><path
                                        d="M498.9944,245 C493.937949,245.003931 489.443175,247.501581 488.033392,251.313119 C487.988869,251.433399 487.988869,251.566591 488.033392,251.686871 C489.444349,255.501583 493.944973,257.999754 499.005624,258 C504.062076,257.996069 508.556825,255.498419 509.966608,251.686871 C510.011131,251.566591 510.011131,251.433399 509.966608,251.313119 C508.55565,247.498417 504.055052,245.000246 498.9944,245 Z M499.000164,247.080003 C501.338501,247.080003 503.250187,249.068135 503.250187,251.499995 C503.250187,253.931855 501.338501,255.919997 499.000164,255.919997 C496.661827,255.919997 494.750142,253.931855 494.750142,251.499995 C494.750142,249.068135 496.661827,247.080003 499.000164,247.080003 Z M499.000164,248.640002 C497.472481,248.640002 496.25015,249.911223 496.25015,251.499995 C496.25015,253.088767 497.472481,254.359998 499.000164,254.359998 C500.527847,254.359998 501.750179,253.088767 501.750179,251.499995 C501.750179,249.911223 500.527847,248.640002 499.000164,248.640002 Z"
                                        id="Shape"></path></g></g></g></svg></span>
                                    </div>
                                </div>
                            </div>

                        })}
                    </div>
                </div>
                {this.renderFavoriteTeam()}
                <div className="news-titles-container">
                    {this.state.news.map(e => {
                        return <Link className="news-titles" to={`newsdetail/${e.id}`}>{e.title}</Link>
                    })}
                </div>
            </div>
            <LeagueMatches />
            <Standings />
        </div>

    }

}
export default Home;