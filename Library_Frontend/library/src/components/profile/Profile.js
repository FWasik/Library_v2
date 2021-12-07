import React, {useState, useEffect} from 'react'
import { Form, Row, Button, Col, Container, Spinner, Image} from 'react-bootstrap'
import '../../css/profile.css'


import { useHistory } from "react-router-dom";
import { useAlert } from 'react-alert'
import Alerts from "../Alerts"
import axiosInstance from '../../axios';



const Profile = () => {

    const alert = useAlert()
    const history = useHistory()

    const [userInfo, setUserInfo] = useState([])
    const [loading, setLoading] = useState(false)
    const [image, setImage] = useState(null)

    const [formData, updateFormData] = useState({
        username: '',
        first_name: '',
        middle_name: '',
        last_name: '',
        phone_number: '',
        PESEL: '',
        email: '',
    });
    
    useEffect(() => {
        setLoading(true)
        axiosInstance
        .get(`auth/users/${localStorage.getItem('username')}/`)
        .then((res) => {
            updateFormData(res.data);
            setTimeout( () => {
                setLoading(false)
            }, 2500)
        })
        .catch((err) => {
            console.log(err.message)
        })

        axiosInstance    
            .get(`auth/users/${localStorage.getItem('username')}/`)
            .then((res) => {
                console.log(res.data)
                setUserInfo(res.data)
                setTimeout( () => {
                    setLoading(false)
                }, 2500)
            })
            .catch((err) => {
                console.log(err.message)        
            })
    }, [updateFormData, alert, history]);


    const handleImage = (e) => {
        e.preventDefault();
        setImage(e.target.files[0])
      }
        
    const onChange = (e) =>
        updateFormData({...formData, [e.target.name]: e.target.value });



    const onSubmit = (e) => {
        e.preventDefault();

        let formDataToSend = new FormData()
        
        if(image) {
            formDataToSend.append('image', image)
        }

        formDataToSend.append('username', formData.username)
        formDataToSend.append('first_name', formData.first_name)
        formDataToSend.append('middle_name', formData.middle_name)
        formDataToSend.append('last_name', formData.last_name)
        formDataToSend.append('phone_number', formData.phone_number)
        formDataToSend.append('PESEL', formData.PESEL)
        formDataToSend.append('email', formData.email)
        
        axiosInstance
            .patch(`auth/users/${localStorage.getItem('username')}/`, 
                formDataToSend, { 
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            .then((res) => {
                console.log(res.data);

                if(localStorage.getItem('username') !== res.data.username)
                    localStorage.setItem('username', res.data.username)
                
                alert.success(`Zaktualizowano informacje o użytkowniku ${localStorage.getItem('username')}!`)
                setTimeout( () => {    
                    history.go(`/${localStorage.getItem('username')}`)
                }, 1500)
            })
            .catch((err) => {
                console.log(err.response.status)
                console.log(err.response.data)

                const data = err.response.data
                
                if(data != null) {
                    Object.keys(data).forEach(key => {
                        const str = data[key][0]
                        console.log(str)
                        if(str.includes("Zły format")) {
                            alert.error(str)
                        }

                        else if(str.includes("This field")) {
                            alert.error('Pole nie może być puste!')
                        }

                        else {
                            alert.error('Zarejestrowano użytkownika o takiej nazwie użytkownika, PESEL, nr.telefonu bądź emailu!')
                        }
                    })
                }
            })
            
    };

    return (
        <>
            <Alerts/>

            <div className = "background" style={{background:`url(${process.env.PUBLIC_URL + '/images/library_2.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                <Container className = "profile">
                    
                    {
                        loading === true ? 
                            <Container>
                                <Spinner animation="border"/> 
                            </Container>
                        :
                        
                        <>  
                            
                            <Container className='profile-info'>
                                <Container>
                                    <Image
                                        src={userInfo.image} 
                                        roundedCircle
                                    />
                                    <h1>{userInfo.username}</h1>
                                
                                </Container>
                                
                                <hr />

                                <Container>
                                    <Row>
                                        <Col sm={5}>
                                            Imie: 
                                        </Col>

                                        <Col sm={7}>
                                            {userInfo.first_name} 
                                        </Col>
                                    </Row>

                                    <Row>
                                        <Col sm={5}>
                                            Drugie imie: 
                                        </Col>

                                        <Col sm={7}>
                                            {userInfo.middle_name} 
                                        </Col>
                                    </Row>

                                    <Row>
                                        <Col sm={5}>
                                            Nazwisko:
                                        </Col>

                                        <Col sm={7}>
                                            {userInfo.last_name} 
                                        </Col>
                                    </Row>

                                    <Row>
                                        <Col sm={5}>
                                            Email: 
                                        </Col>

                                        <Col sm={7}>
                                            {userInfo.email} 
                                        </Col>
                                    </Row>

                                    <Row>
                                        <Col sm={5}>
                                            Numer tel.:
                                        </Col>

                                        <Col sm={7}>
                                            {userInfo.phone_number}
                                        </Col>
                                    </Row>                        

                                    <Row>
                                        <Col sm={5}>
                                            PESEL: 
                                        </Col>

                                        <Col sm={7}>
                                            {userInfo.PESEL}
                                        </Col>
                                    </Row>

                                </Container>
                            
                            </Container>
                        
                            <Container className='profile-update'>
                                <Row>
                                    <Col>
                                        <h1>Aktualizacja</h1>
                                    </Col>
                                </Row>
                                <Col>
                                    <Form onSubmit={onSubmit}>

                                    <Form.Group>
                                        <Form.Floating> 
                                            <Form.Control
                                                size="lg"
                                                type="text"
                                                name="username"
                                                placeholder="Twoja nazwa użytkownika"
                                                value={formData.username }
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
                                                value={formData.email}
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
                                                value={formData.first_name}
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
                                                value={formData.middle_name}
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
                                                value={formData.last_name}
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
                                                value={formData.phone_number}
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
                                                value={formData.PESEL}
                                                onChange={onChange}
                                                required
                                            />
                                            <label htmlFor="floatingInputCustom">PESEL</label>
                                        </Form.Floating>
                                    </Form.Group>  

                                    <Form.Group>
                                        <Form.Floating> 
                                            <input
                                                accept="image/png, image/jpeg"
                                                type="file"
                                                name="image"
                                                placeholder="Image"
                                                onChange={handleImage}
                                                
                                            />
                                        </Form.Floating>
                                    </Form.Group>    

                                        
                                    <Container>
                                        <Button
                                            variant="primary"
                                            type="submit"
                                            onChange={onChange}
                                        >
                                            Aktualizuj
                                        </Button>

                                        <Button
                                            variant="secondary"
                                            type="submit"
                                            onClick={()=> history.push(`/${localStorage.getItem('username')}/password-update`)}
                                        >
                                            Zmiana hasła
                                        </Button>
                                    </Container>
                                    </Form>
                                </Col>
                            </Container>

                        </> 
                    }
                </Container>
            </div>
        </>
    )
}

export default Profile