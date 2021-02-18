/* global django */
const React = require('react')
const Moment = require('moment')

const remainingStr = django.gettext('remaining')
const moreThanStr = django.gettext('More than 1 year remaining')
const participationProjectsStr = django.gettext('Participation projects: ')
const futureParticipationStr = django.gettext('Participation: from ')
const endedParticipationStr = django.gettext('Participation ended. Read result.')
const statusStr = django.gettext('Status: ')
const nothingStr = django.gettext('Nothing to show')

const autoScrollThreshold = 500
const itemListInterval = 10

class LazyBackground extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      source: null
    }
  }

  componentDidMount () {
    window.addEventListener('scroll', this.handleScroll.bind(this), { passive: true })
    this.checkLoadImage()
  }

  componentWillUnmount () {
    window.removeEventListener('scroll', this.handleScroll.bind(this))
  }

  componentDidUpdate (prevProps, prevState, snapshot) {
    if (this.props.item.tile_image !== prevProps.item.tile_image) {
      this.setState({
        source: this.isInViewport() ? this.props.item.tile_image : null
      })
    }
  }

  handleScroll () {
    this.checkLoadImage()
  }

  checkLoadImage () {
    if (this.isInViewport() && !this.state.source) {
      this.setState({
        source: this.props.item.tile_image
      })
    }
  }

  isInViewport () {
    if (!this.lazyBackground) return false
    const rect = this.lazyBackground.getBoundingClientRect()
    const windowHeight = (window.innerHeight || document.documentElement.clientHeight)

    const res = !(Math.floor(100 - (((rect.top >= 0 ? 0 : rect.top) / +-(rect.height / 1)) * 100)) < 1 ||
      Math.floor(100 - ((rect.bottom - windowHeight) / rect.height) * 100) < 1
    )
    return res
  }

  render () {
    return (
      <div
        ref={(el) => (this.lazyBackground = el)}
        className={this.props.isHorizontal ? 'u-lg-only-display maplist-item__img' : 'maplist-item__img'} style={{
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          backgroundImage: this.state.source ? `url(${this.state.source})` : 'none'
        }} alt=""
      >
        {!this.props.isHorizontal && this.props.renderTopics(this.props.item)}
        {this.props.item.tile_image_copyright &&
          <span className="maplist-item__img-copyright copyright">© {this.props.item.tile_image_copyright}</span>}
      </div>
    )
  }
}

class PlansList extends React.Component {
  constructor (props) {
    super(props)

    this.addItemsToList = this.addItemsToList.bind(this)
    this.bindList = this.bindList.bind(this)
    this.handleScroll = this.handleScroll.bind(this)
    this.renderTopics = this.renderTopics.bind(this)

    this.state = {
      itemList: []
    }
  }

  componentDidMount () {
    window.addEventListener('scroll', this.handleScroll, { passive: true })
    this.addItemsToList()
  }

  componentWillUnmount () {
    window.removeEventListener('scroll', this.handleScroll)
  }

  getDocumentHeight () {
    const D = document
    return Math.max(
      D.body.scrollHeight, D.documentElement.scrollHeight,
      D.body.offsetHeight, D.documentElement.offsetHeight,
      D.body.clientHeight, D.documentElement.clientHeight
    )
  }

  handleScroll () {
    const html = document.documentElement
    if (html.scrollTop + html.clientHeight > this.getDocumentHeight() - autoScrollThreshold) {
      this.addItemsToList()
    }
  }

  addItemsToList () {
    const newItemList = this.state.itemList.slice()
    for (let i = this.state.itemList.length;
      i < this.props.items.length &&
      (i - this.state.itemList.length) < itemListInterval; i++) {
      newItemList.push(this.renderListItem(this.props.items[i], i))
    }
    this.setState({
      itemList: newItemList
    })
  }

  bindList (element) {
    this.listElement = element
  }

  getWidth (item) {
    return { width: item.active_phase[0] + '%' }
  }

  getTimespan (item) {
    const timeRemaining = item.active_phase[1].split(' ')
    const daysRemaining = parseInt(timeRemaining[0])
    if (daysRemaining > 365) {
      return (
        <span>{moreThanStr}</span>
      )
    } else {
      return (
        <span>{remainingStr} {item.active_phase[1]}</span>
      )
    }
  }

  getTopicList (item) {
    const topicList = item.topics.map((val) => {
      return this.props.topicChoices[val]
    })
    return topicList
  }

  renderTopics (item) {
    const topicsList = this.getTopicList(item)
    if (item.topics) {
      return (
        <div className={item.tile_image ? 'maplist-item__label-img' : 'maplist-item__label-spacer'}>
          {topicsList.map(topic =>
            <span key={topic} className="label label--secondary maplist-item__label u-spacer-bottom">{topic}</span>
          )}
        </div>
      )
    }
  }

