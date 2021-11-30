import React from 'react'
import { Container } from 'react-bootstrap'
import '../css/home.css'


const Home = () => {


    return (
        <>
            <Container className="video">
                <video src="/videos/Hogwarts Library Ambience - Sam Gielen_Trim.mp4" autoPlay loop muted/>

                <h1>Witaj w Wirtualnej bibliotece!</h1>
                <p>Rozgość się :)</p>
            </Container>
        </>
    )
}

export default Home
