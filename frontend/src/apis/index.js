/**
 * Created by Arman Samiei on 2/28/2021.
 */
import axios from 'axios'
export const backendUrl = 'http://localhost:8000';

export default axios.create({
    baseURL: `http://localhost:8000/`,

});