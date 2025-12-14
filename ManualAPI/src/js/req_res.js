class API {
    constructor() {
        this.API_url = "http://localhost:20202/"
    }

    /**
     * Send data to API
     * @param {string} endpoint
     * @param {string} type POST
     * @param {object} data null
     */
    requestCommunication(endpoint = this.API_url, type = "POST", data = null) {
        fetch(endpoint, {
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
                console.log(res)
            })
            .catch(error => {
                console.log(error)
            })
    }

    /**
     * Communicate with API
     * @param {string} endpoint
     */
    responseCommunicate(endpoint = this.API_url) {
        fetch(endpoint, {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        })
            .then(blob => blob.json())
            .then(res => {
                console.log(res)
            })
            .catch(error => {
                console.log(error)
            })
    }
}