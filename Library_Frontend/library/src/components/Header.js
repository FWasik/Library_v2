import { Navbar, Nav, Button, NavDropdown, Image} from 'react-bootstrap'
import '../css/header.css'

import Alerts from "./Alerts"

import {useHistory} from 'react-router-dom'

import {useState, useEffect, Fragment} from 'react'
import { useAlert } from 'react-alert'
import axiosInstance from '../axios'

const Header = () => {
    
    const [isAuth, setIsAuth] = useState(false)
    const [username, setUsername] = useState(null)
    const [userImage, setUserImage] = useState(null)
    
    const history = useHistory()
    const alert = useAlert()

    useEffect(() => {
        if(isAuth) { 
            axiosInstance    
                .get(`auth/users/${localStorage.getItem('username')}/`)
                .then((res) => {
                    setUserImage(res.data.image)
                })
                .catch((err) => {
                    console.log(err.message)        
                })
        }

        setInterval(() => {
            if (localStorage.getItem('access_token') !== null) {
                setIsAuth(true)
                setUsername(localStorage.getItem('username'))
                

                const token = localStorage.getItem('access_token')
                var jwtPayload = JSON.parse(window.atob(token.split('.')[1]))
                const expiration = new Date(jwtPayload.exp * 1000);
                const now = new Date();
                //const fiveMinutes = 1000 * 60 * 1;
    
                //console.log(expiration)
                //console.log(now)
                //console.log(expiration.getTime())
                //console.log(now.getTime())
                //console.log(expiration.getTime() - now.getTime())
                
                if(expiration.getTime() - now.getTime() <= 0) {
                    localStorage.clear()  
                    alert.error('Sesja wygasła! Zaloguj się ponownie!')
                    history.push('/')
                } 
            
            }

            else if(localStorage.getItem('access_token') === null) {
                setIsAuth(false)
            }

        }, [])

    }, [alert, history, isAuth])

    return (
        <>
            <Alerts/>

            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark" py="5" sticky="top">
                <svg className="bi bi-book" width="48px" height="50px" viewBox="0 0 16 16" fill="white" xmlns="http://www.w3.org/2000/svg">
                    <path fillRule="evenodd" d="M3.214 1.072C4.813.752 6.916.71 8.354 2.146A.5.5 0 0 1 8.5 2.5v11a.5.5 0 0 1-.854.354c-.843-.844-2.115-1.059-3.47-.92-1.344.14-2.66.617-3.452 1.013A.5.5 0 0 1 0 13.5v-11a.5.5 0 0 1 .276-.447L.5 2.5l-.224-.447.002-.001.004-.002.013-.006a5.017 5.017 0 0 1 .22-.103 12.958 12.958 0 0 1 2.7-.869zM1 2.82v9.908c.846-.343 1.944-.672 3.074-.788 1.143-.118 2.387-.023 3.426.56V2.718c-1.063-.929-2.631-.956-4.09-.664A11.958 11.958 0 0 0 1 2.82z"/>
                    <path fillRule="evenodd" d="M12.786 1.072C11.188.752 9.084.71 7.646 2.146A.5.5 0 0 0 7.5 2.5v11a.5.5 0 0 0 .854.354c.843-.844 2.115-1.059 3.47-.92 1.344.14 2.66.617 3.452 1.013A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.276-.447L15.5 2.5l.224-.447-.002-.001-.004-.002-.013-.006-.047-.023a12.582 12.582 0 0 0-.799-.34 12.96 12.96 0 0 0-2.073-.609zM15 2.82v9.908c-.846-.343-1.944-.672-3.074-.788-1.143-.118-2.387-.023-3.426.56V2.718c1.063-.929 2.631-.956 4.09-.664A11.956 11.956 0 0 1 15 2.82z"/>
                </svg>
                <Navbar.Brand href="/">Wirtualna biblioteka</Navbar.Brand>
                <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                <Navbar.Collapse id="responsive-navbar-nav">
                <Nav className="me-auto">
                    
                </Nav>
                <Nav>
                    <Nav.Link href='/about'>Książki</Nav.Link>

                    {isAuth === true ? (
                        <Fragment>
                            <NavDropdown title="Zamówienia" id="collasible-nav-dropdown">
                                <NavDropdown.Item href={'/orders'}>Lista zamówień</NavDropdown.Item>
                                <NavDropdown.Item href={'/orders/add'} bg="dark" variant="dark">Dodaj</NavDropdown.Item>
                            </NavDropdown>
                            <Nav.Link href={`/${username}`}>
                                { userImage !== null ? (
                                     <Image src={ userImage } roundedCircle /> )
                                 : (<> </>)} 
                                {username}
                            </Nav.Link>
                            <Button variant="light" href="/logout">Wyloguj</Button>
                        </Fragment>
                        ) : (

                        <Fragment>
                            {/*

                            <NavDropdown.Item href="#action/3.3" bg="dark" variant="dark">Something</NavDropdown.Item>
                                <NavDropdown.Divider />
                                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item> 
                            
                            <Nav.Link href="/register">Rejestracja</Nav.Link>
                            <Nav.Link href="/login">Logowanie</Nav.Link>*/}

                            <Button variant="light" href='/login'>Logowanie</Button>
                            <Button variant="light" href='/register'>Rejestracja</Button>
                        </Fragment>
                    )}
                    { /*<NavDropdown title="Dropdown" id="collasible-nav-dropdown">
                    <NavDropdown.Item href="#action/3.1" bg="dark" variant="dark">Action</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.2" bg="dark" variant="dark">Another action</NavDropdown.Item>
                    <NavDropdown.Item href="#action/3.3" bg="dark" variant="dark">Something</NavDropdown.Item>
                    <NavDropdown.Divider />
                    <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item> 
                    </NavDropdown> */}
                </Nav>
                </Navbar.Collapse>
                
            </Navbar>
        </>
    )
} 

export default Header