const $ = require('jquery')
const a4api = require('adhocracy4').api

/* eslint-disable */
$(function () {
  const dropdown = $('#idea-remark__dropdown')
  const attributes = dropdown.data('attributes')
  if (typeof attributes !== 'undefined') {
    const objectPk = attributes.item_object_id
    const contentTypeId = attributes.item_content_type
    const remarkId = attributes.id
    const remarkVal = attributes.remark
  }

  if (remarkId) {
    $('#id_remark').val(remarkVal)
  }

  $('#idea-remark__form').submit(function (e) {
    e.preventDefault()
    const $input = $('#id_remark')
    const newVal = $input.val()

    if (remarkVal !== newVal) {
      const data = {
        urlReplaces: {
          objectPk: objectPk,
          contentTypeId: contentTypeId
        },
        remark: newVal
      }

      let response
      if (remarkId) {
        response = a4api.moderatorremark.change(data, remarkId)
      } else {
        response = a4api.moderatorremark.add(data)
      }

      response.done(remark => {
        remarkId = remark.id
        remarkVal = remark.remark
        $('.dropdown.show .dropdown-toggle').dropdown('toggle')
        if (remarkVal) {
          dropdown.find('.idea-remark__btn__notify').show()
        } else {
          dropdown.find('.idea-remark__btn__notify').hide()
        }
      })
    } else {
      $('.dropdown.show .dropdown-toggle').dropdown('toggle')
    }
  })
})
/* eslint-enable */
