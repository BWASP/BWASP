// Get modules
import {API as api, createKey, tableBuilder} from '../jHelper.js';

// Define API Endpoints
const APIEndpoints = {
        vectors: "/api/domain",
        packets: {
            base: "/api/packet",
            type: {
                auto: "automation",
                manual: "manual"
            }
        }
    },
    elements = {
        vectors: ["Category", "URL", "Action", "Params", "Vulnerability Doubt", "Method", "Impact"],
        packets: []
    };

let stateHandler = {
        isVector: true
    },
    keyAndStrings = [
        {
            type: "packets",
            viewString: "Packets"
        },
        {
            type: "vectors",
            viewString: "Attack Vectors"
        }
    ],
    pagination = {
        currentPage: 1,
        rowPerPage: 10
    },
    returnError = (errorMessage = ["No data", ""]) => {
        let condition = (typeof(errorMessage)!=="string");
        console.log(errorMessage, typeof(errorMessage), condition);
        document.getElementById("errMsgTitle").innerText = (condition)
            ? errorMessage[0]
            : errorMessage;
        document.getElementById("errMsgDesc").innerText = (condition)
            ? errorMessage[1]
            : "";
        document.getElementById("loadingProgress").classList.add("d-none");
        document.getElementById("resultNoData").classList.remove("d-none");
        console.error(`:: ERROR :: `, errorMessage);
    };

// define api communicator
let API = await new api()

class pagerTools {
    constructor() {
        this.className = "pagerTools";
        this.API = new api();
        this.paging = {
            currentPage: 1,
            rowPerPage: 10
        };
    }

    toggleLoader(type) {
        document.getElementById("loadingProgress").classList[(type) ? "add" : "remove"]("d-none");
    }

    updatePager(page, rowCount){

    }

    async buildPage() {
        await this.syncData(this.paging.currentPage, this.paging.rowPerPage, this.buildTable);
    }

    async syncData(requestPage, rowPerPage, callback) {
        let localDataPack = [],
            counter = Number();
        await API.communicate(
            APIEndpoints.vectors + `/${((requestPage - 1) * rowPerPage)+1}/${rowPerPage}`,
            (err, res) => {
                if (err) {
                    let redoJob = window.setTimeout(()=>{
                        this.syncData(requestPage, rowPerPage, callback);
                    }, 500);
                    return returnError(err);
                }
                if (res.length === 0) return returnError("No data");

                res.forEach(async (domainData) => {
                    let skeleton = {
                        category: Number(),
                        url: {
                            url: domainData.URL,
                            uri: domainData.URI
                        },
                        payloads: Array(),
                        action: {
                            target: API.jsonDataHandler(domainData["action_URL"]),
                            type: API.jsonDataHandler(domainData["action_URL_Type"])
                        },
                        params: API.jsonDataHandler(domainData["params"]),
                        allowMethod: Array(),
                        vulnerability: {
                            type: Object(),
                            cve: Array()
                        },
                        method: String(),
                        impactRate: 0,
                        details: API.jsonDataHandler(domainData["Details"])
                    };

                    // Reengineer details.
                    Object.keys(skeleton.details).forEach((key) => skeleton.details[key] = API.jsonDataHandler(skeleton.details[key]));

                    // Attack vector data regulation
                    let attackVector = API.jsonDataHandler(domainData["attackVector"]);
                    if (typeof (attackVector["Allow Method"]) !== "undefined") skeleton.allowMethod = attackVector["Allow Method"];
                    delete attackVector["Allow Method"];
                    skeleton.vulnerability.type = attackVector;

                    // Receive data from API
                    await API.communicate(
                        `${APIEndpoints.packets.base}/${APIEndpoints.packets.type.auto}/${domainData["related_Packet"]}`,
                        (err, localRes) => {
                            let packetData = Array();
                            if (!err) packetData = localRes;
                            else API.communicate(`${APIEndpoints.packets.base}/${APIEndpoints.packets.type.manual}/${domainData["related_Packet"]}`, (err, res) => {
                                if (!err) packetData = res;
                            });
                            skeleton.category = packetData["category"];
                            skeleton.method = packetData["requestType"];

                            // Push data(s) to localDataPack
                            localDataPack.push(skeleton);

                            // Push data to callback when job done.
                            if (counter++ + 1 === res.length) {
                                console.info(`${this.className}.syncData() : Loaded ${localDataPack.length} rows.`);
                                callback(localDataPack);
                            }
                        });
                });
            }
        )
    }

