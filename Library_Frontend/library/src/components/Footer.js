import React from 'react'
import {NavDropdown} from 'react-bootstrap'
import '../css/footer.css'


const Footer = () => {
    return (
        <footer className="bg-dark">
            <div className="container-fluid padding">
                <div className="row text-center">
                    <div className="col-md-4">
                        <NavDropdown.Divider />
                        <h5>Kontakt</h5>
                        <NavDropdown.Divider />

                        <p>123-456-789</p>
                        <p>email@email.com</p>
                        <p>ul.Koralowa 2137</p>
                        <p>Lublin, Polska</p>
                    </div>

                    <div className="col-md-4">
                        <NavDropdown.Divider />
                        <h5>Godziny otwarcia</h5>
                        <NavDropdown.Divider />

                        <p>Pon-Pt: 7:00-15:00</p>
                        <p>Sb: 7:00-12:00</p>
                        <p>Nd: Nieczynne</p>
                    </div>
                    
                    <div className="col-md-4">
                        <NavDropdown.Divider />
                        <h5>Social media</h5>
                        <NavDropdown.Divider />

                        <div className="container">
                            <a href="https://www.facebook.com/"> <i className="fa fa-facebook"></i></a>
                            <a href="https://twitter.com/explore"> <i className="fa fa-twitter"></i></a>
                        </div>
                        
                        <div className="container">
                            <a href="https://www.youtube.com/"> <i className="fa fa-youtube"></i></a>
                            <a href="https://www.instagram.com/"> <i className="fa fa-instagram"></i></a>
                        </div>
                    </div>
                </div>

                <div className="col-12 text-center">
                    <NavDropdown.Divider />
                    <h5>&copy; FW 2021</h5>
                    <NavDropdown.Divider />
                </div>
            </div>
        </footer>
    )
}

export default Footer
