function APICommunicationError(name, message) {
    this.message = message;
    this.name = name;
}

class API {
    constructor() {
        this.API = String();
        this.debug = Object();
        this.requestOptions = {
            method: "GET",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        };
        this.getFrontConfig();
    }

    async getFrontConfig() {
        if (this.API !== String() && this.debug !== Object()) return;
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
     * @param {string} requestType
     * @param {object} dataPackage
     * @param {boolean} isLocalhost
     */
    async communicate(endpoint, requestType = "GET", dataPackage = null, isLocalhost = false) {
        await this.getFrontConfig();
        let requestOptions = {
            method: requestType,
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json"
            }
        };
        if (dataPackage !== null) requestOptions["body"] = JSON.stringify(dataPackage);
        const communication = await fetch(`${(isLocalhost) ? "" : this.API.base}${endpoint}`, requestOptions)
            .catch(error => {
                error = error.toString().split(": ");
                throw new APICommunicationError(error[0], error[1]);
            });
        const dataset = await communication.json();
        if (communication.ok) return dataset;
        if (!communication.ok) throw new APICommunicationError("Error", communication.statusText);
    }

    /**
     * JSON Data handling
     * @param {string} str Malformed JSON
     * @param {boolean} parseJSON true
     * @returns {string} Pure JSON
     */
    jsonDataHandler(str, parseJSON = true) {
        if (["object"].includes(typeof (str))) return str;
        let replaceKeyword = ["::SINGLE-QUOTE::", "::DOUBLE-QUOTE::"];
        let replaceKeywords = [
            ["\"", replaceKeyword[1]],
            ["\\'", replaceKeyword[0]],
            ["'", "\""],
            [replaceKeyword[0], "'"],
            [replaceKeyword[1], "\""],
            ["True", "true"],
            ["False", "false"]
        ];
        try {
            JSON.parse(str);
        } catch (e) {
            if (e instanceof SyntaxError) replaceKeywords.forEach(key => str = str.replaceAll(key[0], key[1]));
            else console.error(e);
        }
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

let setMultipleAttributes = (el, attrs) => {
    Object.keys(attrs).forEach(key => el.setAttribute(key, attrs[key]));
}

const createToast = (title, content = "", color = "primary", inline = false, duration = 5) => {
    let prefix = "jFront-Toast";
    let toastAreaID = `${prefix}-Area`;
    let currentToastID = createKey(3, "jFrontToast");
    let colorMatching = {
        danger: "light",
        primary: "light",
        success: "light"
    }[color];
    // Check toast area exists
    if (document.querySelectorAll(`#${toastAreaID}`).length === 0) {
        let localArea = document.createElement("section");
        localArea.id = toastAreaID;
        localArea.classList.add("toast-container", "position-absolute", "top-0", "end-0", "p-3");
        document.getElementsByTagName("body")[0].appendChild(localArea);
    }
    let toastArea = document.getElementById(toastAreaID);
    let toastSkeleton = {
        parent: document.createElement("div"),
        header: {
            parent: document.createElement("div"),
            title: document.createElement("strong"),
            closeButton: document.createElement("button")
        },
        body: document.createElement("div")
    };

    // Build parent
    toastSkeleton.parent.classList.add("toast", "rounded-custom", "border", `border-${color}`);
    if (inline) toastSkeleton.parent.classList.add("align-items-center");
    toastSkeleton.parent.id = currentToastID;
    setMultipleAttributes(toastSkeleton.parent, {
        "role": "alert",
        "aria-live": "assertive",
        "aria-atomic": "true"
    })

    // Build toast head and elements
    toastSkeleton.header.parent.classList.add((inline)
            ? "d-flex"
            : "toast-header",
        "rounded", `bg-${color}`);
    toastSkeleton.header.parent.classList.add(`bg-${color}`);
    toastSkeleton.header.title.classList.add("me-auto");
    toastSkeleton.header.closeButton.classList.add("btn-close");
    if (inline) toastSkeleton.header.closeButton.classList.add("me-2", "m-auto", `text-${colorMatching}`);
    setMultipleAttributes(toastSkeleton.header.closeButton, {
        "type": "button",
        "data-bs-dismiss": "toast",
        "aria-label": "Close"
    })

    // Build toast body
    toastSkeleton.body.classList.add("toast-body");
    if (inline) toastSkeleton.body.classList.add(`text-${colorMatching}`);
    else toastSkeleton.header.title.classList.add(`text-${colorMatching}`);

    // Set values
    toastSkeleton.header.title.innerText = title;
    toastSkeleton.body.innerText = (inline) ? title : content;

    // Mix elements
    if (inline) {
        toastSkeleton.header.parent.append(
            toastSkeleton.body,
            toastSkeleton.header.closeButton
        );
        toastSkeleton.parent.appendChild(toastSkeleton.header.parent);
    } else {
        toastSkeleton.header.parent.append(
            toastSkeleton.header.title,
            toastSkeleton.header.closeButton
        );
        toastSkeleton.parent.append(
            toastSkeleton.header.parent,
            toastSkeleton.body
        );
    }

    toastArea.appendChild(toastSkeleton.parent);

    // Get instance
    let toastBlob = document.getElementById(currentToastID);
    let currentToast = bootstrap.Toast.getOrCreateInstance(toastBlob, {
        delay: duration * 1000
    });

    // Show toast to user
    currentToast.show();

    // Delete toast after duration + 1 sec
    setTimeout(() => toastBlob.remove(), (duration + 1) * 1000)
}

const swapElement = (element, moveTo) => {
    moveTo.appendChild(element);
}

String.prototype.format = function () {
    let outputText = this;
    for (let arg in arguments) {
        outputText = outputText.replace("{" + arg + "}", arguments[arg]);
    }
    return outputText;
};

export {API, createKey, createToast, swapElement, tableBuilder};
