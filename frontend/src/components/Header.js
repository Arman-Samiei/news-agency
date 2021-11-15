/**
 * Created by Arman Samiei on 3/1/2021.
 */
import React,{Component} from 'react'
import backend, {backendUrl} from '../apis'
import logo from '../images/logo.png'
import searchbar from '../images/searchbar.png'
import {Link} from 'react-router-dom'
import {withRouter} from 'react-router-dom'

class Header extends Component{
    state = {query: '', news:[], error:false}
    handleSearchChange = (e) => {
        this.setState({query: e.target.value})
    }

    handleSearch = (e) => {
        e.preventDefault()
        this.props.history.push(`/rankedretrieval/${this.state.query}`)
    }

    renderRegisterOrSignout = () => {
        if (!localStorage.getItem('token'))
            return <div>
                <Link to="/login">ورود/ثبت نام</Link>
            </div>
       return <div>
           <Link to="/logout">خروج</Link>
       </div>
    }

    render(){
        return <div id="header">
            <div>
                <Link to="/"><img src={logo} alt="website logo" /></Link>
            </div>
            {this.renderRegisterOrSignout()}
            <div>
                <Link to="/videos/">ویدئوها</Link>
            </div>
            <div className="livescore">
                <Link to="/livescore/">نتایج زنده</Link>
            </div>
            {localStorage.getItem('token')? <div>
                <Link to="/favoriteteam">انتخاب تیم مورد علاقه</Link>
            </div>: null}
            <div>

                <form id="searchbar" onSubmit={this.handleSearch}>
                    <input type="image" src={searchbar} />
                    <input type="text" name="searchbar" onChange={this.handleSearchChange}/>
                </form>
            </div>
        </div>
    }

}
export default withRouter(Header);