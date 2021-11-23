let express = require('express');
let axios = require('axios');
let router = express.Router();

const sendErrorToUser = (res, status, message) => {
    res.status(status).send({
        message: message
    });
}

/* GET users listing. */
router.post('/job/enroll', function (req, res, next) {
    // Send error if analysis option not presented
    if (typeof (req.body.analysisOption) === "undefined") return sendErrorToUser(res, 400, "Bad request");
    let analysisOption = JSON.parse(req.body.analysisOption);

    axios.post(res.locals.API.api + "/api/job", [{
        targetURL: analysisOption.target.url,
        knownInfo: analysisOption.info,
        recursiveLevel: analysisOption.tool.analysisLevel,
        uriPath: analysisOption.target.path,
        done: false,
        maximumProcess: "None"
    }])
        .then(jobDataSubmitRes => {
            console.log("\n[ SUCCESS ] Job data submission \n");

            axios.post(res.locals.API.core.auto, analysisOption)
                .then(jobSubmitRes => {
                    console.log("\n[ SUCCESS ] Final job order \n")
                    res.send("Submitted!");
                })
                .catch(jobSubmitError => {
                    console.log("\n[ FAIL ] Final job order \n================\n\n", jobSubmitError, "\n\n================")
                });
        })
        .catch(jobDataSubmitError => {
            console.log("\n[ FAIL ] Job data submission \n================\n\n", jobDataSubmitError, "\n\n================")
        });
    // res.send(req.body.analysisOption)
});

module.exports = router;
