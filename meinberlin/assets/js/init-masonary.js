const $ = require('jquery')

$('.grid').masonry({
  // set itemSelector so .grid-sizer is not used in layout
  itemSelector: '.grid-item',
  // use element for option
  // columnWidth: 160
  percentPosition: true,
  columnWidth: '.grid-sizer'
})
