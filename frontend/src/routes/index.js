let express = require('express');
let router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/dashboard', function(req, res, next) {
  res.render('dashboard', { title: 'Dashboard' });
});

router.get('/automation/options', function(req, res, next) {
  res.render('options/automation', { title: 'Dashboard' });
});

router.get('/common/attack_vector', function(req, res, next) {
  res.render('common/attackVector', { title: 'Dashboard' });
});

module.exports = router;
