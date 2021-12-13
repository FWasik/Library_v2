import Header from './components/Header'
import Footer from './components/Footer'
import Register from './components/auth/Register'
import ScrollToTop from './components/ScrollToTop'
import Login from './components/auth/Login'
import Logout from './components/auth/Logout'
import Home from './components/Home'
import PrivateRoute from './components/routers/PrivateRoute'
import ProtectedRoute from './components/routers/ProtectedRoute'
import NotFound from './components/NotFound'
import Profile from './components/profile/Profile'
import Orders from './components/orders/Orders'
import AddOrder from './components/orders/AddOrder'
import Books from './components/Books'
import PasswordUpdate from './components/profile/PasswordUpdate'

import './App.css';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'

import AlertTemplate from 'react-alert-template-basic'
import {transitions, positions, Provider as AlertProvider} from 'react-alert'





const options = {
    timeout: 6000,
    position: positions.TOP_CENTER,
    offset: "12rem",
    transition: transitions.SCALE
}




function App() {
    
  return (
    <Router>
      <AlertProvider template={AlertTemplate} {...options}>
        <Header/>
          
          <ScrollToTop/>
          
          <Switch>
            <Route exact path='/' component={Home}/>

            <Route exact path='/books' component={Books}/>

            <ProtectedRoute exact path='/register' component={Register}/>
              

            <ProtectedRoute exact path='/login' component={Login}/>
              

            <PrivateRoute exact path='/logout' component={Logout}/>

            <PrivateRoute exact path='/orders' component={Orders}/>

            <PrivateRoute exact path='/orders/add' component={AddOrder}/>

            <PrivateRoute exact path='/:username' component={({match}) => {
                if(match.params.username === localStorage.getItem('username')) {
                  return <Profile match={match} />
                } else {
                  return <NotFound/>
                }
              }} />

            <PrivateRoute exact path='/:username/password-update' component={({match}) => {
                if(match.params.username === localStorage.getItem('username')) {
                  return <PasswordUpdate match={match} />
                } else {
                  return <NotFound/>
                }
              }} />


            <PrivateRoute exact path="*" component={NotFound}/>  
              
          </Switch>

          {/*<Route exact path="*" component={NotFound}/>*/}
              
        <Footer/>
      </AlertProvider>
    </Router>
    
  );
}

export default App;
