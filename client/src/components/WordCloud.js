import React, { Component } from "react"

class WordCloud extends Component {
  state = {
    freqDist: [] // array of objects
  }

  render = () => {
    return <div id="myChart" className="container wordcloud" />
  }
}

export default WordCloud
