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
    console.log(analysisOption);

    // Submit analysis option to job API
    axios.post("http://localhost:20102/api/job", [{
        targetURL: analysisOption.target.url,
        knownInfo: analysisOption.info,
        recursiveLevel: analysisOption.tool.analysisLevel,
        uriPath: analysisOption.target.path,
        done: false,
        maximumProcess: "None"
    }])
        .then(jobDataSubmitRes => {

            axios.post("http://localhost:20302/", analysisOption)
                .then(jobSubmitRes => console.log("Done!"))
                .catch(jobSubmitError => console.log("Fail! @ Final job submission", jobSubmitError.response.data));
            res.send("Submitted!");
        })
        .catch(jobDataSubmitError => {
            console.log("Fail! @ Job data submission!", jobDataSubmitError);
        });
    // res.send(req.body.analysisOption)
});

module.exports = router;
