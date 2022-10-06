import { format } from 'timeago.js'

const formatTime = (): void => {
  const times: NodeListOf<HTMLTimeElement> = document.querySelectorAll('time.relative')

  times.forEach((element) => {
    const sevenDays = 60 * 60 * 24 * 7 * 1000
    const datetime = new Date(element.dateTime)

    if (new Date().valueOf() - datetime.valueOf() < sevenDays) {
      element.textContent = format(datetime, 'de')
    }
  })
}

document.addEventListener('DOMContentLoaded', formatTime)
