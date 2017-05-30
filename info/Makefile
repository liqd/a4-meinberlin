TARGET := ../meinberlin/static/info

all: index.html style.css

install: all
	mkdir -p $(TARGET)
	cp index.html $(TARGET)
	cp style.css $(TARGET)
	mkdir -p $(TARGET)/images
	cp -r images/* $(TARGET)/images
	mkdir -p $(TARGET)/bower_components
	mkdir -p $(TARGET)/bower_components/smooth-scroll/dist/js/
	cp -r bower_components/smooth-scroll/dist/js/smooth-scroll.min.js $(TARGET)/bower_components/smooth-scroll/dist/js/.

index.html: index.mustache build.js node_modules
	node build.js > $@

style.css: scss/style.scss scss/*.scss scss/components/*.scss bower_components
	node-sass --output-style expanded $< > $@

bower_components:
	bower install xi/sass-planifolia
	bower install cferdinandi/smooth-scroll

node_modules:
	npm install mustache
	npm install markdown-it

clean:
	rm -f index.html style.css
