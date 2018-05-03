# Participation platform mein.berlin

mein.berlin is a participation platform for the city of Berlin, Germany. It is
based on [adhocracy 4](https://github.com/liqd/adhocracy4).

## Requirements

*   nodejs (+ npm)
*   python 3.x (+ venv + pip)
*   libmagic
*   libjpeg
*   libpq (only if postgres should be used)
*   gdal

## Installation

    git clone https://github.com/liqd/a4-meinberlin.git
    cd a4-meinberlin
    make install
    make fixtures
    make watch
