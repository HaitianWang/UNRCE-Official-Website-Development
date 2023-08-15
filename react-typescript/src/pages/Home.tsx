import react from 'react';
import { BrowserRouter, Routes } from 'react-router-dom';

export interface HomeProps{}
const Home: React.FunctionComponent<HomeProps> = (props) => {
  return <div><p>This is the home page</p></div> 
};

export default Home;