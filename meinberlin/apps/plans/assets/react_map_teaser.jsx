import React from 'react'
import { createRoot } from 'react-dom/client'
import MapTeaserBox from './MapTeaserBox'

module.exports.renderFilter = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  const root = createRoot(el)
  root.render(<MapTeaserBox {...props} />, el)
}
