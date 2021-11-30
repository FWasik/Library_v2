import React from 'react'
import { Row, Col, Container } from 'react-bootstrap'
import '../css/forms.css'


const NotFound = () => {

    return (
        <>
            <div className = "background" style={{height: '57vh', background:`url(${process.env.PUBLIC_URL + '/images/library.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                <Container className = "register">
                    <Row>
                        <Col className="banner">
                            <h1>Nie znaleziono strony!</h1>
                        </Col>
                    </Row>

                </Container>
            </div>
        </>
    )
}

export default NotFound