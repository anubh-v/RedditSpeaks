import React, { Component } from "react"
import WordCloud from "./WordCloud"
class Home extends Component {
  state = {
    freqDist: []
  }

  componentDidMount = () => {
    console.log("Home component mounted")
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
