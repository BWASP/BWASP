// Get modules
import {API as api, createKey, tableBuilder} from '../jHelperModule.js';

// Specified query selectors
let places = {
    detailView: {
        modal: document.getElementById("detailViewModal"),
        container: document.getElementById("detailViewModalContainer"),
        view: document.getElementById("detailViewModalContentView")
    },
    help: {
        modal: document.getElementById('helpModal')
    },
    viewEngine: {
        modal: document.getElementById("viewEnginePrefModal")
    }
};

// Modals
let modals = {
    viewEngine: new bootstrap.Modal(places.viewEngine.modal, {
        keyboard: false,
        backdrop: 'static',
        show: true
    }),
    userHelp: new bootstrap.Modal(places.help.modal, {
        show: true
    }),
    detailView: new bootstrap.Modal(places.detailView.modal, {
        show: true
    })
};

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
};

// Other frontend rendering option / values
const elements = {
        vectors: ["Type", "URL", "Action", "Params", "Threat", "Method", "Impact"],
        packets: []
    },
    coloring = {
        post: "bg-primary",
        get: "bg-success"
    },
    impactRate = [["success", "Low"], ["warning", "Normal"], ["danger", "High"]];

// State Handler
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
    isModalFullscreen = false

// Helper functions
let returnError = (errorMessage = ["No data", ""]) => {
    let condition = {
        isFromHelper: Array.isArray(errorMessage),
        isString: (typeof (errorMessage) !== "string")
    };

    // Flexible data reactor
    let messages = [
        (condition.isFromHelper)
            ? errorMessage.name
            : (condition.isString)
                ? errorMessage[0]
                : errorMessage,
        (condition.isFromHelper)
            ? errorMessage.message
            : (condition.isString)
                ? errorMessage[1]
                : "",
    ];

    document.getElementById("errMsgTitle").innerText = messages[0];
    document.getElementById("errMsgDesc").innerText = messages[1];
    document.getElementById("loadingProgress").classList.add("d-none");
    document.getElementById("resultNoData").classList.remove("d-none");

    // Will be removed in future commits.
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
        };
        this.directories = Object();
    }

    async updateRowCount() {
        await this.getRowCount((rowCount) => {
            let maxPageCount = (Math.round(rowCount / this.paging.rowPerPage)),
                formattedRowCount = rowCount.toLocaleString();

            console.log(
                "Row count: ", rowCount,
                "\nMax page: ", maxPageCount,
                "\nRow count: ", this.data.rowCount,
                "\nCurrent page: ", this.paging.currentPage
            );

            // Set current rowPerPage value
            document.getElementById("viewPref-modal-rowPerPage").innerText = (this.paging.rowPerPage > rowCount)
                ? rowCount
                : this.paging.rowPerPage;
            document.getElementById("viewPref-input-rowPerPage").max = rowCount;
            document.getElementById("viewPref-input-rowPerPage").value = this.paging.rowPerPage;


            document.getElementById("viewPref-modal-allRowCount").innerText = formattedRowCount;
            document.getElementById("viewPref-input-currentPage").value = this.paging.currentPage;
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

    openPagingOption() {
        this.updateRowCount().then(() => {
            modals.viewEngine.show();
        });
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
        modals.viewEngine.hide();
    }

    async syncData(requestPage, rowPerPage, callback) {
        let localDataPack = [],
            counter = Number(),
            pages = {
                from: ((requestPage - 1) * rowPerPage) + 1,
                count: rowPerPage
            };

        await API.communicate(
            APIEndpoints.vectors + `/${pages.from}/${pages.count}`,
            (err, res) => {
                if (err) return returnError(err);
                if (res.length === 0) return returnError("No data");

                res.forEach(async (domainData) => {
                    let skeleton = {
                        id: domainData["id"],
                        category: Number(),
                        url: {
                            url: domainData["URL"],
                            uri: domainData["URI"]
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

                    // Base64 Decryption
                    Object.keys(skeleton.action).forEach((currentKey) => {
                        for (let counter = 0; counter <= skeleton.action[currentKey].length - 1; counter++) {
                            skeleton.action[currentKey][counter] = atob(skeleton.action[currentKey][counter]);
                        }
                    })

                    for (let counter = 0; counter <= skeleton.details.tag.length - 1; counter++) {
                        skeleton.details.tag[counter] = atob(skeleton.details.tag[counter]);
                    }

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
                    threat: document.createElement("td"),
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
            };

            // Build category
            rowElement.child.category.innerText = (dataSet.category === 0)
                ? "Auto"
                : "Manual";
            rowElement.child.category.classList.add("text-muted", "text-center", "small");
            rowElement.parent.appendChild(rowElement.child.category);

            // Build URL
            rowElement.child.URL.innerText = dataSet.url.url + dataSet.url.uri;
            rowElement.child.URL.classList.add("text-break");
            // rowElement.child.URL.classList.add("text-break");
            rowElement.parent.appendChild(rowElement.child.URL);

            // Build action if present
            if (dataSet.action.target.length !== 0) {
                for (let rowNum = 0; rowNum <= dataSet.action.target.length - 1; rowNum++) {
                    let localSkeleton = {
                        parent: document.createElement("div"),
                        target: document.createElement("p"),
                        method: document.createElement("p")
                    }
                    localSkeleton.method.innerText = dataSet.action.type[rowNum];
                    localSkeleton.target.innerText = dataSet.action.target[rowNum];

                    localSkeleton.parent.classList.add("mt-1", "mb-1");
                    localSkeleton.method.classList.add("badge", coloring[dataSet.action.type[rowNum].toLowerCase()], "text-uppercase", "me-2", "mb-1");
                    localSkeleton.target.classList.add("mb-0", "text-break");

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
            rowElement.child.threat.classList.add("text-center");
            paramSet.forEach((param) => {
                let codeElement = document.createElement("code");
                codeElement.innerText = param;
                rowElement.child.threat.appendChild(codeElement);
                if (paramSet[paramSet.length - 1] !== param) rowElement.child.threat.appendChild(builder.commaAsElement());
            })
            rowElement.parent.appendChild((paramSet.length !== 0)
                ? rowElement.child.threat
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

            // Add event listener for each line
            rowElement.parent.addEventListener("click", () => openDetailsModal(dataSet));

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
                this.data.rowCount = res.count;
                callback(Number(res.count));
            });
    }

}

let pager = new pagerTools();
let referredDocuments = Object();

const openDetailsModal = (dataSet) => {
    /**
     * Build Violation section for details modal
     * @param dataPackage
     */
    const buildViolationElement = async (dataPackage) => {
        let guideline = Object(),
            viewArea = document.getElementById("violationViewArea"),
            packageKeys = Object.keys(dataPackage);

        // Load guideline
        await fetch("/datasets/documents/kisa.json")
            .then(blob => blob.json())
            .then(res => guideline = res);

        // Clear HTML Area
        if (packageKeys.length > 0) viewArea.innerHTML = "";

        // Create skeleton
        let skeleton = {
            parent: document.createElement("section"),
            documentName: document.createElement("h5")
        }
        skeleton.documentName.classList.add("fw-bolder", "mb-3");
        skeleton.documentName.innerText = `[${guideline.document.fileType.toUpperCase()}, ${guideline.document.released}] ${guideline.document.name}`;

        skeleton.parent.appendChild(skeleton.documentName);

        packageKeys.forEach((currentElement) => {
            let localSkeleton = {
                    parent: document.createElement("div"),
                    flex: document.createElement("div"),
                    child: {
                        message: document.createElement("p"),
                        page: document.createElement("p"),
                        quote: document.createElement("p")
                    }
                },
                currentGuideline = guideline.detect[currentElement];

            localSkeleton.parent.classList.add("m-3", "p-3", "rounded-custom", "shadow");
            localSkeleton.flex.classList.add("d-flex");
            localSkeleton.child.message.classList.add("mb-0", "fw-bold");
            localSkeleton.child.page.classList.add("mb-0", "text-muted", "ms-auto", "small");
            localSkeleton.child.quote.classList.add("small", "text-muted", "mb-0");

            localSkeleton.child.message.innerText = currentGuideline.message;
            localSkeleton.child.page.innerText = `P. ${currentGuideline.relatedPage}`;
            localSkeleton.child.quote.innerText = currentGuideline.quote;

            localSkeleton.flex.append(
                localSkeleton.child.message,
                localSkeleton.child.page
            );

            localSkeleton.parent.append(
                localSkeleton.flex,
                localSkeleton.child.quote
            );

            skeleton.parent.appendChild(localSkeleton.parent);
        })

        viewArea.appendChild(skeleton.parent);
    };

    const buildReferredDocs = async (target, types = String()) => {
        let overallDocuments = Array(),
            viewArea = document.getElementById("referredDocumentViewArea");
        if (Object.keys(referredDocuments).length === 0) {
            await fetch("/static/data/referredDocuments.json")
                .then(blob => blob.json())
                .then(res => referredDocuments = res);
        }
        if (typeof (referredDocuments[target]) === "undefined") return;
        if (!Array.isArray(referredDocuments[target])) {
            let typeCategory = Object.keys(referredDocuments[target]);
            let localDataSet = referredDocuments[target][(types !== String())
                ? types
                : "Generic"];
            localDataSet.forEach((currentValue) => overallDocuments.push(currentValue));
        } else referredDocuments[target].forEach((currentValue) => overallDocuments.push(currentValue));

        overallDocuments.forEach((currentDocument) => {
            let localSkeleton = {
                parent: document.createElement("li"),
                innerLink: document.createElement("a")
            };
            localSkeleton.innerLink.classList.add("text-decoration-none");
            localSkeleton.innerLink.href = currentDocument.link;
            localSkeleton.innerLink.target = "_BLANK";
            localSkeleton.innerLink.innerHTML = `${currentDocument["name"]} - ${currentDocument["author"]}`;
            localSkeleton.parent.appendChild(localSkeleton.innerLink);
            viewArea.appendChild(localSkeleton.parent);
        });
    }

    let dataKind = ["cookie", "queryString", "tag"],
        modalElements = Object();

    places.detailView.view.className = "";
    places.detailView.view.classList.add("modal-content", "p-4", "border-rounded", "shadow");


    // Initialize table elements
    dataKind.forEach((currentKind) => {
        modalElements[currentKind] = {
            noData: document.getElementById(`detail-${currentKind}`),
            dataPlace: document.getElementById(`detail-${currentKind}-data`),
            tablePlace: document.getElementById(`tablePlace-${currentKind}`)
        }
        modalElements[currentKind].noData.classList.add("d-none");
        modalElements[currentKind].dataPlace.classList.add("d-none");
        modalElements[currentKind].tablePlace.innerHTML = "";
    })

    // Set current row ID
    document.getElementById("currentRowID").innerText = dataSet.id;

    // Set each value - impact
    let modalDataElement = {
        impact: document.getElementById("detail-impact"),
        threat: document.getElementById("detail-threat"),
        url: {
            method: document.getElementById("detail-method"),
            url: document.getElementById("detail-URL"),
            uri: document.getElementById("detail-URI"),
        },
        actions: document.getElementById("detail-actions")
    };

    // Impact rate
    modalDataElement.impact.className = "";
    modalDataElement.impact.classList.add("badge", "rounded-pill", "small", `bg-${impactRate[dataSet.impactRate][0]}`);
    modalDataElement.impact.innerText = impactRate[dataSet.impactRate][1];

    // Threats
    modalDataElement.threat.innerText = "";
    let doubtList = Object.keys(dataSet.vulnerability.type["doubt"]);
    document.getElementById("referredDocumentViewArea").innerHTML = "";
    if (doubtList.length > 0) {
        doubtList.forEach((currentThreat) => {
            buildReferredDocs(currentThreat);
            modalDataElement.threat.innerText +=
                currentThreat.concat(
                    (doubtList[doubtList.length - 1] !== currentThreat) ? ", " : ""
                );
        });
    } else {
        modalDataElement.threat.innerText = "-";
    }

    // URL
    modalDataElement.url.url.innerText = dataSet.url.url;
    modalDataElement.url.uri.innerText = dataSet.url.uri;
    modalDataElement.url.method.innerText = dataSet.method.toUpperCase();

    // Actions
    modalDataElement.actions.innerHTML = " - ";
    if (dataSet.action.target.length > 0) {
        modalDataElement.actions.innerHTML = "";
        for (let currentRow = 0; currentRow <= dataSet.action.target.length - 1; currentRow++) {
            let localSkeleton = {
                parent: document.createElement("p"),
                method: document.createElement("span"),
                target: document.createElement("span")
            }
            localSkeleton.method.classList.add("badge", "text-uppercase", "me-2", "mb-1",
                (typeof (coloring[dataSet.action.type[currentRow].toLowerCase()]) === "undefined")
                    ? "bg-warning"
                    : coloring[dataSet.action.type[currentRow].toLowerCase()]);
            localSkeleton.target.classList.add("text-break");

            localSkeleton.method.innerText = dataSet.action.type[currentRow];
            localSkeleton.target.innerText = dataSet.action.target[currentRow];
            localSkeleton.parent.append(
                localSkeleton.method,
                localSkeleton.target
            );
            modalDataElement.actions.appendChild(localSkeleton.parent);
        }
    } else {
        dataSet.action.innerHTML = " - ";
    }


    // Create cookie view
    [dataKind[0], dataKind[1]].forEach((currentKind) => {
        Object.keys(dataSet.details[currentKind]).forEach((currentData) => {
            let localSkeleton = {
                parent: document.createElement("tr"),
                key: document.createElement("th"),
                value: {
                    parent: document.createElement("td"),
                    value: document.createElement("code")
                }
            };
            localSkeleton.key.innerText = currentData;
            localSkeleton.value.value.innerText = dataSet.details[currentKind][currentData];
            localSkeleton.value.parent.appendChild(localSkeleton.value.value);

            localSkeleton.key.classList.add("text-break");
            localSkeleton.value.parent.classList.add("text-break");

            localSkeleton.parent.append(
                localSkeleton.key,
                localSkeleton.value.parent
            );
            modalElements[currentKind].tablePlace.appendChild(localSkeleton.parent);
        })
        if (Object.keys(dataSet.details[currentKind]).length !== 0) modalElements[currentKind].dataPlace.classList.remove("d-none");
        else modalElements[currentKind].noData.classList.remove("d-none");
    })

    if (dataSet.details[dataKind[2]].length !== 0) {
        dataSet.details[dataKind[2]].forEach((currentTag) => {
            let localSkeleton = {
                pre: document.createElement("pre"),
                code: document.createElement("code")
            };
            localSkeleton.code.classList.add("language-html");
            localSkeleton.code.innerText = currentTag;
            localSkeleton.pre.appendChild(localSkeleton.code);

            modalElements[dataKind[2]].tablePlace.appendChild(localSkeleton.pre);
        })
        modalElements[dataKind[2]].dataPlace.classList.remove("d-none");
    } else modalElements[dataKind[2]].noData.classList.remove("d-none");

    if (Object.keys(dataSet.vulnerability.type["misc"]).length > 0) {
        buildViolationElement(dataSet.vulnerability.type["misc"]);
    }

    hljs.highlightAll();
    modals.detailView.show();

    console.log(dataSet);
}

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

document.getElementById("toggleDetailViewModalSize").addEventListener("click", () => {
    let toggleKeywords = ["remove", "add"];
    document.getElementById("togglerIcon").className
        = `fas fa-${(isModalFullscreen) ? "expand" : "compress"}-alt`;
    places.detailView.container.classList[toggleKeywords[Number(isModalFullscreen)]]("modal-lg");
    places.detailView.container.classList[toggleKeywords[Number(!isModalFullscreen)]]("modal-fullscreen");
    isModalFullscreen = !isModalFullscreen;
})

window.onload = () => {
    pager.buildPage().then(() => {
        document.getElementById("openHelpModal").addEventListener("click", () => modals.userHelp.toggle());
        // document.getElementById("viewPref-input-rowPerPage").value = 12;
        console.log("rowPerPage", document.getElementById("viewPref-input-rowPerPage").value, pager.paging.rowPerPage);
    })
};