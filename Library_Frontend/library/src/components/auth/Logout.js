import React, {useEffect} from 'react'


import { useAlert } from 'react-alert'

import { useHistory } from 'react-router';

const Logout = () => {

    const alert = useAlert()
    const history = useHistory()

    useEffect(() => {
        try {
            localStorage.clear()
            alert.success('Wylogowano poprawnie!')
            history.push('/')
            
        } 
    
        catch (err) {
            console.error(err)
        }

    }, [alert, history]);

    return (
        <>
        </>
    )
}

export default Logout