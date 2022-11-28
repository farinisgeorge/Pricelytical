import React, {useEffect, useState} from 'react';
import axios from 'axios'
import './App.css';
import About from './views/About'
import Home from './views/Home'
import Login from './views/Login'
import Profile from './views/Profile'
import NavBar from './components/NavBar'
import MyFooter from './components/MyFooter'
import SignUp from './views/SignUp'
import Pricing from './views/Pricing'
import Analysis_list from './views/Analysis_list'
import Contact from './views/Contact'
import Analysis from './views/Analysis'
import Create from './views/Create_analysis'
import {SERVER_ADDRESS} from "./constants/config"
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom"



function App() {
  const [logedin, setLogedin] = useState(true)
  const [user, setUser] = useState({
                                    id: "",
                                    username : "",
                                    email: "",
                                    first_name: "",
                                    last_name: "",
                                  })

  const LogSet = (bool) => {
    setLogedin(bool)
  }


  useEffect(()=>{
    const postdata = {
      refresh : localStorage.getItem('refresh_token')
    }
    const options = {
      headers:{
              Accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }    
    } 
    
    axios.post(SERVER_ADDRESS + 'accounts/refresh/', postdata, options).then(response => {
            localStorage.setItem('access_token', response.data.access);
            console.log("New Token: ",response.data.access);
          }).catch((error) =>{
            localStorage.removeItem('access_token');
            console.log("Could not update token");
                
          });
  },[])

  useEffect(  () =>  {
    const options = {
      headers:{
              Accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }    
    } 
    
    axios.get(SERVER_ADDRESS + 'accounts/current-user/', options).then(response => {
          setUser({
            id: response.data.id,
            username : response.data.username,
            first_name: response.data.first_name,
            last_name: response.data.last_name,
            email: response.data.email,
          })
          localStorage.setItem('user', response.data.username)
          setLogedin(true)
          console.log("done",response.data,user);
          }).catch((error) =>{
            setLogedin(false)
            
            console.log("Have an error");
                
              });
    
    
},[logedin])



  return (
    
      <div className='relative'>
      <Router>
      <NavBar setloged={LogSet} logedin={logedin} user={user.username}/>
        <Switch>
          <Route exact path="/"><Home /></Route>
          <Route path="/about" ><About /></Route>
          <Route path="/pricing" ><Pricing /></Route>
          <Route path="/contact"><Contact/></Route>
          <Route path="/login"><Login setloged={LogSet}/></Route>
          <Route path="/signup"><SignUp/></Route>
          <Route path="/analysis/list" render={() => logedin ? (<Analysis_list/>) : (<Redirect to='/login'/>)}/>
          <Route path="/analysis/create" render={() => logedin ? (<Create/>) : (<Redirect to='/login'/>)}/>
          <Route path="/profile" render={() => logedin ? (<Profile user={user} />) : (<Redirect to='/login'/>)}/>
          {/* <Route path="/analysis/create" render={() => logedin ? (<Create/>) : (<Create/>)}/> */}
          <Route path="/analysis/report/:id"> <Analysis/></Route>
          
          
          
        </Switch>
        <div className="relative-bottom">
          <div className='shadow'>
            <MyFooter/>
          </div>
        </div>
      
      </Router>
      
      </div>
 
  );
}

export default App;
