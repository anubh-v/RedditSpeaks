import React, { Component } from "react"
import WordCloud from "./WordCloud"
class Home extends Component {
  render() {
    return (
      <div>
        <div className="container home">
          <h4 className="center">Home</h4>
          <WordCloud className="wordcloud" />
        </div>
      </div>
    )
  }
}

export default Home
