import cookie from 'js-cookie'

export function updateItem (data, url, method) {
  return fetch(url, {
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'X-CSRFToken': cookie.get('csrftoken')
    },
    method,
    body: JSON.stringify(data)
  }
  )
}

// toLocaleDate returns a formatted and internationalized
// date string. Fallback formatting is the German variant.
// input: 2021-11-11T15:37:19.490201+01:00
// output: 11. November 2021 (depending on locale)
export const toLocaleDate = (
  isodate,
  locale = 'de-DE',
  formatStyle = { month: 'short', day: 'numeric', year: 'numeric' }
) => {
  const date = new Date(isodate)
  return new Intl.DateTimeFormat(locale, formatStyle).format(date)
}

/*
 * checks if two arrays are equal
 *
 * @param {array} a
 * @param {array} b
 * @returns {boolean}
 */
export const arraysEqual = (a, b) => {
  if (a === b) return true
  if (a == null || b == null) return false
  if (a.length !== b.length) return false

  const aSorted = [...a].sort()
  const bSorted = [...b].sort()

  for (let i = 0; i < aSorted.length; ++i) {
    if (aSorted[i] !== bSorted[i]) return false
  }
  return true
}
