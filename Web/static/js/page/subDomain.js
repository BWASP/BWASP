// Get modules
import {
    API as api,
    createKey,
    createToast,
    swapElement,
    dataSlicer,
    tableBuilder as TBuilder,
    elementBuilder as EBuilder
} from '../jHelper.js';

let tableBuilder = new TBuilder();
let elementBuilder = new EBuilder();

// Specified query selectors
let places = {
    detailView: {
        // modal: document.getElementById("detailViewModal"),
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
    })
};

// Define API Endpoints
const APIEndpoints = {
    subDomain: "/api/systeminfo",
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
        vectors: ["Type", "Sub Domain"],
        packets: []
    },
    coloring = {
        none: "bg-danger",
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
            viewString: "Sub Domains"
        }
    ],
    isModalFullscreen = false

// define api communicator
let API = await new api();

// Modal toggler
const toggleModalSize = (fixed = null) => {
    if (typeof (fixed) === "boolean") isModalFullscreen = fixed;
    let toggleKeywords = ["remove", "add"];
    document.getElementById("togglerIcon").className = `fas fa-${(isModalFullscreen) ? "expand" : "compress"}-alt`;
    places.detailView.container.classList[toggleKeywords[Number(isModalFullscreen)]]("modal-lg");
    places.detailView.container.classList[toggleKeywords[Number(!isModalFullscreen)]]("modal-fullscreen");
    isModalFullscreen = !isModalFullscreen;
}

class pagerTools {
    constructor() {
        this.builder = new TBuilder();
        this.className = "pagerTools";
        this.maxLength = 50;
        this.API = new api();
        this.syncedData = {
            packets: Object()
        };
        this.dataSet = Array();
        this.paging = {
            currentPage: 1,
            rowPerPage: 10
        };
        this.data = {
            rowCount: Number(),
            pageCount: 1
        };
        this.error = false;
        this.directories = Object();
    }

    // Helper functions
    returnError(errorMessage = ["No data", ""]) {
        this.error = true;
        let condition = {
            isFromHelper: typeof (errorMessage) === "object",
            isLocal: Array.isArray(errorMessage),
            isString: (typeof (errorMessage) !== "string")
        };

        // Flexible data reactor
        let messages = [
            (condition.isFromHelper)
                ? errorMessage.name
                : (condition.isLocal)
                    ? errorMessage[0]
                    : errorMessage,
            (condition.isFromHelper)
                ? errorMessage.message
                : (condition.isLocal)
                    ? errorMessage[1]
                    : "",
        ];

        document.getElementById("tablePlaceHolder").classList.add("d-none");
        document.getElementById("errMsgTitle").innerText = messages[0];
        document.getElementById("errMsgDesc").innerText = messages[1];
        document.getElementById("loadingProgress").classList.add("d-none");
        document.getElementById("resultNoData").classList.remove("d-none");

        // Will be removed in future commits.
        console.error(`:: ERROR :: `, errorMessage);
    };

    // async updateRowCount() {
    //     let countRes = await API.communicate("/api/domain/count");
    //     this.data.rowCount = Number(countRes.count);
    //
    //     let maxPageCount = (Math.round(this.data.rowCount / this.paging.rowPerPage)),
    //         formattedRowCount = this.data.rowCount.toLocaleString();
    //
    //     console.log(
    //         "Row count: ", this.data.rowCount,
    //         "\nMax page: ", maxPageCount,
    //         "\nRow count: ", this.data.rowCount,
    //         "\nCurrent page: ", this.paging.currentPage
    //     );
    //
    //     // Set current rowPerPage value
    //     document.getElementById("viewPref-modal-rowPerPage").innerText = (this.paging.rowPerPage > this.data.rowCount)
    //         ? this.data.rowCount
    //         : this.paging.rowPerPage;
    //     document.getElementById("viewPref-input-rowPerPage").max = this.data.rowCount;
    //     document.getElementById("viewPref-input-rowPerPage").value = this.paging.rowPerPage;
    //
    //
    //     document.getElementById("viewPref-modal-allRowCount").innerText = formattedRowCount;
    //     document.getElementById("viewPref-input-currentPage").value = this.paging.currentPage;
    //     this.updateMaxPage();
    //     return true;
    // }

