const config = {
  testEnvironment: 'jsdom',
  modulePaths: [
    '<rootDir>'
  ],
  moduleNameMapper: {
    '\\.(css|less|scss|sass)$': '<rootDir>/__mocks__/styleMock.js',
    '\\.(gif|ttf|eot|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '(django)': '<rootDir>/__mocks__/djangoMock.js',
    'react-flip-move': '<rootDir>/__mocks__/flipmoveMock.js',
    // maplibre-gl v6 is ESM only and jest resolves modules as CommonJS
    '^maplibre-gl$': '<rootDir>/__mocks__/maplibreGlMock.js',
    '^maplibre-gl/dist/maplibre-gl\\.mjs$': '<rootDir>/__mocks__/maplibreGlMock.js'
  },
  testMatch: [
    '**/*.jest.js',
    '**/*.jest.jsx'
  ],
  collectCoverage: true,
  collectCoverageFrom: [
    '**/*.jsx',
    '!**/coverage/**',
    '!**/node_modules/**',
    '!**/babel.config.js',
    '!**/jest.setup.js',
    '!**/chrome/**',
    '!**/site-packages/adhocracy4/**',
    '!static/**'
  ],
  testPathIgnorePatterns: [
    '/(.*/site-packages/adhocracy4/.*)/',
    '/(static/.*)/'
  ],
  transform: {
    '^.+\\.[t|j]sx?$': 'babel-jest'
  },
  transformIgnorePatterns: [
  // transpile all node_modules, not great?
    '/node_modules/(?!(.*)/)'
  ],
  setupFilesAfterEnv: [
    '<rootDir>/setupTests.js'
  ]
}

module.exports = config
