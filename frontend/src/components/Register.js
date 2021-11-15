/**
 * Created by Arman Samiei on 3/13/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import {withRouter} from 'react-router-dom'
import './login_register.css'

class Register extends Component {
    state = {
        state: "enterEmail",
        email: "",
        code: "",
        mainPassword: "",
        confirmPassword: "",
        passwordsNotMatch: false,
        wrongConfCode: false,
        isSignedUp: false
    }
    renderContent = () => {
        if (this.state.state == "enterEmail") {
            return <form className="login-register-form" onSubmit={this.handleEmailSubmit}>
                <input onChange={this.handleEmailChange} type="email" placeholder="ایمیل"/>
                <input type="submit" value="ارسال"/>
            </form>
        }
        else if (this.state.state == "enterCode") {
            return <form className="login-register-form" onSubmit={this.handleConfirmationCodeSubmit}>
                <div className="entering-code">کد تایید ارسال شده به ایمیل را وارد کنید</div>
                <input type="text" onChange={this.handleConfirmationCodeChange} placeholder="کد تایید"/>
                <input type="submit" value="ارسال" />
            </form>
        }
        else if (this.state.state == "enterPassword") {
            return <form className="login-register-form" onSubmit={this.handlePasswordsSubmit}>
                <input type="password" onChange={(e) => this.handlePassword(e, true)} placeholder="رمزعبور"/>
                <input type="password" onChange={(e) => this.handlePassword(e, false)} placeholder="تکرار رمز عبور"/>
                <input type="submit" value="ارسال"/>
            </form>
        }
    }
    handleEmailSubmit = (e) => {
        e.preventDefault()
        backend.post('api/users/confirmationcode', {
            email: this.state.email
        })
            .then(res => {
                this.setState({state: "enterCode"})

            })

    }
    handleEmailChange = (e) => {
        this.setState({email: e.target.value})
    }
    handleConfirmationCodeSubmit = (e) => {
        e.preventDefault()
        backend.post('api/users/checkconfirmationcode', {
            email: this.state.email,
            confirmationcode: this.state.code
        })
            .then(res => {
                this.setState({state: 'enterPassword'})
            })
            .catch(e => {
                if (e.response.status == 403) {
                    this.setState({wrongConfCode: true})
                }
            })
    }
    handleConfirmationCodeChange = (e) => {
        this.setState({code: e.target.value})
    }
    handlePassword = (e, isMainPassword) => {
        if (isMainPassword == true)
            this.setState({mainPassword: e.target.value})
        else
            this.setState({confirmPassword: e.target.value})
    }
    handlePasswordsSubmit = (e) => {
        e.preventDefault();
        if (this.state.mainPassword != this.state.confirmPassword) {
            this.setState({passwordsNotMatch: true})
            console.log('heil')
            return;
        }
        backend.post('api/users/setpassword', {
            email: this.state.email,
            password: this.state.mainPassword,
        })
            .then(res => {
                this.props.history.push('/login')
            })
            .catch(e => {
                if (e.response.status == 403) {
                    this.setState({isSignedUp: true})
                }
            })


    }

    renderUserIsSignedUp = () => {
        if (this.state.isSignedUp) {
            return <div className="failure">شما قبلاً ثبت نام کردید</div>
        }
        return null
    }

    renderPasswordNotMatchError = () => {
        if (this.state.passwordsNotMatch) {
            return <div className="failure">عدم تطابق رمزها</div>
        }
        return null
    }

    renderWrongConfCodeError = () => {
        if (this.state.wrongConfCode)
            return <div className="failure">کد تایید وارد شده صحیح نیست</div>
        return null
    }

    render() {
        return <div>
            {this.renderPasswordNotMatchError()}
            {this.renderWrongConfCodeError()}
            {this.renderUserIsSignedUp()}
            {this.renderContent()}
        </div>
    }
}

export default withRouter(Register)