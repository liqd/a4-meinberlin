import React, {useState} from 'react'

export const VotingCodeForm = (props) => {
  const [inputField , setInputField] = useState({
      voting_code: ''
  })

  const inputsHandler = (e) =>{
      setInputField( {[e.target.name]: e.target.value} )
  }

  const submitButton = () =>{
      alert("Thankyou for submitting")
  }

  return (
    <div className="form-group u-inline-flex">
      <input
        className="input-group__input"
        type="text"
        name="voting_code"
        onChange={inputsHandler}
        value={inputField.first_name}/>
      <button
        className="input-group__after btn"
        onClick={submitButton}>Redeem code</button>
    </div>
  )
}
