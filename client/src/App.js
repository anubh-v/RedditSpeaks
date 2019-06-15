import React from "react"
import { Route, BrowserRouter, Switch } from "react-router-dom"
import Home from "./components/Home"
import About from "./components/About"
import Navbar from "./components/Navbar"

function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Navbar />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/about" component={About} />
        </Switch>
      </div>
    </BrowserRouter>
  )
}

export default App
