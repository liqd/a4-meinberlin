import React, { useEffect, useId, useState } from 'react'
import django from 'django'
import useDebounce from '../contrib/useDebounce'
import { useMap } from 'react-leaflet'
import { AutoComplete } from '../contrib/forms/AutoComplete'

const addressSearchCapStr = django.gettext('Address Search')

function fetchSuggestions (address) {
  return fetch(apiUrl + '?address=' + address)
    .then((response) => response.json())
}

function onAddressSearchChange (event) {
  if (event.target.value === '' && this.state.address) {
    this.map.removeLayer(this.state.address)
    this.setState({
      address: null
    })
  }
}

function selectSearchResult (event, searchResults) {
  const index = parseInt(event.target.value, 10)
  const address = searchResults[index]
  this.displayAdressMarker(address)
  this.setState(
    { displayResults: false }
  )
}

const apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'

const ProjectsMapSearch = ({
  onSubmitHandler
}) => {
  const id = useId()
  const [geoJson, setGeoJson] = useState(null)
  const [searchString, setSearchString] = useState('')
  const map = useMap()

  const debouncedOnChange = useDebounce(async () => {
    const geoJson = await fetchSuggestions(searchString)
    setGeoJson(geoJson)
  })

  useEffect(() => {
    debouncedOnChange()
  }, [searchString])

  return (
    <div className="projects-map-search">
      <form onSubmit={onSubmitHandler} data-embed-target="ignore">
        <div className="searchform-slot ">
          <div className="form-group">
            <label className="aural" htmlFor={id}>{addressSearchCapStr}</label>
            <div className="searchterm">
              <i className="bicon bicon-search lens" aria-hidden="true" />
              <AutoComplete choices={[{ name: 'Swedish', value: 'sv' }, { name: 'English', value: 'en' }]} />
              <button className="submit " type="submit" title="Suchen">
                <span className="aural">Suchen</span><i className="bicon bicon-arrow-right icon" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </form>
      {/* <form onSubmit={e => this.onAddressSearchSubmit(e)}> */}
      {/*  <div className="input-group"> */}
      {/*    <label */}
      {/*      htmlFor="id-map-address-search" */}
      {/*      className="visually-hidden" */}
      {/*    > */}
      {/*      {addressSearchCapStr} */}
      {/*    </label> */}
      {/*    <input */}
      {/*      className="form-control" */}
      {/*      type="search" */}
      {/*      id="id-map-address-search" */}
      {/*      placeholder={addressSearchCapStr} */}
      {/*      onChange={e => this.onAddressSearchChange(e)} */}
      {/*    /> */}
      {/*    <button */}
      {/*      className="btn btn--light input-group__after" */}
      {/*      type="submit" */}
      {/*    > */}
      {/*      <i className="fa fa-search" aria-hidden="true" /> */}
      {/*      <span className="visually-hidden"> */}
      {/*        {addressSearchCapStr} */}
      {/*      </span> */}
      {/*    </button> */}
      {/*  </div> */}
      {/* <ul aria-labelledby="id_filter_address"> */}
      {/*  {searchResults.map((name, i) => { */}
      {/*    return ( */}
      {/*      <li key={i}> */}
      {/*        <button */}
      {/*          type="button" */}
      {/*          value={i} */}
      {/*          onClick={this.selectSearchResult.bind(this)} */}
      {/*        > */}
      {/*          {name.properties.strname} {name.properties.hsnr} in {name.properties.plz} {name.properties.bezirk_name} */}
      {/*        </button> */}
      {/*      </li> */}
      {/*    ) */}
      {/*  })} */}
      {/* </ul> */}

      {/* {this.state.displayError && */}
      {/*  <ul aria-labelledby="id_filter_address" className="map-list-combined__map__search__error"> */}
      {/*    <li>{nothingStr}</li> */}
      {/*  </ul>} */}

    </div>
  )
}

export default ProjectsMapSearch
