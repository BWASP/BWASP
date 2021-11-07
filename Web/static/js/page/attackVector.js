// Get modules
import {API as api, createKey} from '../jHelper.js';

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
    returnError = (errorMessage = "No data") => {
        document.getElementById("loadingProgress").classList.add("d-none");
        document.getElementById("resultNoData").classList.remove("d-none");
        document.getElementById("errorMessagePlace").innerText = errorMessage;
        console.error(`:: ERROR :: ${errorMessage}`);
    };

// API Communicator.
let API = new api();

async function dataUpdater(requestType, requestPage, rowPerPage) {
    let currentState = (stateHandler.isVector) ? "vectors" : "packets",
        dataPackage = Array();
    await API.communicate(
        APIEndpoints.vectors + `/${requestPage * rowPerPage + (requestPage === 0) ? 1 : 0}/${(requestPage + 1) * rowPerPage}`,
        (error, res) => {
            console.log("Domain data: ", res);
            if (error) return returnError(error);
            if (res.length <= 0) console.error(":: ERROR :: No data");
            res.forEach((domainData) => {
                let skeleton = {
                    category: String(),
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
                    vulnerability: {
                        type: String(),
                        cve: Array()
                    },
                    method: String(),
                    impactRate: 0,
                    details: API.jsonDataHandler(domainData["Details"])
                }, packetData = Array();


                // Packet - when Automatic
                API.communicate(`${APIEndpoints.packets.base}/${APIEndpoints.packets.type.auto}/${domainData["related_Packet"]}`, (err, res) => {
                    if (!err) packetData.push(res);
                    else API.communicate(`${APIEndpoints.packets.base}/${APIEndpoints.packets.type.manual}/${domainData["related_Packet"]}`, (err, res) => {
                        if (!err) packetData.push(res);
                    });
                    console.log(`Packet data of No. ${domainData["related_Packet"]}`, packetData);
                    skeleton.category = packetData[0]["category"];
                    skeleton.method = packetData[0]["requestType"];
                    // console.log("Packet: ", packetData[0]);
                });

                dataPackage.push(skeleton);
            });

        });
    return dataPackage;
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
            tmpElement.innerText = currentElement;
            thead.child.appendChild(tmpElement);
        })
        thead.parent.appendChild(thead.child);
        return thead.parent;
    }
}

