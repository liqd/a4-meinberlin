import StickyBox from 'react-sticky-box'
const React = require('react')
let PlansList = require('./PlansList')
let PlansMap = require('./PlansMap')
let FilterNav = require('./FilterNav')
let ListMapSwitch = require('./MapListSwitch')

const breakpoint = 800

class ListMapBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      width: window.innerWidth,
      items: [],
      searchResults: null,
      address: null,
      selected: null,
      displayError: false,
      displayResults: false,
      showListMap: window.innerWidth > breakpoint,
      resizeMap: false,
      filterChanged: false,
      status: -1,
      participation: -1,
      district: props.selectedDistrict,
      topic: props.selectedTopic
    }
  }

  handleWindowSizeChange () {
    this.setState({ width: window.innerWidth })
  }

  componentWillMount () {
    window.addEventListener('resize', this.handleWindowSizeChange.bind(this))
  }

  componentWillUnmount () {
    window.removeEventListener('resize', this.handleWindowSizeChange.bind(this))
  }

  componentDidMount () {
    this.updateList()
  }

  componentDidUpdate () {
    if (this.state.filterChanged === true) {
      this.updateList()
    }
  }

  isInFilter (item) {
    return (this.state.topic === '-1' || this.state.topic === item.topic || this.state.topic.toLowerCase() === item.topic.toLowerCase()) &&
      (this.state.district === '-1' || this.state.district === item.district)
  }

  updateList () {
    let items = []
    this.props.initialitems.forEach((item, i) => {
      if (this.isInFilter(item)) {
        items.push(item)
      }
    })
    this.setState({
      items: items,
      filterChanged: false
    })
  }

  toggleSwitch () {
    let newValue = !this.state.showListMap
    this.setState({ showListMap: newValue })
  }

  selectDistrict (district) {
    this.setState({
      filterChanged: true,
      district: district
    })
  }

  selectTopic (topic) {
    this.setState({
      filterChanged: true,
      topic: topic
    })
  }

  render () {
    const { width } = this.state
    const isMobile = width <= breakpoint

    if (isMobile) {
      return (
        <div>
          <ListMapSwitch
            toggleSwitch={this.toggleSwitch.bind(this)}
          />
          {!this.state.showListMap &&
          <PlansList key="content" items={this.state.items} />
          }
          {this.state.showListMap &&
          <PlansMap key="content"
            resize={this.state.resizeMap}
            items={this.state.items}
            bounds={this.props.bounds}
            districts={this.props.districts}
            baseurl={this.props.baseurl}
            districtnames={this.props.districtnames} />
          }
        </div>)
    } else {
      return (
        <div>
          <FilterNav
            selectDistrict={this.selectDistrict.bind(this)}
            selectTopic={this.selectTopic.bind(this)}
            district={this.state.district}
            districtnames={this.props.districtnames}
            topic={this.state.topic}
            topicChoices={this.props.topicChoices}
          />
          <ListMapSwitch
            toggleSwitch={this.toggleSwitch.bind(this)}
          />
          { this.state.showListMap
            ? <div className="map-list-combined">
              <div id="list" className="list-container map-list-combined__list">
                <PlansList key="content" items={this.state.items} />
              </div>
              <div id="map" className="map-container map-list-combined__map">
                <StickyBox offsetTop={0} offsetBottom={0}>
                  <PlansMap key="content"
                    resize={this.state.resizeMap}
                    items={this.state.items}
                    bounds={this.props.bounds}
                    districts={this.props.districts}
                    baseurl={this.props.baseurl}
                    districtnames={this.props.districtnames} />
                </StickyBox>
              </div>
            </div>
            : <div className="map-list-combined">
              <div className="list-container map-list-combined__list">
                <PlansList key="content" items={this.state.items} />
              </div>
            </div>
          }
        </div>)
    }
  }
}

module.exports = ListMapBox
