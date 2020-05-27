var request = require('request');

module.exports = (app) => {
    app.get('/', require('./home').get);
    app.get('/test', require('./test').get);
}