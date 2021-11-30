import React, {useState} from 'react'
import { Form, Row, Button, Col, Container} from 'react-bootstrap'
import '../../css/forms.css'

import { useAlert } from 'react-alert'
import { useHistory } from "react-router-dom";
import Alerts from "../Alerts"
import axiosInstance from '../../axios'


const Login = () => {

    const alert = useAlert()
    const history = useHistory()


    const [formData, setFormData] = useState({
        username: "",
        password: "",
    });
    
    const { username, password } = formData;
    
    const onChange = (e) =>
        setFormData({ ...formData, [e.target.name]: e.target.value });
    
    const onSubmit = async (e) => {
        e.preventDefault();
        
          // console.log(formData);
        const user = {
            username,
            password,
        };

        const body = JSON.stringify(user);
        axiosInstance
            .post("token/", body)
            .then((res) => {
                //console.log(JSON.stringify(res.data))
                localStorage.setItem('access_token', res.data.access)
                localStorage.setItem('refresh_token', res.data.refresh)
                localStorage.setItem('username', user.username)
                axiosInstance.defaults.headers['Authorization'] =
                'JWT ' + localStorage.getItem('access_token')

                //console.log(localStorage.getItem("username"))
                history.push('/')
                alert.success(`Zalogowano jako ${localStorage.getItem('username')}!`) 
            })
            .catch((err) => {
                
                alert.error("Nieprawidłowe dane logowania!")
            }) 
    };

    return (
        <>
            <Alerts/>

            <div className = "background" style={{background:`url(${process.env.PUBLIC_URL + '/images/library.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                <Container className = "login">
                    <Row>
                        <Col className="banner">
                            <h1>Logowanie</h1>
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
                                        placeholder="username"
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

                            <Container>
                                <Button
                                    variant="primary"
                                    type="submit"
                                    onChange={onChange}
                                >
                                    Zaloguj się
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
                            onClick={()=> history.push('/register')}
                        >
                            Zarejestruj się
                        </Button>
                    </Container>
                </Container>
            </div>
        </>
    )
}

export default Login