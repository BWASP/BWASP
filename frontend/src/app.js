let createError = require('http-errors');
let express = require('express');
let path = require('path');
let cookieParser = require('cookie-parser');
let logger = require('morgan');
let fs = require('fs');

let indexRouter = require('./routes/index');
let apiRouter = require('./routes/api');
let usersRouter = require('./routes/users');

let app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use(function (req, res, next) {

    /*
        For NodeJS-Only (Standalone mode)
         - Make sure variable "standaloneMode" must be false before production for Docker container-by-container communication
     */
    let standaloneMode = false,
        localhostAddr = "http://localhost",
        configAPI = JSON.parse(fs.readFileSync("config/apiAddress.json", "utf8"));

    res.locals.API = {
        api: ((standaloneMode) ? localhostAddr : configAPI.api["url"]).concat(`:${configAPI.api["port"]}`),
        core: {
            auto: ((standaloneMode) ? localhostAddr : configAPI.core.auto["url"]).concat(`:${configAPI.core.auto["port"]}`),
            manual: ((standaloneMode) ? localhostAddr : configAPI.core.manual["url"]).concat(`:${configAPI.core.manual["port"]}`)
        }
    }
    next();
});

app.use('/', indexRouter);
app.use('/api', apiRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function (req, res, next) {
    next(createError(404));
});

// error handler
app.use(function (err, req, res, next) {
    // set locals, only providing error in development
    res.locals.message = err.message;
    res.locals.error = req.app.get('env') === 'development' ? err : {};

    // render the error page
    res.status(err.status || 500);
    res.render('error');
});

module.exports = app;
