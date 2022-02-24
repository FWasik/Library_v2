import axios from 'axios'


var baseURL

if(process.env.NODE_ENV === 'development')
	baseURL = 'http://127.0.0.1:8000/api/'

else
	baseURL = 'https://django-react-library.herokuapp.com/api/'

	
const axiosInstance = axios.create({
	baseURL: baseURL,
	headers: {
		Authorization: localStorage.getItem('access_token')
			? 'JWT ' + localStorage.getItem('access_token')
			: null,
		'Content-Type': 'application/json',
		accept: 'application/json',
	}, 
});


export default axiosInstance