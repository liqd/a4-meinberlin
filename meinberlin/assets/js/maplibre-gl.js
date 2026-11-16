// maplibre-gl v6 is an ES module build that loads a separate web worker.
// Bundlers cannot infer the location of that worker, so it has to be
// registered explicitly. Webpack turns the `new URL()` below into an asset
// that is emitted next to the other static files.
import * as maplibregl from 'maplibre-gl/dist/maplibre-gl.mjs'

maplibregl.setWorkerUrl(
  new URL('maplibre-gl/dist/maplibre-gl-worker.mjs', import.meta.url).toString()
)

export * from 'maplibre-gl/dist/maplibre-gl.mjs'
