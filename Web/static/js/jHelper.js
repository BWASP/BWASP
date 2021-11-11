class API {
    constructor() {
        fetch("/static/data/frontConfig.json")
            .then(blob => blob.json())
            .then(res => {
                this.API = res.API
                this.debug = res.debug
            })
    }

    /**
     * Communicate with API
     * @param {string} endpoint
     * @param {function} callback
     */
    communicate(endpoint, callback) {
        if(typeof(this.API)==="undefined") return callback(["API Communication error", "Please wait until it retries."]);
        fetch(this.API.base + endpoint, {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        })
            .then(blob => blob.json())
            .then(res => {
                if (this.debug.mode === true
                    && this.debug.functions.printAllOutput === true) console.log(`:: DEBUG : RETURN ::\n${res}`);
                callback(null, res);
            })
            .catch(error => {
                console.log(`:: DEBUG : ERROR ::\n${error}`);
                callback(error.toString().split(": "))
            })
    }

    /**
     * Send data to API
     * @param {string} endpoint
     * @param {string} type POST
     * @param {object} data null
     * @param {function} callback
     */
    relativeCommunication(endpoint, type = "POST", data = null, callback) {
        fetch(this.API.base + endpoint, {
            method: type,
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accept": "application/json"
            },
            body: JSON.stringify(data)
        })
            .then(blob => blob.json())
            .then(res => {
                if (this.debug.mode === true
                    && this.debug.functions.printAllOutput === true) console.log(`:: DEBUG : RETURN ::\n${res}`);
                callback(null, res);
            })
            .catch(error => {
                console.log(`:: DEBUG : ERROR ::\n${error}`);
                callback(error)
            })
    }

    /**
     * JSON Data handling
     * @param {string} str Malformed JSON
     * @param {boolean} parseJSON true
     * @returns {string} Pure JSON
     */
    jsonDataHandler(str, parseJSON = true) {
        if (typeof (str) === "object") return str;
        let replaceKeyword = ["::SINGLE-QUOTE::", "::DOUBLE-QUOTE::"];
        str = str
            .replaceAll("\"", replaceKeyword[1])
            .replaceAll("\\'", replaceKeyword[0])
            .replaceAll("'", "\"")
            .replaceAll("True", "true")
            .replaceAll("False", "false")
            .replaceAll(replaceKeyword[0], "'")
            .replaceAll(replaceKeyword[1], "\"");
        ["True", "False"].forEach((currentKeyword)=>{
            str = str.replaceAll(currentKeyword, currentKeyword.toLowerCase);
        })
        return (parseJSON) ? JSON.parse(str) : str;
    }
}

class tableBuilder {
    /**
     * Builds table <thead> element
     * @param {Array} elements
     * @return {Object} thead
     */
    buildHead(elements) {
        if (typeof (elements) !== "object" || elements.length === 0) return Error("tableBuilder.buildHead() : Expected array of heading elements");
        let thead = {
            parent: document.createElement("thead"),
            child: document.createElement("tr")
        };
        elements.forEach((currentElement) => {
            let tmpElement = document.createElement("th");
            tmpElement.classList.add("text-center");
            tmpElement.innerText = currentElement;
            thead.child.appendChild(tmpElement);
        })
        thead.parent.appendChild(thead.child);
        return thead.parent;
    }

    dataNotPresent() {
        let noData = document.createElement("td");
        noData.innerText = " - ";
        noData.classList.add("text-muted", "text-center");
        return noData;
    }

    commaAsElement() {
        let comma = document.createElement("span");
        comma.innerText = ", ";
        return comma;
    }
}

/**
 * Create random keys
 * @param {number} level
 * @param {string} keyPrefix
 * @returns {string} Created key
 */
let createKey = (level = 2, keyPrefix = "anonID") => {
    let createdKey = keyPrefix;
    let gen = () => {
        return Math.random().toString(36).substring(2);
    }
    for (let i = 0; i < level; i++) createdKey += `-${gen()}`;
    return createdKey;
}

String.prototype.format = function () {
    let outputText = this;
    for (let arg in arguments) {
        outputText = outputText.replace("{" + arg + "}", arguments[arg]);
    }
    return outputText;
};

export {API, createKey, tableBuilder};
