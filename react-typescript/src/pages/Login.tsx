import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

export interface LoginProps {}
const Login: React.FunctionComponent<LoginProps> = (props) => {
  return (
    <div className="centered-box">
      <div className="login-box">
        <img src="/RCEWA_Logo.png" alt="Logo" className="logo-image" />
        <h3 className="login-heading">Log In</h3>
        <form className="login-form" method="post">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input type="text" name="username" className={`input-field autofill-styles`} />
          </div>
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input type="password" name="password" />
          </div>
          <p className="Login-link">
            No account yet? Sign up <a href="/Login" style={{ color: 'white' }}>HERE</a>
          </p>
          <input type="submit" value="Submit" className="submit-button" />
        </form>
      </div>
    </div>
  );
};

export default Login;
