const path = require('path')
module.exports = {
  entry: {
    server: './server.js'
  },
  output: {
    path: path.resolve(__dirname, './dist'),
    filename: '[name].js'
  },
  target: 'node',
  module: {

  }
}
