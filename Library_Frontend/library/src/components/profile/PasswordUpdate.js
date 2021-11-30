import React, {useState} from 'react'
import { Form, Row, Button, Col, Container} from 'react-bootstrap'
import '../../css/forms.css'

import { useAlert } from 'react-alert'
import { useHistory } from "react-router-dom";
import Alerts from "../Alerts"
import axiosInstance from '../../axios';


const PasswordUpdate = () => {
    
    const alert = useAlert()
    const history = useHistory()

    const [formData, updateFormData] = useState({
        password: '',
        password1: '',
        old_password: ''
    });


    const onChange = (e) =>
        updateFormData({...formData, [e.target.name]: e.target.value });


    const onSubmit = (e) => {
        e.preventDefault();

        let formDataToSend = new FormData()
        

        formDataToSend.append('password', formData.password)
        formDataToSend.append('password1', formData.password1)
        formDataToSend.append('old_password', formData.old_password)
        
        
        axiosInstance
            .patch(`auth/users/${localStorage.getItem('username')}/`, 
                formDataToSend, { 
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then((res) => {
            
                alert.success(`Zmieniono hasło!`)
                setTimeout( () => {    
                    history.push(`/${localStorage.getItem('username')}`)
                }, 1500)
            })
            .catch((err) => {
                console.log(err.response.status)
                console.log(err.response.data)

                const data = err.response.data
                
                if(data != null) {
                    Object.keys(data).forEach(key => {
                        console.log(data[key])
                        alert.error(data[key])
                    })
                }
            })
            
    };


    return (
        <>
            <Alerts/>

            <div className = "background" style={{background:`url(${process.env.PUBLIC_URL + '/images/library_2.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                <Container className = "register">
                    <Row>
                        <Col className="banner">
                            <h1>Zmiana hasła</h1>
                        </Col>
                    </Row>

                    <hr />
                    
                    <Row>
                        <Col>
                            <Form onSubmit={onSubmit}>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="password"
                                            name="old_password"
                                            placeholder="old_password"
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Poprzednie hasło</label>
                                    </Form.Floating>
                                </Form.Group>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="password"
                                            name="password"
                                            placeholder="password"
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Hasło</label>
                                    </Form.Floating>
                                </Form.Group>
                    
                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="password"
                                            name="password1"
                                            placeholder="password1"
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Powtórz hasło</label>
                                    </Form.Floating>
                                </Form.Group>
                                
                                <Container className='container-pass'> 
                                    <h5>Hasło musi zawierać:</h5>
                                    <ul>
                                        <li>Od 8 do 30 znaków</li>
                                        <li>Minimum 1 znak specjalny ( #$@!%&*? )</li>
                                        <li>Minimum 1 liczbę</li>
                                        <li>Minimum 1 małą literę</li>
                                        <li>Minimum 1 dużą literę</li>
                                    </ul>
                                </Container>
                                
                                <Container>
                                    <Button
                                        variant="primary"
                                        type="submit"
                                        onChange={onChange}
                                    >
                                        Zmień hasło
                                    </Button>
                                </Container>
                            </Form>
                        </Col>
                    </Row>
                </Container>
            </div>
        </>
    )
}

export default PasswordUpdate
