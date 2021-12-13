import React, {useEffect, useState, useRef} from 'react'
import {Table, Button, Container, Spinner} from 'react-bootstrap'
import Alerts from '../Alerts'
import { useAlert } from 'react-alert'
import { useHistory } from "react-router-dom";
import '../../css/orders.css'

import axiosInstance from '../../axios'

import { confirmAlert } from 'react-confirm-alert'
import 'react-confirm-alert/src/react-confirm-alert.css'


const Orders = () => {
    
    const [orders, setOrders] = useState([])

    var orderToDelete = useRef(null)
    const [loading, setLoading] = useState(false)
    const alert = useAlert()
    const history = useHistory()


    const options = { 
        customUI: ({ onClose }) => {
            return (
                <div id="react-confirm-alert">
                    <div className="react-confirm-alert-overlay overlay-custom-class-name">
                        <div className="react-confirm-alert">
                            <div className="react-confirm-alert-body" style={{textAlign: "center"}}>
                                <h1>Potwierdzenie</h1>
                                    <h5>Na pewno chcesz usunąć zamówienie?</h5>
                                <div className="react-confirm-alert-button-group" style={{justifyContent:"center"}}>
                                    <Button onClick={onClose} id='confirm_no'>
                                        Anuluj
                                    </Button>

                                    <Button variant="danger" id='confirm_yes' onClick={ () => { 
                                                                                deleteOrder( orderToDelete.id)
                                                                                
                                                                                onClose()
                                                                                }
                                                                                
                                                                            }
                                                                        
                                        >Tak</Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        }
    }

    const onClick = (order) => {
        orderToDelete = order

        console.log(orderToDelete)
        
        confirmAlert(options)
    }



    useEffect( () => {
        setLoading(true)
        axiosInstance
            .get("orders/")
            .then((res) => {
                //console.log(res.data)
                setOrders(res.data)

                setTimeout( () => {
                    setLoading(false)
                }, 2000)
                
            })
            .catch((err) => {
                console.log(err.message)
                console.log(err)
            }) 
    }, [alert, history, orderToDelete])
    

    const deleteOrder = (id) => {
        axiosInstance
            .delete(`/orders/${id}/`)
            .then( () => {
                const ordersRes = orders.filter((order) => order.id !== id)
                setOrders(ordersRes)
                alert.success(`Usunięto zamówienie o ID ${id}!`)
            })
            .catch((err) => {
                const error = err.response.data
                console.log(error)
                if (error === "Błąd! Za późno na anulowanie zamówienia! Skontaktuj się z adminem!")
                    alert.error(error)
            })
    }


    return (    
        <>  
        
            <Alerts/>
            
            <div className="backgroundOrders" style={{background:`url(${process.env.PUBLIC_URL + '/images/library_2.jpg'})`, backgroundSize: "cover", width: "100%"}}>
                <div className="card card-body">
                
                        {
                            loading === true ?
                                <Container>    
                                    <Spinner animation="border" /> 
                                </Container>
                            :
                            
                            <>
                                <h1>Lista zamówień</h1>
                                
                                {
                                    orders.length === 0 ?
                                        <h2>Brak zamówień</h2>
                                    
                                    :
                                        <Table striped bordered hover responsive variant="dark">
                                        <thead>
                                            <tr>
                                                <th scope="col" style={{width: "2%"}}>ID: </th>
                                                <th id='separator' scope="col"style={{width: "17%"}}>Ksiązka/i</th>
                                                <th id='separator' scope="col"style={{width: "17%"}}>Autor/zy</th>
                                                
                                                <th scope="col"style={{width: "15%"}}>Data utworzenia wyp.: </th>
                                                <th scope="col"style={{width: "11%"}}>Data dostarczenia: </th>
                                                <th scope="col"style={{width: "11%"}}>Data końca wyp.:</th>
                                                <th scope="col"style={{width: "8%"}}>Dostawca: </th>
                                                <th scope="col"style={{width: "20%"}}>Adres:</th>
                                                <th scope="col"style={{width: "8%"}}>Akcja</th>
                                            </tr>
                                        </thead>
                        
                                        <tbody>
                                            { 
                                                orders.map(order => (
                                                <tr key={order.id}>
                                                    <td> {order.id} </td>
                                                    
                                                    <td>
                                                        {
                                                            order.book.map(book => (
                                                                        <tr >
                                                                            
                                                                                {book.title} 
                                                                                <br/>
                                                                                <br/>
                                                                                <br/>
                                                                        </tr>
                                                                    
                                                            ))    
                                                        } 
                                                    </td>

                                                    <td>
                                                        {
                                                            order.book.map(book => (
                                                                        <tr>
                                                                            {
                                                                                book.author.map(author => (
                                                                                    <tr>
                                                                                        <td> {author.first_name} { author.middle_name} {author.last_name} </td>
                                                                                        <br/>
                                                                                        <br/>
                                                                                        <br/>
                                                                                    </tr>
                                                                                ))
                                                                            }
                                                                        </tr>
                                                                    
                                                            ))    
                                                        } 
                                                    </td>

                                                    

                                                    <td> {order.date_order_create} </td>
                                                    <td> {order.date_delivery} </td>
                                                    <td> {order.rental_end} </td>
                                                    <td> {order.deliverer.name} </td>
                                                    <td> {order.address.street} {order.address.number_of_building} 

                                                        { 
                                                            order.address.number_of_apartment ? 
                                                            
                                                                <> / </>
                                                            
                                                            :

                                                            <></>
                                                        }
                                                        
                                                        {order.address.number_of_apartment} <br/> <br/> 
                                                        {order.address.zip_code} {" "} {order.address.city} <br/> <br/> 
                                                        {order.address.state}   </td>
                                                    
                                                    
                                                    <td id="button"> 
                                                        <Button variant="danger" onClick={ () => onClick(order)}>
                                                            Usuń 
                                                        </Button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </Table>
                                }
                            </>
                        }
            
                </div>
            </div>
        </>   
    )
    
}

export default Orders