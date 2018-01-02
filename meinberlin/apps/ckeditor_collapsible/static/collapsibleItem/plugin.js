/* eslint-disable */

function getCollapsibleItem() {
  return '<div class="collapsible-item">' +
         '   <div class="collapsible-item-title">Title Text</div>' +
         '   <div class="collapsible-item-body">Body Text</div>' +
         '</div>';
}

CKEDITOR.dtd.$editable.a = 1;

CKEDITOR.plugins.add('collapsibleItem', {
    requires: 'widget',
    icons: 'collapsibleitem',
    hidpi: true,
    init: function (editor) {
        editor.widgets.add('collapsibleItem', {
            button: 'Insert Collapsible Item',
            template: getCollapsibleItem(),
            editables: {
                title: {
                    selector: '.collapsible-item-title',
                    allowedContent: 'strong em u'
                },
                content: {
                    selector: '.collapsible-item-body',
                    allowedContent: 'p;br;span(*)[*];ul;ol;li;strong;em;u;hr;a;a[*];a(*)[*];img(*)[*];',
                }
            },
            allowedContent: 'div(!collapsible-item*)[*]',
            requiredContent: 'div(collapsible-item);',
            upcast: function (element) {
                return element.name == 'div' && element.hasClass('collapsible-item');
            },
            init: function () {
                //called when widget instance is created
                this.setData('itemId', 'Collapsible' + (new Date()).getTime());
            },
            data: function () {
                //called whenever the data is updated
                this.element.setAttribute('id', this.data.itemId);
            },
        });
    },

    onLoad: function () {
        CKEDITOR.addCss(
            '.collapsible-item::before {font-size:10px;color:#000;content: "Collapsible element"}' +
            '.collapsible-item {padding: 8px;margin: 10px;background: #eee;border-radius: 8px;border: 1px solid #ddd;box-shadow: 0 1px 1px #fff inset, 0 -1px 0px #ccc inset;}' +
            '.collapsible-item-title, .collapsible-item-body {box-shadow: 0 1px 1px #ddd inset;border: 1px solid #cccccc;border-radius: 5px;background: #fff;}' +
            '.collapsible-item-title {margin: 0 0 8px;padding: 5px 8px;}' +
            '.collapsible-item-body {padding: 0 8px;}'
        );
    }
});
