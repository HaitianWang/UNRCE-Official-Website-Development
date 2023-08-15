import react from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import "./styles/aaa.css";
import Home from './pages/Home';
import Login from './pages/Login'
import Signup from './pages/Signup'


export interface AppProps{}
const App: React.FunctionComponent<AppProps> = (props) => {
  return (<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />}/>
    <Route path="login" element={<Login />}/>
    <Route path="signup" element={<Signup />}/>
    </Routes>
    </BrowserRouter>
    );
};

export default App;
