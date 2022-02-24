import React, { useState, useEffect } from 'react'
import { Form, Button, Row, Col, Container } from 'react-bootstrap'
import { useHistory } from "react-router-dom";
import { useAlert } from 'react-alert'
import Alerts from '../Alerts'
import '../../css/forms.css'

import Select from 'react-select'
import makeAnimated from 'react-select/animated';

import axiosInstance from '../../axios';





const AddOrder = () => {
    
    const [books, setBooks] = useState([])
    const [deliverers, setDeliverers] = useState()

    const [selectedDeliverer, setSetelectedDeliverer] = useState(null)
    const [selectedBooks, setSetelectedBooks] = useState([])

    const [address, setAddress] = useState({
        street: '',
        number_of_building: '',
        number_of_apartment: '',
        city: '',
        state: '',
        zip_code: '',
    })
    
    const history = useHistory()
    const alert = useAlert()

    const optionsBooks = books && books.map(book =>({label:book.title, value: book.id}))
    /*const optionsDeliverer = deliverers && deliverers.map(deliverer =>({label:deliverer.name, value: deliverer.id})) <--- NIE DZIAŁA*/
    

    useEffect( () => {
        axiosInstance 
            .get('books/')
            .then( (res) => {
                setBooks(res.data)
            })

        axiosInstance
            .get('deliverers/')
            .then( (res) => {
                setDeliverers(res.data)
            })
        
    
    }, [alert, history])


    const postOrder = () => {
        axiosInstance
            .post('orders/', {
                book: selectedBooks,
                deliverer: selectedDeliverer,
                address: {
                    street: address.street,
                    number_of_building: address.number_of_building,
                    number_of_apartment: address.number_of_apartment,
                    city: address.city,
                    state: address.state,
                    zip_code: address.zip_code
                }
            })
            .then((res) => {
                console.log(res)
                alert.success("Utworzono zamówienie!")
                history.push("/orders")
            })
            .catch((err) => {
                //console.log(err.response.data.address)

                const data = err.response.data.address
                const books = err.response.data['Validation_error'] 
                
                
                if(books)
                    alert.error(err.response.data['Validation_error'])

                if(data) {
                    Object.keys(data).forEach(key => {
                        alert.error(data[key][0])
                    })
                }        
            })

    }

    const onChange = (e) => { 
        setAddress({...address, [e.target.name]: e.target.value });
    }


    const handleSelectChangeDeliverer = (e) => {
        try {
            setSetelectedDeliverer(e.value)
        }
        
        catch {
            setSetelectedDeliverer(null)
        }
    }

    const handleSelectChangeBooks = (e) => {
        setSetelectedBooks(Array.isArray(e) ? e.map(x => x.value) : [])
    }


    const onSubmit = (e) => {
        if(selectedBooks.length === 0 || selectedDeliverer === null) {
            alert.error('Opcje wyboru nie mogą być puste!')
        }

        else {
            postOrder()
        }

        e.preventDefault()   
    }

    return (
        <>
            <Alerts/>

            <div className = "background" style={{background:`url(${process.env.PUBLIC_URL + '/images/library_2.jpg'})`, backgroundSize: "cover", width: "100%"}} >
                <Container className = "register">
                    <Row>
                        <Col className="banner">
                            <h1>Dodawanie zamówienia</h1>
                        </Col>
                    </Row>

                    <hr />
                    
                    <Row>
                        <Col>
                            <Form onSubmit={onSubmit}>

                                <Form.Group >
                                    <Form.Floating>
                                        <Select options={optionsBooks} 
                                                isMulti 
                                                placeholder="Wybierz książki"
                                                value={optionsBooks.filter(obj => selectedBooks.includes(obj.value))}
                                                components={makeAnimated()} 
                                                noOptionsMessage={() => 'Brak wyszukiwanej książki'}
                                                onChange={handleSelectChangeBooks}/>
                                    </Form.Floating>
                                </Form.Group>


                                <Form.Group >
                                    <Form.Floating>
                                        <Select options={deliverers && deliverers.map(deliverer =>({label:deliverer.name, value: deliverer.id}))}  
                                                value={deliverers && deliverers.map(deliverer =>({label:deliverer.name, value: deliverer.id})).find(obj => obj.value === selectedDeliverer)}
                                                placeholder="Wybierz dostawce" 
                                                noOptionsMessage={() => 'Brak wyszukiwanego dostawcy'}
                                                isClearable 
                                                onChange={handleSelectChangeDeliverer}/>
                                    </Form.Floating>
                                </Form.Group>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="text"
                                            name="street"
                                            placeholder="Nazwa ulicy"
                                            value={address.street}
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Nazwa ulicy</label>
                                    </Form.Floating>
                                </Form.Group>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="text"
                                            name="number_of_building"
                                            placeholder="Numer budynku"
                                            value={address.number_of_building}
                                            onChange={onChange}
                                            required
                                            
                                        />
                                        <label htmlFor="floatingInputCustom">Numer budynku</label>
                                    </Form.Floating>
                                </Form.Group>
                                
                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="text"
                                            name="number_of_apartment"
                                            placeholder="Numer mieszkania (opcjonalnie)"
                                            value={address.number_of_apartment}
                                            onChange={onChange}
                                        />
                                        <label htmlFor="floatingInputCustom">Numer mieszkania (opcjonalnie)</label>
                                    </Form.Floating>
                                </Form.Group>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="text"
                                            name="city"
                                            placeholder="Nazwa miasta"
                                            value={address.city}
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Nazwa miasta</label>
                                    </Form.Floating>
                                </Form.Group>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="text"
                                            name="state"
                                            placeholder="Województwo"
                                            value={address.state}
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Województwo</label>
                                    </Form.Floating>
                                </Form.Group>

                                <Form.Group>
                                    <Form.Floating> 
                                        <Form.Control
                                            size="lg"
                                            type="text"
                                            name="zip_code"
                                            placeholder="Kod pocztowy"
                                            value={address.zip_code}
                                            onChange={onChange}
                                            required
                                        />
                                        <label htmlFor="floatingInputCustom">Kod pocztowy</label>
                                    </Form.Floating>
                                </Form.Group>

                                <hr />

                                <Container>
                                    <Button
                                        variant="primary"
                                        type="submit"
                                    >
                                        Dodaj
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

export default AddOrder