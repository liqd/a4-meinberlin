/* global django */

const remainingStr = django.gettext('remaining')
const moreThanStr = django.gettext('More than 1 year remaining')

function getTimespan (item) {
  const timeRemaining = item.active_phase[1].split(' ')
  const daysRemaining = parseInt(timeRemaining[0])
  if (daysRemaining > 365) {
    return (moreThanStr)
  } else {
    return (
      remainingStr + ' ' + item.active_phase[1]
    )
  }
}

export default getTimespan
