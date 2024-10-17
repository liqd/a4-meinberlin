import React from 'react'
import django from 'django'
import { IconSwitch } from '../contrib/IconSwitch'
import { ToggleSwitch } from '../contrib/ToggleSwitch'
import { PillBtn } from '../contrib//PillBtn'

const filterProjectListStr = django.gettext('Filtered list of projects')
const searchResultsStr = django.gettext(' search results')
const removeFilterStr = django.gettext(' remove filter')
const showMapStr = django.gettext('Show map')
const showMapAriaStr = django.gettext('show map')
const listStr = django.gettext('List')
const mapStr = django.gettext('Map')
const showListStr = django.gettext('show list')
const viewModeStr = django.gettext('View mode')

class Toggles extends React.Component {
  clickStatusButton () {
    this.props.changeStatusSelection(-1)
  }

  clickParticipationButton () {
    this.props.changeParticipationSelection(-1)
  }

  clickOrganisationButton () {
    this.props.changeOrganisationSelection('-1')
  }

  clickTitleSearchButton () {
    this.props.changeTitleSearchSelection('-1')
  }

  titleSearchButtonString () {
    if (this.props.titleSearchString.length > 20) {
      return this.props.titleSearchString.substr(0, 20) + '...'
    }
    return this.props.titleSearchString
  }

  organisationButtonString () {
    if (this.props.organisationString.length > 20) {
      return this.props.organisationString.substr(0, 20) + '...'
    }
    return this.props.organisationString
  }

  statusFilterBtn () {
    if (this.props.displayButtons && this.props.statusSelected) {
      return (
        <PillBtn
          removeItemStr={removeFilterStr}
          onClickRemove={this.clickStatusButton.bind(this)}
          choiceBtnID="remove-search-filter"
          choiceString={this.props.statusString}
          choiceCount={this.props.statusCount}
        />
      )
    }
  }

  organisationFilterBtn () {
    if (this.props.displayButtons && this.props.organisationSelected) {
      return (
        <PillBtn
          removeItemStr={removeFilterStr}
          onClickRemove={this.clickOrganisationButton.bind(this)}
          choiceBtnID="remove-organisation-filter"
          choiceString={this.organisationButtonString()}
        />
      )
    }
  }

  participationFilterBtn () {
    if (this.props.displayButtons && this.props.participationSelected) {
      return (
        <PillBtn
          removeItemStr={removeFilterStr}
          onClickRemove={this.clickParticipationButton.bind(this)}
          choiceBtnID="remove-search-filter"
          choiceString={this.props.participationString}
          choiceCount={this.props.participationCount}
        />
      )
    }
  }

  searchFilterBtn () {
    if (this.props.displayButtons && this.props.titleSearchSelected) {
      return (
        <PillBtn
          removeItemStr={removeFilterStr}
          onClickRemove={this.clickTitleSearchButton.bind(this)}
          choiceBtnID="remove-search-filter"
          choiceString={this.titleSearchButtonString()}
          choiceCount={this.props.titleSearchCount}
        />
      )
    }
  }

  render () {
    if (this.props.isSlider) {
      return (
        <div>
          <h2 className="visually-hidden-focusable">{filterProjectListStr}</h2>
          <div className="l-frame switch-container">
            <div className={this.props.displayButtons ? 'switch-filter__label' : 'd-none'}>{this.props.projectCount}{searchResultsStr}</div>
            <div className="switch-filter__btn-group">
              {this.statusFilterBtn()}
              {this.participationFilterBtn()}
              {this.organisationFilterBtn()}
              {this.searchFilterBtn()}
            </div>
            <ToggleSwitch
              uniqueId="map-switch"
              toggleSwitch={this.props.toggleSwitch}
              onSwitchStr={showMapStr}
              defaultChecked
            />
          </div>
        </div>
      )
    } else {
      return (
        <div>
          <div className="l-frame switch-container mb-2">
            <div className={this.props.displayButtons ? 'switch-filter__label' : 'd-none'}>{this.props.projectCount}{searchResultsStr}</div>
            <div className="switch-filter__btn-group">
              {this.statusFilterBtn()}
              {this.participationFilterBtn()}
              {this.organisationFilterBtn()}
              {this.searchFilterBtn()}
            </div>
            <IconSwitch
              fullWidth
              viewModeStr={viewModeStr}
              buttons={[
                {
                  ariaLabel: showListStr,
                  label: listStr,
                  icon: 'fa fa-list',
                  id: 'show_list',
                  isActive: !this.props.displayMap,
                  handleClick: this.props.showList
                },
                {
                  ariaLabel: showMapAriaStr,
                  label: mapStr,
                  icon: 'fa fa-map',
                  id: 'show_map',
                  isActive: this.props.displayMap,
                  handleClick: this.props.showMap
                }
              ]}
            />
          </div>
        </div>
      )
    }
  }
}

module.exports = Toggles
