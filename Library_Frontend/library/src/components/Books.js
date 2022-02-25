import React from 'react'
import '../css/books.css'
import { Container, Carousel, Spinner, Image, Row, Col } from 'react-bootstrap'

import Alerts from "./Alerts"
import {useState, useEffect} from 'react'
import axiosInstance from '../axios'
import '../css/forms.css'

const Books = () => {

    const [books, setBooks] = useState([])
    const [loading, setLoading] = useState(false)


    useEffect(() => {
        setLoading(true)
        axiosInstance   
            .get('books/')
            .then((res) => {
                setBooks(res.data)
                
                setTimeout( () => {
                    setLoading(false)
                }, 2500)
            })
            .catch((err) => {
                console.log(err.message)        
            })

    }, [])

    return (
        <>
            <Alerts/>

            <div style={{background:`url(${process.env.PUBLIC_URL + '/images/library.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                

                <div className='caroBack'>
                
                    {
                        loading === true ? 
                            <Container className="spinner-container">
                                <Spinner animation="border"/> 
                            </Container>

                        :

                        <>
                            <h1> Dostępne książki: </h1>
                            
                            <Container className="carousel">
                                
                                    <Carousel interval="500000">

                                    { books && books.map(book => ( 
                                            <Carousel.Item >
                                                <Image
                                                    src={book.image} 
                                                />
                                                <Carousel.Caption>
                                                    
                                                    <Container>
                                                        <Row>
                                                            <Col sm={5}>
                                                                <h3>Tytuł:</h3>
                                                            </Col>

                                                            <Col sm={7}>
                                                                <h3>{book.title}</h3>
                                                            </Col>
                                                        </Row>

                                                        <Row>
                                                            <Col sm={5}>
                                                                Autor/zy: 
                                                            </Col>

                                                            <Col sm={7}>
                                                                { book.author.map( author => ( 
                                                                    <>
                                                                        {author.first_name} { author.middle_name} {author.last_name} <br/>
                                                                    </>
                                                                ))} 
                                                            </Col>
                                                        </Row>

                                                        <Row>
                                                            <Col sm={5}>
                                                                Wydawnictwo: 
                                                            </Col>

                                                            <Col sm={7}>
                                                                {book.publisher.name}
                                                            </Col>
                                                        </Row>

                                                        <Row>
                                                            <Col sm={5}>
                                                                Gatunek/ki:
                                                            </Col>

                                                            <Col sm={7}>
                                                                { book.genre.map( genre => ( 
                                                                    <>
                                                                        {genre.name} <br/>
                                                                    </>
                                                                ))}
                                                            </Col>
                                                        </Row>

                                                        <Row>
                                                            <Col sm={5}>
                                                                Liczba strony:
                                                            </Col>

                                                            <Col sm={7}>
                                                                {book.number_of_pages}
                                                            </Col>
                                                        </Row>                        

                                                        <Row>
                                                            <Col sm={5}>
                                                                Data wydania: 
                                                            </Col>

                                                            <Col sm={7}>
                                                                {book.year_of_release}
                                                            </Col>
                                                        </Row>

                                                        <Row>
                                                            <Col sm={5}>
                                                                Dostępnych sztuk:
                                                            </Col>

                                                            <Col sm={7}>
                                                                {book.amount}
                                                            </Col>
                                                        </Row>   
                                                    </Container>
                                                    <Container>
                                                        <p>{book.summary}</p>
                                                    </Container>
                                                </Carousel.Caption>
                                            </Carousel.Item>     
                                        ) )

                                    }  
                                    </Carousel>                       
                            </Container>
                        </> 
                    } 
                </div>
            </div>
        </>
    )
}

export default Books
