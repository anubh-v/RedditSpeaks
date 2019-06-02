import React, { Component } from "react"
import WordCloud from "./WordCloud"
import axios from "axios"

const path = "http://localhost:5000/freqdist"
class Home extends Component {
  state = {
    freqDist: []
  }

  componentDidMount = () => {
    console.log("Home component mounted")
    axios.get(path).then(res => {
      console.log(res)
      // this.setState({
      //   freqDist: res.data
      // })
    })
  }

  render() {
    return (
      <div>
        <div className="container home">
          <h2 className="center">Home</h2>
          <WordCloud className="container wordcloud" />
        </div>
      </div>
    )
  }
}

export default Home