document.getElementById("switchToPacket").addEventListener("click", () => {
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
    table.elements.table.classList.add("table");

    // Build thead
    table.elements.table.appendChild(
        builder.buildHead(elements[currentState.type])
    )

    // Get data by pagination
    dataUpdater(null, pagination.currentPage, pagination.rowPerPage).then((res) => {
        console.log("Data Result : ", res);
    })


    // =================================================================================
    //   LEGACY BELOW
    // =================================================================================

    /*
    let newThead = document.createElement("tr"),
        element = [
            ["URL", "Vulnerability Doubt", "Method", "Date", "Impact"],
            ["URL", "Packet", "Vulnerability Doubt", "Method", "Related Data", "Date", "Impact"]
        ],
        currentState = (stateHandler.isVector) ? {
            type: "vectors",
            viewString: "Attack Vectors"
        } : {
            type: "packets",
            viewString: "Packets"
        };


    // Update texts from DOM
    // document.getElementById("switchToType").innerText = currentState.viewString;
    document.getElementById("pageTitle").innerHTML = currentState.viewString;
    document.title = `${currentState.viewString} - BWASP`;

    // Initialize tablePlace DIV
    tablePlace.innerHTML = "";

    // Toggle loading screen
    document.getElementById("loadingProgress").classList.remove("d-none");
    document.getElementById("resultNoData").classList.add("d-none");

    // Build thead
    element[Number(!stateHandler.isVector)].forEach((columnName) => {
        let tempThElement = document.createElement("th");
        tempThElement.innerHTML = columnName;
        newThead.appendChild(tempThElement);
    });
    // render thead
    table.thead.appendChild(newThead);

    // Build tbody
    let currentKey = (stateHandler.isVector) ? "vectors" : "packets";

    API.communicate(APIEndpoints[currentState.type], (error, dataPackage) => {
        if (error) return returnError(error);
        else if (dataPackage.length <= 0) returnError();
        // console.log(dataPackage);
    })
    /*
        fetch(API[currentKey]).then((res) => {
            if(res.status!==200 && !debug) noData();
            else res.json().then((buildData)=>{
                if(debug) buildData = implementationSample[currentKey];
                if (buildData.length<=0){
                    document.getElementById("loadingProgress").classList.add("d-none");
                    document.getElementById("resultNoData").classList.remove("d-none");
                    return;
                }
                for (let count = 0; count < buildData.length; count++) {
                    let frame = document.createElement("tr"),
                        localData = buildData[count],
                        element = Object(),
                        impactData = [];

                    if(localData.date === "None" && !debug) return noData();

                    // URL
                    let idKey = createKey();
                    element["url"] = {
                        parent: document.createElement("td"),
                        child: {
                            url: document.createElement("a"),
                            dropdown: {
                                parent: document.createElement("div"),
                                child: {
                                    title: document.createElement("p"),
                                    contents: document.createElement("ul")
                                }
                            }
                        }
                    };

                    element.url.parent.classList.add("align-middle");
                    element.url.parent.style.setProperty("width", `${(stateHandler.isVector)?20:10}%`, "important");

                    element.url.child.url.href = `#${idKey}`;
                    element.url.child.url.innerHTML = localData.url;
                    element.url.child.url.classList.add("d-block", "py-3", "m-0", "fw-bold", "text-decoration-none", "text-primary");
                    element.url.child.url.setAttribute("data-bs-toggle", "collapse");
                    element.url.child.url.setAttribute("role", "button");
                    element.url.child.url.setAttribute("aria-expanded", "false")
                    element.url.child.url.setAttribute("aria-controls", idKey);

                    element.url.child.dropdown.parent.classList.add("collapse");
                    element.url.child.dropdown.parent.id = idKey;

                    element.url.child.dropdown.child.title.classList.add("font-weight-bold", "mb-1");
                    element.url.child.dropdown.child.title.innerText = "Payloads";

                    localData.payloads.forEach((payload) => {
                        let liElement = document.createElement("li");
                        liElement.innerText = payload;
                        element.url.child.dropdown.child.contents.appendChild(liElement);
                    })
                    element.url.child.dropdown.parent.append(
                        element.url.child.dropdown.child.title,
                        element.url.child.dropdown.child.contents
                    );
                    element.url.parent.append(
                        element.url.child.url,
                        element.url.child.dropdown.parent
                    );
                    frame.appendChild(element.url.parent);

                    // Packets
                    if(!stateHandler.isVector){
                        element["packet"] = document.createElement("td");
                        element.packet.innerText = localData.packet;
                        element.packet.classList.add("align-middle");
                        element.packet.style.setProperty("width", `${(stateHandler.isVector)?0:15}%`, "important");
                        frame.appendChild(element.packet);
                    }

                    // Vulnerability doubt
                    element["vuln"] = {
                        parent: document.createElement("td"),
                        title: document.createElement("p"),
                        cve: document.createElement("div")
                    };

                    if(stateHandler.isVector) element.vuln.cve.classList.add("d-inline-flex");
                    element.vuln.title.classList.add("font-weight-bold", "mb-2", "text-danger");
                    element.vuln.title.innerText = localData.vulnerability.type;
                    element.vuln.parent.appendChild(element.vuln.title);

                    localData.vulnerability.CVE.forEach((data)=>{
                        let cveElement = {
                            parent: document.createElement("p"),
                            code: document.createElement("code"),
                            description: document.createElement("span")
                        },
                        separateBy = [
                            document.createElement("span"),
                            document.createElement("br")
                        ];
                        separateBy[0].innerText = ",";
                        cveElement.parent.classList.add("mb-1", (!stateHandler.isVector)?"mb-1":"mr-1");
                        cveElement.code.innerText = data.numbering;
                        cveElement.parent.appendChild(cveElement.code);
                        cveElement.parent.appendChild(separateBy[Number(!stateHandler.isVector)]);

                        if(!stateHandler.isVector){
                            cveElement.description.innerText = data.description;
                            cveElement.description.className = "small";
                            cveElement.parent.append(cveElement.description);
                        }
                        element.vuln.cve.appendChild(cveElement.parent);
                    })
                    element.vuln.parent.appendChild(element.vuln.cve);

                    element.vuln.parent.classList.add("align-middle");
                    element.vuln.parent.style.setProperty("width", `${(stateHandler.isVector)?60:45}%`, "important");
                    frame.appendChild(element.vuln.parent);

                    // Method
                    element["method"] = document.createElement("td");
                    element.method.innerText = localData.method;
                    element.method.classList.add("align-middle");
                    element.method.style.setProperty("width", "3%", "important");
                    frame.appendChild(element.method);

                    // Related
                    if(!stateHandler.isVector){
                        let relatedData = {
                            parent: document.createElement("td"),
                            child: document.createElement("div")
                        };
                        relatedData.parent.classList.add("align-middle");
                        localData.relatedData.forEach((data)=>{
                            let relatedDOM = document.createElement("a")
                            relatedDOM.href = data;
                            relatedDOM.innerHTML = data;
                            relatedData.child.appendChild(relatedDOM);
                        })
                        relatedData.parent.style.setProperty("width", "10%", "important");
                        relatedData.parent.appendChild(relatedData.child);
                        frame.appendChild(relatedData.parent);
                    }

                    let date = new Date(localData.date);
                    date = date.toISOString().substring(0, 19).split("T")
                    date.push("UTC");
                    element["date"] = {
                        parent: document.createElement("td"),
                        child: {
                            date: document.createElement("span"),
                            time: document.createElement("span")
                        }
                    }
                    element.date.parent.classList.add("align-middle");
                    element.date.child.date.classList.add("fw-bold");
                    element.date.child.date.innerText = date[0];
                    element.date.child.time.innerText = `${date[1]} ${date[2]}`;
                    element.date.parent.append(
                        element.date.child.date,
                        document.createElement("br"),
                        element.date.child.time
                    );
                    element.date.parent.style.setProperty("width", "10%", "important");
                    frame.appendChild(element.date.parent);

                    // Impact
                    element["impact"] = {
                        parent: document.createElement("td"),
                        child: document.createElement("p")
                    };

                    switch(localData.impactRate){
                        case 0:
                            impactData = ["success", "Low"]
                            break
                        case 1:
                            impactData = ["warning", "Normal"]
                            break
                        case 2:
                            impactData = ["danger", "High"]
                            break
                    }

                    element.impact.parent.classList.add("align-middle");
                    element.impact.child.classList.add("small", "text-center", "p-1", "mb-0", "pl-3", "pr-3", "rounded-pill", `btn-${impactData[0]}`);
                    element.impact.child.innerText = impactData[1];

                    element.impact.parent.appendChild(element.impact.child);
                    element.impact.parent.style.setProperty("width", "5%", "important");
                    frame.appendChild(element.impact.parent);

                    table.tbody.appendChild(frame);
                }

                table.table.classList.add("table", "table-stripped");
                table.table.id = tableID;
                table.table.append(
                    table.thead,
                    table.tbody
                );
                tablePlace.appendChild(table.table);
                // $(`#${tableID}`).DataTable();
                document.getElementById("loadingProgress").classList.add("d-none");
            })

    })
     */
})

window.onload = () => {
    let userHelpModal = new bootstrap.Modal(document.getElementById('helpModal'), {
        show: true
    });
    document.getElementById("openHelpModal").addEventListener("click", () => userHelpModal.toggle());
    document.getElementById("switchToPacket").click();
};