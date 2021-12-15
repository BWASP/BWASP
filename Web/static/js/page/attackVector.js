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
            viewString: "Attack Vectors"
        }
    ],
    isModalFullscreen = false

// define api communicator
let API = await new api();

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

    async updateRowCount() {
        let countRes = await API.communicate("/api/domain/count");
        this.data.rowCount = Number(countRes.count);

        let maxPageCount = (Math.round(this.data.rowCount / this.paging.rowPerPage)),
            formattedRowCount = this.data.rowCount.toLocaleString();

        console.log(
            "Row count: ", this.data.rowCount,
            "\nMax page: ", maxPageCount,
            "\nRow count: ", this.data.rowCount,
            "\nCurrent page: ", this.paging.currentPage
        );

        // Set current rowPerPage value
        document.getElementById("viewPref-modal-rowPerPage").innerText = (this.paging.rowPerPage > this.data.rowCount)
            ? this.data.rowCount
            : this.paging.rowPerPage;
        document.getElementById("viewPref-input-rowPerPage").max = this.data.rowCount;
        document.getElementById("viewPref-input-rowPerPage").value = this.paging.rowPerPage;


        document.getElementById("viewPref-modal-allRowCount").innerText = formattedRowCount;
        document.getElementById("viewPref-input-currentPage").value = this.paging.currentPage;
        this.updateMaxPage();
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

        // Receive data from API
        await this.syncData(this.paging.currentPage, this.paging.rowPerPage);

        // Return if has error
        if (this.error) return;

        // Update value
        document.getElementById("rowPerPage").innerText = String(this.dataSet.length);

        // Build table and hide modal
        this.buildTable();
        modals.viewEngine.hide();
    }

    async syncData(requestPage, rowPerPage) {
        let requestPages = {
            from: ((requestPage - 1) * rowPerPage) + 1,
            to: rowPerPage
        }
        this.dataSet = Array();
        try {
            await API.communicate(`${APIEndpoints.vectors}/${requestPages.from}/${requestPages.to}`)
        } catch (e) {
            return this.returnError(e);
        }

        let vectors = await API.communicate(`${APIEndpoints.vectors}/${requestPages.from}/${requestPages.to}`),
            malformedID = {
                vector: ["Details/", "action_URL", "action_URL_Type", "params", "Details"],
                packet: ["requestJson", "responseHeader"]
            };

        // If no data present
        if (vectors.length === 0) return this.returnError("No data");
        else for (const vector of vectors) {
            let packet = Object();

            if (Object.keys(this.syncedData).includes(String(vector["related_Packet"]))) packet = this.syncedData[vector["related_Packet"]];
            else {
                packet = await API.communicate(`${APIEndpoints.packets.base}/${vector["related_Packet"]}`);
                packet = packet[0];
                this.syncedData[vector["related_Packet"]] = packet;
            }

            // Parse attack vector
            vector.attackVector = JSON.parse(vector.attackVector);

            // Fix malformed JSON
            malformedID.vector.forEach((id) => {
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
            malformedID.packet.forEach((id) => packet[id] = API.jsonDataHandler(packet[id]));

            // Base64 Decode
            ["action_URL", "action_URL_Type"].forEach((target) => {
                for (let count = 0; count <= vector[target].length - 1; count++) {
                    vector[target][count] = atob(vector[target][count])
                }
            })
            for (let count = 0; count <= vector.Details.tag.length - 1; count++) {
                vector.Details.tag[count] = atob(vector.Details.tag[count])
            }
            // vector.action_URL_Type.forEach((id) => console.log(vector.action_URL_Type));

            this.dataSet.push({
                vector: vector,
                packet: packet
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

class detailsModal {
    constructor(viewParent) {
        this.viewParent = viewParent;
    }

    async open(dataset) {
        // Initialize
        Object.keys(this.viewParent).forEach(area => this.viewParent[area].innerHTML = "");

        // Set current row ID
        document.getElementById("currentRowID").innerText = dataset.vector.id;

        // Build vectors
        await this.buildToTables(dataset, ["cookie", "Cookies"]);
        await this.buildToTables(dataset, ["queryString", "Query String"]);
        await this.writeVectorValues(dataset);
        if (dataset.vector.Details.tag.length > 0) this.buildTags(dataset);
        if (Object.keys(dataset.vector.attackVector["misc"]).length > 0) await this.buildViolationElement(dataset.vector.attackVector["misc"]);
        if (Object.keys(dataset.vector.attackVector["doubt"]).length > 0) await this.buildReferredDocs(dataset);
        await this.buildDoubt(dataset);
        await this.buildTestOptionResult(dataset);

        // Build Packets
        await this.buildPacketRequest(dataset);
        await this.buildResponseData(dataset);

        // Log dataset
        console.log(dataset);

        // Build
        modals.detailView.show();
    }

    buildTestOptionResult(dataset) {
        let processedData = Object(),
            doubts = dataset.vector.attackVector.doubt,
            virtual = {
                div: document.createElement("div")
            };

        // Processing data
        for (const key of Object.keys(doubts)) {
            let doubt = doubts[key];
            if (doubt.detect === undefined || typeof (doubt.detect) !== "object" || doubt.detect.length <= 0) continue;
            if (processedData[key] === undefined) processedData[key] = Array();

            for (const data of doubt.detect) {
                if (processedData[key][data.type] === undefined) processedData[key][data.type] = Array();
                processedData[key][data.type].push({
                    target: data.url,
                    param: data.param
                })
            }
        }

        // Create view by processed data
        for (const method of Object.keys(processedData)) {
            let methodView = document.createElement("h5");
            methodView.classList.add("mb-3");
            methodView.innerText = method;
            virtual.div.appendChild(methodView);

            for (const type of Object.keys(processedData[method])) {
                let tableDiv = document.createElement("div"),
                    processedParams = Array();

                for (const data of processedData[method][type]) {
                    processedParams = Array();

                    for (const param of Object.keys(data.param)) processedParams.push([
                        {
                            value: param,
                            raw: false
                        },
                        {
                            value: data.param[param],
                            raw: false
                        }
                    ]);

                    let table = tableBuilder.buildTable(
                        ["Key", "Value"],
                        [
                            [
                                {
                                    value: "Target",
                                    raw: false
                                },
                                {
                                    value: data.target,
                                    raw: false
                                }
                            ],
                            [
                                {
                                    value: "Param",
                                    raw: false
                                },
                                {
                                    value: tableBuilder.buildTable(
                                        ["ID", "Value"],
                                        processedParams
                                    ),
                                    raw: true
                                }
                            ]
                        ]
                    )
                    tableDiv.appendChild(table);
                }
                virtual.div.appendChild(
                    pager.createAccordion(type, tableDiv)
                )
            }
        }

        this.viewParent.vectors.appendChild(
            pager.createAccordion("Tested payloads", virtual.div)
        );
    }

    buildResponseData(dataset) {
        let url = dataset.vector.URI.split("?")[0].split("."),
            supportedExt = ["html"];

        this.viewParent.packets.appendChild(
            pager.createAccordion(
                "Response Data",
                elementBuilder.createCode(
                    dataset.packet.responseBody,
                    (supportedExt.includes(url[url.length - 1]))
                        ? url[url.length - 1]
                        : supportedExt[0]
                )
            )
        );
        // elementBuilder.initCode();
    }

    buildPacketRequest(dataset) {
        let headers = [
                {
                    name: "Request Header",
                    data: dataset.packet.requestJson.headers
                },
                {
                    name: "Response Header",
                    data: dataset.packet.responseHeader
                }
            ],
            responseData = Array();

        for (const header of headers) {
            responseData = Array();

            for (const type of Object.keys(header.data)) {
                responseData.push([
                    {
                        value: type,
                        raw: false
                    },
                    {
                        value: header.data[type],
                        raw: false
                    }
                ]);
            }

            this.viewParent.packets.appendChild(
                pager.createAccordion(header.name, tableBuilder.buildTable(
                    ["Key", "Value"],
                    responseData
                ))
            );
        }
    }

    async buildViolationElement(dataPackage) {
        let element = document.createElement("div"),
            packageKeys = Object.keys(dataPackage),
            replacement = {
                code: [["{{", "<code>"], ["}}", "</code>"]]
            },
            guideline = await API.communicate("/static/data/documents/kisa.json", "GET", null, true);

        // Clear HTML Area
        if (packageKeys.length > 0) element.innerHTML = "";

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
            localSkeleton.flex.classList.add("d-flex", "mb-2");
            localSkeleton.child.message.classList.add("mb-0", "fw-bold");
            localSkeleton.child.page.classList.add("mb-0", "text-muted", "ms-auto", "small");
            localSkeleton.child.quote.classList.add("small", "text-muted", "mb-0");


            Object.keys(replacement).forEach(target => {
                replacement[target].forEach((elementTarget) => {
                    currentGuideline.message = currentGuideline.message.replaceAll(elementTarget[0], elementTarget[1]);
                })
            })

            localSkeleton.child.message.innerHTML = currentGuideline.message;
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

        element.appendChild(skeleton.parent);

        this.viewParent.vectors.appendChild(pager.createAccordion("Violation", element));
    }

    buildDoubt(dataset) {
        let doubt = dataset.vector.attackVector["doubt"],
            renderData = Array();

        for (const vuln in doubt) {
            let currentData = [{
                value: vuln,
                raw: false
            }], virtual = {
                div: document.createElement("div"),
                space: Array()
            }
            console.log("vuln: ", vuln, "\nData: ", doubt[vuln]);
            switch (typeof (doubt[vuln])) {
                case "string":
                    currentData.push({
                        value: doubt[vuln],
                        raw: false
                    });
                    break;
                case "object":
                    for (const type of [["type", "warning"], ["required", "danger"]]) {
                        if (doubt[vuln][type[0]] !== undefined && doubt[vuln][type[0]][0] !== "None" && doubt[vuln][type[0]].length > 0) {
                            for (const data of doubt[vuln][type[0]]) virtual.space.push([data, type[1]]);
                        }
                    }

                    for (const data of virtual.space) virtual.div.appendChild(elementBuilder.createBadge(data[0], data[1]));

                    currentData.push({
                        value: virtual.div,
                        raw: true
                    });

                    break;
                default:
                    console.log("Nope!");
            }

            // console.log("currentData: ", currentData.length, currentData);
            if (currentData.length > 1) renderData.push(currentData);
        }

        let builtTable = tableBuilder.buildTable(["Type", "Value"], renderData);
        console.log(builtTable);
        this.viewParent.vectors.appendChild(
            pager.createAccordion("Predictable Vulnerabilities", builtTable)
        )
    }

    async buildReferredDocs(dataset) {
        let doubt = {
                data: dataset.vector.attackVector["doubt"],
                keys: Object.keys(dataset.vector.attackVector["doubt"])
            },
            overallDocuments = Array(),
            parent = document.createElement("div");

        console.log(doubt.keys.length);

        if (doubt.keys.length > 0) {
            referredDocuments = await API.communicate("/static/data/referredDocuments.json", "GET", null, true);
            let ref = Array();
            for (const key of doubt.keys) {
                let storage = Array();

                if (referredDocuments[key] === undefined) return createToast("Error", "Cannot find requested document");
                else {
                    if (Array.isArray(referredDocuments[key])) storage = referredDocuments[key];
                    else storage = referredDocuments[key]["Generic"];
                }

                storage.forEach(data => ref.push(data));
            }

            ref.forEach(currentValue => overallDocuments.push(currentValue));
        }

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
            parent.appendChild(localSkeleton.parent);
        });

        this.viewParent.vectors.appendChild(
            pager.createAccordion("Referred Document", parent)
        );
    }

    buildTags(dataset) {
        let codeParent = document.createElement("div");
        dataset.vector.Details.tag.forEach(currentTag => codeParent.appendChild(elementBuilder.createCode(currentTag, "html")))
        this.viewParent.vectors.appendChild(pager.createAccordion("Tags", codeParent));

        elementBuilder.initCode();
    }

    buildToTables(dataset, type) {
        // console.log(dataset, type, dataset.vector.Details, dataset.vector.Details[type[0]]);
        let data = dataset.vector.Details[type[0]],
            formedData = Array();

        if (Object.keys(data).length > 0) {
            Object.keys(data).forEach(lib => {
                formedData.push([
                    {
                        value: lib,
                        raw: false
                    },
                    {
                        value: data[lib],
                        raw: false
                    }
                ]);
            })

            let builtTable = tableBuilder.buildTable(["Key", "Value"], formedData);

            this.viewParent.vectors.appendChild(pager.createAccordion(type[1], builtTable));
        }
    }

    writeVectorValues(dataset) {
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
        modalDataElement.impact.classList.add("badge", "rounded-pill", "small", `bg-${impactRate[dataset.vector.impactRate][0]}`);
        modalDataElement.impact.innerText = impactRate[dataset.vector.impactRate][1];

        // URL
        modalDataElement.url.url.innerText = dataset.vector.URL;
        modalDataElement.url.uri.innerText = dataset.vector.URI;
        modalDataElement.url.method.innerText = dataset.packet.requestType.toUpperCase();

        // Actions
        modalDataElement.actions.innerHTML = " - ";
        if (dataset.vector.action_URL_Type.length > 0) {
            modalDataElement.actions.innerHTML = "";
            for (let currentRow = 0; currentRow <= dataset.vector.action_URL.length - 1; currentRow++) {
                let localSkeleton = {
                    parent: document.createElement("p"),
                    method: document.createElement("span"),
                    target: document.createElement("span")
                }
                localSkeleton.method.classList.add("badge", "text-uppercase", "me-2", "mb-1",
                    (typeof (coloring[dataset.vector.action_URL_Type[currentRow].toLowerCase()]) === "undefined")
                        ? "bg-warning"
                        : coloring[dataset.vector.action_URL_Type[currentRow].toLowerCase()]);
                localSkeleton.target.classList.add("text-break");

                localSkeleton.method.innerText = dataset.vector.action_URL_Type[currentRow];
                localSkeleton.target.innerText = dataset.vector.action_URL[currentRow];
                localSkeleton.parent.append(
                    localSkeleton.method,
                    localSkeleton.target
                );
                modalDataElement.actions.appendChild(localSkeleton.parent);
            }
        } else {
            modalDataElement.actions.innerHTML = " - ";
        }

        // Threats
        modalDataElement.threat.innerText = "";
        let doubtList = Object.keys(dataset.vector.attackVector["doubt"]);
        if (doubtList.length > 0) {
            doubtList.forEach((currentThreat) => {
                modalDataElement.threat.innerText +=
                    currentThreat.concat(
                        (doubtList[doubtList.length - 1] !== currentThreat) ? ", " : ""
                    );
            });
        } else {
            modalDataElement.threat.innerText = "-";
        }
    }
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