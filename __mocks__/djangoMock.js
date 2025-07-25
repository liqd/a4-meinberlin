module.exports = {
  gettext: (text) => text,
  pgettext: (text) => text,
  ngettext: (text, count) => text + count,
  interpolate: (text, count) => text + count,
  npgettext: (context, text, count) => text + count
}
