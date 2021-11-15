import "./App.css";
import {BrowserRouter, Route, Switch, Router, withRouter} from "react-router-dom";
import React, {Component} from "react";
import Home from "./Home";
import Header from "./Header";
import NewsDetail from "./NewsDetail";
import NewsFilterPlayer from "./NewsFilterPlayer";
import NewsFilterTeam from "./NewsFilterTeam";
import LiveScore from "./LiveScore";
import Videos from "./Videos";
import Video from "./Video";
import Register from "./Register";
import Login from "./Login";
import ForgotPassword from "./ForgotPassword";
import FavoriteTeam from "./FavoriteTeam";
import BooleanSearchResults from "./BooleanSearchResults";
import RankedRetrieval from "./RankedRetrieval"
import Logout from "./Logout";
import backend from "../apis";
class App extends Component {
    state = {isLoggedIn: false, isLoggedOut: false}

    setLoggedIn = () => {
        // backend.get('api/users/test', {
        //     headers: {
        //         Authorization: 'Token ' + localStorage.getItem('token')
        //     }
        // })
        this.setState({isLoggedIn: true})
    }

    setLoggedOut = () => {
        this.setState({isLoggedOut: true})
    }

    render() {
        return (
            <BrowserRouter>
                <Header />
                <Switch>

                    <Route exact path='/'
                           render={(props) => <Home {...props} />}/>
                    <Route exact path='/newsdetail/:newsid'
                           render={(props) => <NewsDetail {...props} />}/>
                    <Route exact path='/newsfilterplayer/:playerId'
                           render={(props) => <NewsFilterPlayer {...props} />}/>
                    <Route exact path='/newsfilterteam/:teamId'
                           render={(props) => <NewsFilterTeam {...props} />}/>
                    <Route exact path='/livescore'
                           render={(props) => <LiveScore {...props} />}/>
                    <Route exact path='/videos'
                           render={(props) => <Videos {...props} />}/>
                    <Route exact path='/videos/video/:videoid'
                           render={(props) => <Video {...props} />}/>
                    <Route exact path='/register'
                           render={(props) => <Register {...props} />}/>
                    <Route exact path='/login'
                           render={(props) => <Login setLoggedIn={this.setLoggedIn} {...props} />}/>
                    <Route exact path='/forgotpassword'
                           render={(props) => <ForgotPassword {...props} />}/>
                    <Route exact path='/favoriteteam'
                           render={(props) => <FavoriteTeam {...props} />}/>
                    <Route exact path='/rankedretrieval/:query'
                           render={(props) => <RankedRetrieval {...props} />}/>
                    <Route exact path='/booleansearchresults/:query'
                           render={(props) => <BooleanSearchResults {...props} />}/>
                    <Route exact path='/logout'
                           render={(props) => <Logout setLoggedOut={this.setLoggedOut} {...props} />}/>
                </Switch>
            </BrowserRouter>
        )

    }

}
export default App;