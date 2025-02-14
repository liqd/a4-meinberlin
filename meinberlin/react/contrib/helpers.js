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

/*
 * converts an object to URLSearchParams
 *
 * This function takes an object and converts it into a URLSearchParams
 * instance, which can be used for query string formatting in URLs.
 * It handles arrays by appending each value to the parameter, and ignores
 * any null or undefined values.
 *
 * Example:
 * For the input:
 *   { search: 'apple', category: 'fruit', tags: ['red', 'green'], page: null }
 * The output will be:
 *   "search=apple&category=fruit&tags=red&tags=green"
 *
 * @param {Object} params - The object to convert into URLSearchParams
 * @returns {URLSearchParams} - The resulting URLSearchParams instance
 */
export const toSearchParams = (params) => {
  return Object.entries(params).reduce((acc, [key, value]) => {
    if (value == null || value === '') return acc

    if (Array.isArray(value)) {
      value.forEach(val => (val != null && val !== '') && acc.append(key, val))
    } else {
      acc.set(key, value)
    }

    return acc
  }, new URLSearchParams())
}
