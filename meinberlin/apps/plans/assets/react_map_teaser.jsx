var MapTeaserBox = require('./MapTeaserBox')
var React = require('react')
var ReactDOM = require('react-dom')

module.exports.renderFilter = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<MapTeaserBox {...props} />, el)
}
