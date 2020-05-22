var request = require('request');

module.exports = (app) => {
    app.get('/', require('./home').get);
}