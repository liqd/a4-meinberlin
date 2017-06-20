var React = require('react')
var django = require('django')

// const ChapterListItem = (name, handleMoveUp, handleMoveDown, handleDelete, ...props) => {
//   return (
//   <div>
//     <h3>{name}</h3>
//
//     <div className="commenting__actions button-group">
//       <button
//         className="button button--light"
//         onClick={handleMoveUp}
//         disabled={!handleMoveUp}
//         title={django.gettext('Move up')}
//         type="button">
//         <i className="fa fa-chevron-up"
//            aria-label={django.gettext('Move up')}/>
//       </button>
//       <button
//         className="button button--light"
//         onClick={handleMoveDown}
//         disabled={!handleMoveDown}
//         title={django.gettext('Move down')}
//         type="button">
//         <i className="fa fa-chevron-down"
//            aria-label={django.gettext('Move down')}/>
//       </button>
//       <button
//         className="button button--light"
//         onClick={handleDelete}
//         title={django.gettext('Delete')}
//         type="button">
//         <i className="fa fa-trash"
//            aria-label={django.gettext('Delete')}/>
//       </button>
//     </div>
//   </div>
// )}

const ChapterListItem = React.createClass({
  getErrorCount: function () {
    if (this.props.errors && Object.keys(this.props.errors).length > 0) {
      let errorCount = Object.keys(this.props.errors).length
      if (this.props.errors['paragraphs']) {
        errorCount = errorCount - 1 + Object.keys(this.props.errors['paragraphs']).length
      }
      return <span className="errorcount"> ({errorCount})</span>
    }
  },

  render: function () {
    return (
      <li className="commenting">
        <button className="commenting__content commenting--toc__button button button--light button--small" type="button" onClick={this.props.onClick}>
          {this.props.name}
          {this.getErrorCount()}
        </button>

        <div className="commenting__actions button-group">
          <button
            className="button button--light button--small"
            onClick={this.props.onMoveUp}
            disabled={!this.props.onMoveUp}
            title={django.gettext('Move up')}
            type="button">
            <i className="fa fa-chevron-up"
              aria-label={django.gettext('Move up')} />
          </button>
          <button
            className="button button--light button--small"
            onClick={this.props.onMoveDown}
            disabled={!this.props.onMoveDown}
            title={django.gettext('Move down')}
            type="button">
            <i className="fa fa-chevron-down"
              aria-label={django.gettext('Move down')} />
          </button>
          <button
            className="button button--light button--small"
            onClick={this.props.onDelete}
            title={django.gettext('Delete')}
            type="button">
            <i className="fa fa-trash"
              aria-label={django.gettext('Delete')} />
          </button>
        </div>
      </li>
    )
  }
})

module.exports = ChapterListItem
