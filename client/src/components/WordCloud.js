import React, { Component } from "react"
import D3WordCloud from "react-d3-cloud"
class WordCloud extends Component {
  state = {
    freqDist: [
      { text: "Hey", value: 1000 },
      { text: "lol", value: 200 },
      { text: "first impression", value: 800 },
      { text: "very cool", value: 1000000 },
      { text: "duck", value: 10 }
    ] // array of objects
  }

  render = () => {
    const fontSizeMapper = word => Math.log2(word.value) * 5
    const rotate = word => word.value % 360
    return this.props.freqDist.length === 0 ? (
      <div id="myChart" className="container">
        <h5 className="wordcloud-title center"> Waiting for backend... </h5>
      </div>
    ) : (
      <div id="myChart" className="container">
        <h5 className="wordcloud-title center"> Generated WordCloud </h5>
        <D3WordCloud
          data={this.props.freqDist}
          fontSizeMapper={fontSizeMapper}
          rotate={rotate}
        />
      </div>
    )
  }
}

export default WordCloud
