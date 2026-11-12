// maplibre-gl v6 ships as ES module only and can no longer be resolved by
// jest's CommonJS module loader. The unit tests never render a real map, so a
// stub with the API surface used by adhocracy4 is sufficient.
class Map {}

const setWorkerUrl = () => {}

module.exports = { Map, setWorkerUrl }
