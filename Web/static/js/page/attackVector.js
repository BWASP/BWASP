// Get modules
import {API as api, createKey, tableBuilder} from '../jHelper.js';

// Define Modals
let viewEnginePrefModal = new bootstrap.Modal(document.getElementById("viewEnginePrefModal"), {
    keyboard: false,
    backdrop: 'static',
    show: true
});
let userHelpModal = new bootstrap.Modal(document.getElementById('helpModal'), {
    show: true
});

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
        vectors: ["Category", "URL", "Action", "Params", "Threat", "Method", "Impact"],
        packets: []
    },
    coloring = {
        post: "bg-primary",
        get: "bg-success"
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
    returnError = (errorMessage = ["No data", ""]) => {
        let condition = (typeof (errorMessage) !== "string");
        console.log(errorMessage, typeof (errorMessage), condition);
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
let API = await new api();

class pagerTools {
    constructor() {
        this.className = "pagerTools";
        this.API = new api();
        this.paging = {
            currentPage: 1,
            rowPerPage: 10
        };
        this.data = {
            rowCount: Number(),
            pageCount: 1
        }
    }

    buildPaginationButton() {

    }

    async updateRowCount() {
        await this.getRowCount((rowCount) => {
            let maxPageCount = (Math.round(rowCount / this.paging.rowPerPage)).toLocaleString(),
                formattedRowCount = rowCount.toLocaleString();
            console.log(rowCount, maxPageCount, this.data.rowCount);
            document.getElementById("viewPref-modal-allRowCount").innerText = formattedRowCount;
            console.log(maxPageCount);
            document.getElementById("viewPref-input-rowPerPage").max = rowCount;
            document.getElementById("viewPref-input-rowPerPage").value = this.paging.rowPerPage;
            document.getElementById("viewPref-input-currentPage").value = this.paging.currentPage;
            console.log("Current page: ", this.paging.currentPage);
            this.updateMaxPage();
        });
        return true;
    }

    updateMaxPage() {
        this.data.pageCount = Math.round(this.data.rowCount / this.paging.rowPerPage);
        console.log("Page: ", this.data.pageCount);
        this.data.pageCount += (this.data.rowCount % document.getElementById("viewPref-input-rowPerPage").value === 0) ? 0 : 1;
        document.getElementById("viewPref-modal-pageCount").innerText = String(this.data.pageCount);
        document.getElementById("viewPref-input-currentPage").max = this.data.pageCount;
        document.getElementById("viewPref-input-currentPage").value = this.paging.currentPage;
        document.getElementById("viewPref-modal-currentPage").innerText = this.paging.currentPage;
    }

    async openPagingOption() {
        await this.updateRowCount();
        viewEnginePrefModal.show();
    }


    toggleLoader(type) {
        document.getElementById("loadingProgress").classList[(type) ? "add" : "remove"]("d-none");
    }

    updatePager(page = this.paging.currentPage, rowCount = this.paging.rowPerPage) {
        this.paging = {
            currentPage: page,
            rowPerPage: rowCount
        };
        this.buildPage().then(() => {
            console.info("updatePager() : Called buildPage()");
        });
    }

    async buildPage() {
        // Add loading
        document.getElementById("loadingProgress").classList.remove("d-none");
        document.getElementById("tablePlace").classList.add("d-none");
        document.getElementById("tablePlaceHolder").classList.add("d-none");

        // Update value
        document.getElementById("rowPerPage").innerText = this.paging.rowPerPage;

        // Do job
        await this.syncData(this.paging.currentPage, this.paging.rowPerPage, this.buildTable);
        viewEnginePrefModal.hide();
    }

    async syncData(requestPage, rowPerPage, callback) {
        let localDataPack = [],
            counter = Number();
        await API.communicate(
            APIEndpoints.vectors + `/${((requestPage - 1) * rowPerPage) + 1}/${rowPerPage}`,
            (err, res) => {
                if (err) {
                    let redoJob = window.setTimeout(() => {
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
                        impactRate: domainData["impactRate"],
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
                holder: document.getElementById("tablePlaceHolder"),
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
                for(let rowNum=0; rowNum<=dataSet.action.target.length-1; rowNum++) {
                    let localSkeleton = {
                        parent: document.createElement("div"),
                        target : document.createElement("p"),
                        method : document.createElement("p")
                    }
                    localSkeleton.method.innerText = dataSet.action.type[rowNum];
                    localSkeleton.target.innerText = dataSet.action.target[rowNum];

                    localSkeleton.parent.classList.add("mt-1", "mb-1");
                    localSkeleton.method.classList.add("badge", coloring[dataSet.action.type[0].toLowerCase()], "text-uppercase", "me-2", "mb-1");
                    localSkeleton.target.classList.add("mb-0");

                    localSkeleton.parent.append(
                        localSkeleton.method,
                        localSkeleton.target
                    )
                    rowElement.child.action.parent.appendChild(localSkeleton.parent);
                }
                rowElement.parent.appendChild(rowElement.child.action.parent);
            } else {
                rowElement.parent.appendChild(builder.dataNotPresent());
            }

            // Build params if present
            let paramSet = Array();
            rowElement.child.params.classList.add("text-center");
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
            paramSet = Object.keys(dataSet.vulnerability.type.doubt);
            rowElement.child.doubt.classList.add("text-center");
            paramSet.forEach((param) => {
                let codeElement = document.createElement("code");
                codeElement.innerText = param;
                rowElement.child.doubt.appendChild(codeElement);
                if (paramSet[paramSet.length - 1] !== param) rowElement.child.doubt.appendChild(builder.commaAsElement());
            })
            rowElement.parent.appendChild((paramSet.length !== 0)
                ? rowElement.child.doubt
                : builder.dataNotPresent()
            );

            // Build Method
            rowElement.child.method.method.innerText = dataSet.method;
            rowElement.child.method.method.classList.add("badge", "bg-success");
            rowElement.child.method.parent.classList.add("text-center");
            rowElement.child.method.parent.appendChild(rowElement.child.method.method);
            rowElement.parent.appendChild(rowElement.child.method.parent);

            // Build Impact
            rowElement.child.impact.rate.innerText = impactRate[dataSet.impactRate][1];
            rowElement.child.impact.rate.classList.add("badge", "rounded-pill", `bg-${impactRate[dataSet.impactRate][0]}`, "small");
            rowElement.child.impact.parent.classList.add("text-center");
            rowElement.child.impact.parent.appendChild(rowElement.child.impact.rate);
            rowElement.parent.appendChild(rowElement.child.impact.parent);

            // Add current row to main tbody
            table.elements.tbody.append(rowElement.parent);
            // console.log(dataSet);
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
        document.getElementById("tablePlaceHolder").classList.remove("d-none");
    }

    async getRowCount(callback) {
        await API.communicate(
            "/api/domain/count",
            (err, res) => {
                console.log(res);
                this.data.rowCount = res.RowCount;
                callback(Number(res.RowCount));
            });
    }

}

let pager = new pagerTools();

document.getElementById("openPrefModal").addEventListener("click", () => pager.openPagingOption());

document.getElementById("viewPref-input-rowPerPage").addEventListener("change", function () {
    document.getElementById("viewPref-modal-rowPerPage").innerText = this.value;
    pager.paging.rowPerPage = Number(this.value);
    pager.updateMaxPage();
})

document.getElementById("viewPref-input-currentPage").addEventListener("change", function () {
    document.getElementById("viewPref-modal-currentPage").innerText = this.value;
    pager.paging.currentPage = this.value;
})

document.getElementById("viewPref-button-save").addEventListener("click", () => pager.buildPage());

window.onload = () => {
    pager.buildPage().then(() => {
        document.getElementById("openHelpModal").addEventListener("click", () => userHelpModal.toggle());
        // document.getElementById("viewPref-input-rowPerPage").value = 12;
        console.log("rowPerPage", document.getElementById("viewPref-input-rowPerPage").value, pager.paging.rowPerPage);
    })
};