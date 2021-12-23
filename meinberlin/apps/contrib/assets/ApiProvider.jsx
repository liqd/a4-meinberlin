import React from 'react'
import cookie from 'js-cookie'

const getHeaders = () => ({
  'Content-Type': 'application/json; charset=utf-8',
  'X-CSRFToken': cookie.get('csrftoken')
})

const getOpts = (method, data) => {
  const opts = {
    headers: getHeaders(),
    method: method
  }
  data && (opts.body = JSON.stringify(data))
  return opts
}

const ApiContext = React.createContext(null)

export const ApiProvider = props => {
  const value = {
    get: props.get || get,
    post: props.post || post,
    put: props.put || put,
    patch: props.patch || patch,
    remove: props.remove || remove
  }
  return (
    <ApiContext.Provider value={value}>{props.children}</ApiContext.Provider>
  )
}

export const useApi = () => {
  const context = React.useContext(ApiContext)
  if (!context) {
    throw new Error(
      'useApi() only works with ApiProvider: context not there yet or missing?'
    )
  }
  return context
}

// Following methods are provided to interact with
// our REST Api endpoints. GET, POST, PUT, PATCH and
// DELETE (called REMOVE, bc its a reserved word)

const get = async url => {
  try {
    const response = await fetch(url)
    const json = await response.json()
    return [json, undefined]
  } catch (error) {
    return [undefined, error]
  }
}

const post = async (url, data) => {
  try {
    const opts = await getOpts('POST', data)
    const response = await fetch(url, opts)
    const json = await response.json()
    return [json, undefined]
  } catch (error) {
    return [undefined, error]
  }
}

const put = url => {
  console.log('PUT method fired')
}

const patch = url => {
  console.log('PATCH method fired')
}

const remove = async url => {
  try {
    const opts = await getOpts('DELETE')
    const response = await fetch(url, opts)
    const json = await response.json()
    return [json, undefined]
  } catch (error) {
    return [undefined, error]
  }
}
