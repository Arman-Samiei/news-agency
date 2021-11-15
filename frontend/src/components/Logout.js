/**
 * Created by Arman Samiei on 4/2/2021.
 */
import React, {Component} from "react";
import backend from "../apis";


class Logout extends Component {
    state = {message: ''}

    componentDidMount() {
        if (localStorage.getItem('token')) {
            backend.post('api/users/logout', {
                    logout: 'true'
                }, {
                    headers: {Authorization: 'Token ' + localStorage.getItem('token')}
                }
            ).then(r => {
                this.props.setLoggedOut()
                localStorage.removeItem('token')
                this.setState({message: 'با موفقیت خارج شدید.'})
                setTimeout(function(){
                    window.location.reload(false)
                }, 3000)
            }).catch(r => {
                this.setState({message: 'خطایی رخ داد.'})
            })
        }
    }

    render() {
        return <div>
            {this.state.message}
        </div>
    }
}

export default Logout;