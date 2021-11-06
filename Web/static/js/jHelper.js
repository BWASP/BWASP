class API {
    constructor() {
        this.getConfig();
        console.log(this);
    }

    async getConfig(){
        await fetch("/static/data/frontConfig.json")
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
        this.getConfig().then(()=>{
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
                    callback(error)
                })
        })
    }

    /**
     * Send data to API
     * @param {string} endpoint
     * @param {string} type POST
     * @param {object} data null
     * @param {function} callback
     */
    relativeCommunication(endpoint, type="POST", data=null, callback){
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
     * @returns {string} Pure JSON
     */
    jsonDataHandler(str) {
        let replaceKeyword = "::SINGLE-QUOTE::";
        str = str.replaceAll("\\'", replaceKeyword).replaceAll("'", "\"").replaceAll(replaceKeyword, "\\'");
        return JSON.parse(str);
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

export {API, createKey};
