/**
 * Created by Arman Samiei on 3/24/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link, withRouter} from 'react-router-dom'
import './login_register.css'

class Login extends Component {
    state = {email: '', password: '', error:false}

    handleEmailChange = (e) => {
        this.setState({email: e.target.value})
    }

    handlePasswordChange = (e) => {
        this.setState({password: e.target.value})
    }

    handleSubmit = (e) => {
        e.preventDefault()
        backend.post('api/users/login', {
            email: this.state.email,
            password: this.state.password,
        })
            .then(res => {
                localStorage.setItem('token', res.data.token)
                this.props.setLoggedIn()
                this.props.history.push('/')
            })
            .catch(res => {
                this.setState({error:true})
            })
    }
    handleError = () =>{
        if(this.state.error == true)
            return <div className="failure">ورود ناموفق</div>
    }
    render() {
        return <div>
            {this.handleError()}
            <form className="login-register-form" onSubmit={this.handleSubmit}>
                <input type="email" onChange={this.handleEmailChange} placeholder="ایمیل"/>
                <input type="password" onChange={this.handlePasswordChange} placeholder="رمز عبور"/>
                <input type="submit" value="ورود"/>
            </form>
            <Link to="/register">ثبت نام</Link>
            <Link to="/forgotpassword">رمز عبور را فراموش کرده ام.</Link>
        </div>
    }
}

export default withRouter(Login)