/**
 * Created by Arman Samiei on 3/29/2021.
 */
import React, {Component} from 'react'
import backend, {backendUrl} from '../apis'
import {Link} from 'react-router-dom'
import './login_register.css'
class ForgotPassword extends Component{
    state={email:'', error:false, success:false}
    render() {
        return <div>
            <form className="login-register-form" onSubmit={this.handleSubmit}>
                <input type="email" onChange={this.handleEmailChange} placeholder="ایمیل"/>
                <input type="submit" value="ارسال"/>
            </form>
        </div>
        {this.successful()}
        {this.renderErrorMessage()}
    }
    handleEmailChange =(e) =>{
        this.setState({email:e.target.value})
    }
    successful = () =>{
        if(this.state.success === true){
            return <div className="success">رمز عبور به ایمیل ارسال شد</div>
        }
        this.setState({error:false})
    }
    renderErrorMessage = () =>{
        if(this.state.error === true)
            return <div className="failure">شما ثبت نام نکرده اید.</div>
    }
    handleSubmit = (e) =>{
        e.preventDefault()
        backend.post('api/users/forgotpassword', {
            email: this.state.email
        })
            .then(res => {
                this.setState({success:true})

            })
            .catch(res =>{
                this.setState({error:true})
            })
    }
}
export default ForgotPassword;