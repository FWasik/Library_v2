import { Route, Redirect } from 'react-router-dom';


function ProtectedRoute({ component: Component, ...rest }) {
    return (
        <Route
        {...rest}

        render={ props => 
                localStorage.getItem('access_token') === null ? (
                    <Component {...props} />
                ) : (
                    <Redirect
                        to={{
                        pathname: '/',
                        state: { from: props.location }
                        }}
                    />
                )
        }
        />
    );
}

export default ProtectedRoute;