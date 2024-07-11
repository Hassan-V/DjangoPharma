const path = require('path');

module.exports = {
  entry: {
    main: './central/static/js/index.js',
  },
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'central/static/js'),
  },
  mode: 'development',
};