    buildTable(dataPackage) {
        let builder = new tableBuilder(),
            table = {
                ID: createKey(),
                place: document.getElementById("tablePlace"),
                elements: {
                    table: document.createElement("table"),
                    tbody: document.createElement("tbody")
                }
            },
            currentState = keyAndStrings[Number(stateHandler.isVector)];

        // Update title bar string and
        document.getElementById("pageTitle").innerHTML = currentState.viewString;
        document.title = `${currentState.viewString} - BWASP`;

        // Initialize tablePlace DIV
        table.place.innerHTML = "";

        // Toggle loading screen
        document.getElementById("loadingProgress").classList.remove("d-none");
        document.getElementById("resultNoData").classList.add("d-none");

        // Set default table classes
        table.elements.table.classList.add("table", "table-hover");

        dataPackage.forEach((dataSet) => {
            let rowElement = {
                    parent: document.createElement("tr"),
                    child: {
                        category: document.createElement("th"),
                        URL: document.createElement("td"),
                        action: {
                            parent: document.createElement("td"),
                            target: document.createElement("p"),
                            method: document.createElement("p")
                        },
                        params: document.createElement("td"),
                        doubt: document.createElement("td"),
                        method: {
                            parent: document.createElement("td"),
                            method: document.createElement("span")
                        },
                        impact: {
                            parent: document.createElement("td"),
                            rate: document.createElement("span")
                        }
                    },
                    lineBreak: document.createElement("br")
                },
                impactRate = [["success", "Low"], ["warning", "Normal"], ["danger", "High"]];

            // Build category
            rowElement.child.category.innerText = (dataSet.category === 0)
                ? "Auto"
                : "Manual";
            rowElement.child.category.classList.add("text-muted", "text-center", "small");
            rowElement.parent.appendChild(rowElement.child.category);

            // Build URL
            rowElement.child.URL.innerText = dataSet.url.url + dataSet.url.uri;
            // rowElement.child.URL.classList.add("text-break");
            rowElement.parent.appendChild(rowElement.child.URL);

            // Build action if present
            if (dataSet.action.target.length !== 0) {
                rowElement.child.action.method.innerText = dataSet.action.type[0];
                rowElement.child.action.target.innerText = dataSet.action.target[0];

                rowElement.child.action.method.classList.add("badge", "bg-success", "text-uppercase", "me-2", "mb-1");
                rowElement.child.action.target.classList.add("mb-0");

                rowElement.child.action.parent.append(
                    rowElement.child.action.method,
                    rowElement.child.action.target
                );
                rowElement.parent.appendChild(rowElement.child.action.parent);
            } else {
                rowElement.parent.appendChild(builder.dataNotPresent());
            }

            // Build params if present
            let paramSet = Array();
            dataSet.params.forEach((param) => {
                if (param !== "") {
                    if (param.includes("=")) param = param.split("=")[0];
                    paramSet.push(param);
                }
            });

            if (paramSet.length !== 0) {
                paramSet.forEach((param) => {
                    let codeElement = document.createElement("code");
                    codeElement.innerText = param;
                    rowElement.child.params.appendChild(codeElement);
                    if (paramSet[paramSet.length - 1] !== param) rowElement.child.params.appendChild(builder.commaAsElement());
                })
                rowElement.parent.appendChild(rowElement.child.params);
            } else {
                rowElement.parent.appendChild(builder.dataNotPresent());
            }

            // Build vulnerability doubt
            paramSet = Object.keys(dataSet.vulnerability.type);
            paramSet.forEach((param) => {
                let codeElement = document.createElement("code");
                codeElement.innerText = param;
                rowElement.child.doubt.appendChild(codeElement);
                if (paramSet[paramSet.length - 1] !== param) rowElement.child.doubt.appendChild(builder.commaAsElement());
            })
            rowElement.parent.appendChild(rowElement.child.doubt);

            // Build Method
            rowElement.child.method.method.innerText = dataSet.method;
            rowElement.child.method.method.classList.add("badge", "bg-success");
            rowElement.child.method.parent.appendChild(rowElement.child.method.method);
            rowElement.parent.appendChild(rowElement.child.method.parent);

            // Build Impact

            rowElement.child.impact.rate.innerText = impactRate[dataSet.impactRate][1];
            rowElement.child.impact.rate.classList.add("badge", "rounded-pill", `bg-${impactRate[dataSet.impactRate][0]}`, "small")
            rowElement.child.impact.parent.appendChild(rowElement.child.impact.rate);
            rowElement.parent.appendChild(rowElement.child.impact.parent);

            // Add current row to main tbody
            table.elements.tbody.append(rowElement.parent);
            console.log(dataSet);
        });
        // Build table element
        table.elements.table.append(
            builder.buildHead(elements[currentState.type]),
            table.elements.tbody
        )

        // Finalize jobs
        table.place.appendChild(table.elements.table);
        document.getElementById("loadingProgress").classList.add("d-none");
        document.getElementById("tablePlace").classList.remove("d-none");
    }

    getRowCount() {
        API.communicate(
            "/api/domain/count",
            (err, res) => {
                console.log(res);
            });
    }

}

let pager = new pagerTools();

window.onload = () => {
    let userHelpModal = new bootstrap.Modal(document.getElementById('helpModal'), {
        show: true
    });
    pager.buildPage().then(() => console.log(`Called data handlers`));
    document.getElementById("openHelpModal").addEventListener("click", () => userHelpModal.toggle());
    document.getElementById("switchToPacket").click();
};