    updateMaxPage() {
        this.data.pageCount = Math.round(this.data.rowCount / this.paging.rowPerPage);
        console.log("Page: ", this.data.pageCount);
        this.data.pageCount += (this.data.rowCount % document.getElementById("viewPref-input-rowPerPage").value === 0) ? 0 : 1;
        document.getElementById("viewPref-modal-pageCount").innerText = String(this.data.pageCount);
        document.getElementById("viewPref-input-currentPage").max = this.data.pageCount;
        document.getElementById("viewPref-input-currentPage").value = this.paging.currentPage;
        document.getElementById("viewPref-modal-currentPage").innerText = this.paging.currentPage;
    }

    // openPagingOption() {
    //     this.updateRowCount().then(() => {
    //         modals.viewEngine.show();
    //     });
    // }


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

        // Receive data from API
        await this.syncData();

        // Return if has error
        if (this.error) return;

        // Update value
        document.getElementById("rowPerPage").innerText = String(this.dataSet.length);

        // Build table and hide modal
        this.buildTable();
        modals.viewEngine.hide();
    }

    async syncData() {

        this.dataSet = Array();
        try {
            await API.communicate(`${APIEndpoints.subDomain}`)
        } catch (e) {
            return this.returnError(e);
        }

        let vectors = await API.communicate(`${APIEndpoints.subDomain}`),
            malformedID = {
                subDomain: ["subDomain"]
            };

        // If no data present
        if (vectors.length === 0) return this.returnError("No data");
        else for (const vector of vectors) {
            // Parse attack vector
            vector.subDomain = JSON.parse(vector.subDomain);

            // Fix malformed JSON
            malformedID.subDomain.forEach((id) => {
                // Check if scans recursively
                let recursive = id.includes("/");
                if (recursive) id = id.replaceAll("/", "");

                // Handle data to jsonDataHandler
                vector[id] = API.jsonDataHandler(vector[id]);

                // Recursive Handler
                if (recursive) {
                    Object.keys(vector[id]).forEach((key) => {
                        if (typeof (vector[id][key]) === "string") {
                            vector[id][key] = API.jsonDataHandler(vector[id][key]);
                        }
                    })
                }
            });


            this.dataSet.push({
                subDomain: vector
            })
        }

        return this.dataSet;
    }

    buildTable() {
        let table = {
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

        this.dataSet.forEach((dataSet) => {
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
            rowElement.child.category.innerText = (dataSet.packet.category === 0)
                ? "Auto"
                : "Manual";
            rowElement.child.category.classList.add("text-muted", "text-center", "small");
            rowElement.parent.appendChild(rowElement.child.category);

            // Build URL
            rowElement.child.URL.innerText = dataSlicer(dataSet.vector.URL + dataSet.vector.URI, this.maxLength);
            rowElement.child.URL.classList.add("text-break");
            // rowElement.child.URL.classList.add("text-break");
            rowElement.parent.appendChild(rowElement.child.URL);

            // Build action if present
            if (dataSet.vector.action_URL.length !== 0) {
                for (let rowNum = 0; rowNum <= dataSet.vector.action_URL.length - 1; rowNum++) {
                    if (dataSet.vector.action_URL[rowNum] !== "") {
                        let localSkeleton = {
                                parent: document.createElement("div"),
                                target: document.createElement("p"),
                                method: document.createElement("p")
                            },
                            methodType = dataSet.vector.action_URL_Type[rowNum];

                        if (methodType === undefined) methodType = "None";

                        localSkeleton.method.innerText = methodType;
                        localSkeleton.target.innerText = dataSlicer(dataSet.vector.action_URL[rowNum], this.maxLength);

                        localSkeleton.parent.classList.add("mt-1", "mb-1");
                        localSkeleton.method.classList.add("badge", coloring[methodType.toLowerCase()], "text-uppercase", "me-2", "mb-1");
                        localSkeleton.target.classList.add("mb-0", "text-break");

                        localSkeleton.parent.append(
                            localSkeleton.method,
                            localSkeleton.target
                        )
                        rowElement.child.action.parent.appendChild(localSkeleton.parent);
                    }
                }
                rowElement.parent.appendChild(rowElement.child.action.parent);
            } else {
                rowElement.parent.appendChild(this.builder.dataNotPresent());
            }

            // Build params if present
            let paramSet = Array();
            rowElement.child.params.classList.add("text-center");
            dataSet.vector.params.forEach((param) => {
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
                    if (paramSet[paramSet.length - 1] !== param) rowElement.child.params.appendChild(this.builder.commaAsElement());
                })
                rowElement.parent.appendChild(rowElement.child.params);

            } else {
                rowElement.parent.appendChild(this.builder.dataNotPresent());
            }

            // Build vulnerability doubt
            paramSet = Object.keys(dataSet.vector.attackVector.doubt);
            rowElement.child.threat.classList.add("text-center");
            paramSet.forEach((param) => {
                let codeElement = document.createElement("code");
                codeElement.innerText = param;
                rowElement.child.threat.appendChild(codeElement);
                if (paramSet[paramSet.length - 1] !== param) rowElement.child.threat.appendChild(this.builder.commaAsElement());
            })
            rowElement.parent.appendChild((paramSet.length !== 0)
                ? rowElement.child.threat
                : this.builder.dataNotPresent()
            );

            // Build Method
            rowElement.child.method.method.innerText = dataSet.packet.requestType;
            rowElement.child.method.method.classList.add("badge", "bg-success");
            rowElement.child.method.parent.classList.add("text-center");
            rowElement.child.method.parent.appendChild(rowElement.child.method.method);
            rowElement.parent.appendChild(rowElement.child.method.parent);

            // Build Impact
            rowElement.child.impact.rate.innerText = impactRate[dataSet.vector.impactRate][1];
            rowElement.child.impact.rate.classList.add("badge", "rounded-pill", `bg-${impactRate[dataSet.vector.impactRate][0]}`, "small");
            rowElement.child.impact.parent.classList.add("text-center");
            rowElement.child.impact.parent.appendChild(rowElement.child.impact.rate);
            rowElement.parent.appendChild(rowElement.child.impact.parent);

            // Add current row to main tbody
            table.elements.tbody.append(rowElement.parent);

            // Add event listener for each line
            rowElement.parent.addEventListener("click", async () => {
                let modal = new detailsModal({
                    vectors: document.getElementById("detailView-vector"),
                    packets: document.getElementById("detailView-packet")
                });
                await modal.open(dataSet);
                // openDetailsModal(dataSet)
            });

            // console.log(dataSet);
        });
        // Build table element
        table.elements.table.append(
            this.builder.buildHead(elements[currentState.type]),
            table.elements.tbody
        )

        // Finalize jobs
        table.place.appendChild(table.elements.table);
        document.getElementById("loadingProgress").classList.add("d-none");
        document.getElementById("tablePlace").classList.remove("d-none");
        document.getElementById("tablePlaceHolder").classList.remove("d-none");
    }

    createAccordion(title, HTMLObject) {
        let skeleton = {
            parent: document.createElement("div"),
            title: {
                parent: document.createElement("h2"),
                button: document.createElement("button")
            },
            body: {
                parent: document.createElement("div"),
                childBox: document.createElement("div")
            }
        }, elementID = {
            head: createKey(3, "accordion"),
            body: createKey(3, "accordion")
        }

        // Create parent
        skeleton.parent.classList.add("accordion-item");

        // Create head
        skeleton.title.parent.classList.add("accordion-header");
        skeleton.title.parent.id = elementID.head;

        skeleton.title.button.classList.add("accordion-button", "collapsed");
        skeleton.title.button.type = "button";
        skeleton.title.button.setAttribute("data-bs-toggle", "collapse");
        skeleton.title.button.setAttribute("aria-expanded", "false");
        skeleton.title.button.setAttribute("data-bs-target", `#${elementID.body}`);
        skeleton.title.button.setAttribute("aria-controls", elementID.body);
        skeleton.title.button.innerText = title;

        skeleton.title.parent.appendChild(skeleton.title.button);

        // Build body
        skeleton.body.parent.classList.add("accordion-collapse", "collapse");
        skeleton.body.parent.id = elementID.body;
        skeleton.body.parent.setAttribute("aria-labelledby", elementID.head);

        skeleton.body.childBox.classList.add("accordion-body");
        skeleton.body.childBox.append(HTMLObject);

        skeleton.body.parent.appendChild(skeleton.body.childBox);

        // Assembly
        skeleton.parent.append(
            skeleton.title.parent,
            skeleton.body.parent
        );

        return skeleton.parent;
    }
}

let pager = new pagerTools();
let referredDocuments = Object();

// document.getElementById("openPrefModal").addEventListener("click", () => pager.openPagingOption());

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
        document.getElementById("openHelpModal").addEventListener("click", () => modals.userHelp.toggle());
        // document.getElementById("viewPref-input-rowPerPage").value = 12;
        console.log("rowPerPage", document.getElementById("viewPref-input-rowPerPage").value, pager.paging.rowPerPage);
    })
};