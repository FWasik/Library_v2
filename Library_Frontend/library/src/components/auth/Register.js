import React, {useState} from 'react'
import { Form, Row, Button, Col, Container} from 'react-bootstrap'
import '../../css/forms.css'

import { useAlert } from 'react-alert'
import { useHistory } from "react-router-dom";
import Alerts from "../Alerts"
import axiosInstance from '../../axios';

const Register = () => {

    const alert = useAlert()
    const history = useHistory()


    const [formData, setFormData] = useState({
        username: "",
        first_name: "",
        middle_name: "",
        last_name: "",
        phone_number: "",
        PESEL: "",
        email: "",
        password: "",
        password1: "",
    });
    
    const { username, first_name, middle_name,
        last_name, phone_number, PESEL,
        email, password, password1 } = formData;
    
    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });
    
    const onSubmit = async (e) => {
        e.preventDefault();

        let formDataToSend = new FormData()

        formDataToSend.append('username', formData.username)
        formDataToSend.append('first_name', formData.first_name)
        formDataToSend.append('middle_name', formData.middle_name)
        formDataToSend.append('last_name', formData.last_name)
        formDataToSend.append('phone_number', formData.phone_number)
        formDataToSend.append('PESEL', formData.PESEL)
        formDataToSend.append('email', formData.email)
        formDataToSend.append('password', formData.password)
        formDataToSend.append('password1', formData.password1)



        axiosInstance
            .post("auth/users/", 
                formDataToSend, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then((res) => {
                console.log(res.data);
                history.push('/')
                alert.success('Udało Ci się zarejestrować użytkownika')
            })
            .catch((err) => {
                //console.log(err.response.status)
                //console.log(err.response.data)

                const data = err.response.data

                if(data != null) {
                    Object.keys(data).forEach(key => {
                        const str = data[key][0]
                        console.log(str)
                        if(str.includes("Zły format") || str.includes("Hasła")) {
                            alert.error(str)
                        }

                        else {
                            alert.error('Zarejestrowano użytkownika o takiej nazwie użytkownika, PESEL bądź emailu!')
                        }
                    })
                }   
            })
    };

    return (
        <>
            <Alerts/>

            <div className = "background" style={{background:`url(${process.env.PUBLIC_URL + '/images/library.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                <Container className = "register">
                    <Row>
                        <Col className="banner">
                            <h1>Rejestracja</h1>
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
                                        type="text"
                                        name="username"
                                        placeholder="Twoja nazwa użytkownika"
                                        value={username}
                                        onChange={onChange}
                                        required
                                    />
                                    <label htmlFor="floatingInputCustom">Nazwa użytkownika</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 
                                    <Form.Control
                                        size="lg"
                                        type="text"
                                        name="email"
                                        placeholder="email"
                                        value={email}
                                        onChange={onChange}
                                        required
                                    />
                                    <label htmlFor="floatingInputCustom">Email</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 
                                    <Form.Control
                                        size="lg"
                                        type="text"
                                        name="first_name"
                                        placeholder="Pierwsze imie"
                                        value={first_name}
                                        onChange={onChange}
                                        required
                                    />
                                    <label htmlFor="floatingInputCustom">Pierwsze imie</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 
                                    <Form.Control
                                        size="lg"
                                        type="text"
                                        name="middle_name"
                                        placeholder="Drugie imie"
                                        value={middle_name}
                                        onChange={onChange}
                                    />
                                <label htmlFor="floatingInputCustom">Drugie imie (opcjonalnie)</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 

                                    <Form.Control
                                        size="lg"
                                        type="text"
                                        name="last_name"
                                        placeholder="Twoja nazwa użytkownika"
                                        value={last_name}
                                        onChange={onChange}
                                        required
                                    />
                                    <label htmlFor="floatingInputCustom">Nazwisko</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 

                                    <Form.Control
                                        size="lg"
                                        type="text"
                                        name="phone_number"
                                        placeholder="phone_number"
                                        value={phone_number}
                                        onChange={onChange}
                                        required
                                    />
                                    <label htmlFor="floatingInputCustom">Numer telefonu</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 
                                    <Form.Control
                                        size="lg"
                                        type="text"
                                        name="PESEL"
                                        placeholder="PESEL"
                                        value={PESEL}
                                        onChange={onChange}
                                        required
                                    />
                                    <label htmlFor="floatingInputCustom">PESEL</label>
                                </Form.Floating>
                            </Form.Group>

                            <Form.Group>
                                <Form.Floating> 
                                    <Form.Control
                                        size="lg"
                                        type="password"
                                        name="password"
                                        placeholder="password"
                                        value={password}
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
                                        value={password1}
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
                                    Zarejestruj się
                                </Button>
                            </Container>
                            </Form>
                        </Col>
                    </Row>

                    <hr />
                    
                    <Container>
                        <Button
                            variant="secondary"
                            type="submit"
                            onChange={onChange}
                            onClick={()=> history.push('/login')}
                        >
                            Zaloguj się na konto
                        </Button>
                    </Container>
                </Container>
            </div>
        </>
    )
}

export default Register