  getText (item) {
    if (item.length > 170) {
      return item.substr(0, 170) + '...'
    } else {
      return item
    }
  }

  getDate (item) {
    let newDate = Date.parse(item.future_phase.replace(/ /g, 'T'))
    newDate = Moment(newDate).format('DD.MM.YYYY')
    return newDate
  }

  renderListItem (item, i) {
    const statusClass = (item.participation_active === true) ? 'participation-tile__status-active' : 'participation-tile__status-inactive'
    return (
      <li
        className={this.props.isHorizontal ? 'participation-tile__horizontal' : 'participation-tile__vertical'}
        key={i}
      >

        <a href={item.url} target={item.subtype === 'external' ? '_blank' : '_self'} rel="noreferrer">
          {item.type === 'project' &&
            <div className="participation-tile__body maplist-item">
              {item.tile_image &&
                <LazyBackground
                  item={item}
                  renderTopics={this.renderTopics}
                  isHorizontal={this.props.isHorizontal}
                />}
              <div className="participation-tile__content">
                {(this.props.isHorizontal || !item.tile_image) && this.renderTopics(item)}
                <span className="maplist-item__roofline">{item.district}</span>
                <h3 className="maplist-item__title">{item.title}</h3>
                {!this.props.isHorizontal &&
                  <div className="maplist-item__description">
                    <span>{this.getText(item.description)}</span>
                  </div>}
                <div className="maplist-item__link" />
                {item.subtype === 'container' &&
                  <div className="maplist-item__stats">
                    <span className="participation-tile__proj-count">
                      <i
                        className="fas fa-th"
                        aria-hidden="true"
                      />{
                        participationProjectsStr
                      }
                    </span>
                    <span>{item.published_projects_count}</span>
                  </div>}
                {item.future_phase && !item.active_phase &&
                  <div className="status-item status__future">
                    <span className="participation-tile__status">
                      <i
                        className="fas fa-clock"
                        aria-hidden="true"
                      />{futureParticipationStr}{this.getDate(item)}
                    </span>
                  </div>}
                {item.active_phase &&
                  <div className="status-item status__active">
                    <div className="status-bar__active">
                      <span
                        className="status-bar__active-fill"
                        style={this.getWidth(item)}
                      />
                    </div>
                    <span className="participation-tile__status"><i className="fas fa-clock" aria-hidden="true" />
                      {this.getTimespan(item)}
                    </span>
                  </div>}
                {item.past_phase && !item.active_phase && !item.future_phase &&
                  <div className="status-item status-bar__past">
                    <span
                      className="participation-tile__status"
                    >{endedParticipationStr}
                    </span>
                  </div>}
              </div>
              <div className="status-item_spacer" />
            </div>}
          {item.type === 'plan' &&
            <div className="participation-tile__body maplist-item">
              {item.tile_image &&
                <LazyBackground
                  item={item}
                  renderTopics={this.renderTopics.bind(this)}
                  isHorizontal={this.props.isHorizontal}
                />}
              <div className="participation-tile__content">
                {(this.props.isHorizontal || !item.tile_image) && this.renderTopics(item)}
                <span className="maplist-item__roofline">{item.district}</span>
                <h3 className="maplist-item__title">{item.title}</h3>
                <div className="maplist-item__link" />
                <div className="maplist-item__stats">
                  <span className="participation-tile__proj-count">
                    <i
                      className="fas fa-th"
                      aria-hidden="true"
                    />{
                      participationProjectsStr
                    }
                  </span>
                  <span>{item.published_projects_count}</span>
                  <br />
                  <span className="participation-tile__status">
                    <i
                      className="fas fa-clock"
                      aria-hidden="true"
                    />{statusStr}
                  </span>
                  <span className={statusClass}>{item.participation_string}</span>
                </div>
                <div className="status-item_spacer" />
              </div>
            </div>}
          {item.subtype === 'external' &&
            <div className="maplist-item__corner-badge maplist-item__corner-badge--external" />}
          {item.access === 2 && item.type === 'project' &&
            <div className="maplist-item__corner-badge maplist-item__corner-badge--semi-public" />}
          {item.access === 3 && item.type === 'project' &&
            <div className="maplist-item__corner-badge maplist-item__corner-badge--private" />}
        </a>
      </li>
    )
  }

  renderList () {
    if (this.state.itemList.length > 0) {
      return (
        <ul className="u-list-reset participation-tile__list">
          {this.state.itemList}
        </ul>
      )
    } else {
      return (
        <div className="list-item-empty">{nothingStr}</div>
      )
    }
  }

  render () {
    return (
      <div ref={this.bindList}>
        {this.renderList()}
      </div>
    )
  }
}

module.exports = PlansList
