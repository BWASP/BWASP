let pagination = {
        currentPage: 1,
        overallPageCount: 1
    },
    currentState = false,
    idKeyList = [],
    key = "";

const options = {
    verifyResStatusCode: false,
    debug: true,
    API: {
        vectors: "http://192.168.50.158:20102/api/attackVector",
        packets: "/api/attack_vector"
    },
    requestOption: {
        mode: "no-cors",
        headers : {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    }
};


let createKey = () => {
    let gen = () => {
        let key = Math.random().toString(36).substring(2);
        if (!idKeyList.includes(key)) return key;
        else gen()
    }
    return `anonID-${gen()}-${gen()}`;
}

document.getElementById("switchToPacket").addEventListener("click", function() {
    let noData = () => {
        document.getElementById("loadingProgress").classList.add("d-none");
        document.getElementById("resultNoData").classList.remove("d-none");
    }
    document.getElementById("switchToType").innerText = (currentState) ? "Attack Vectors" : "Packets";
    // document.getElementById("currentType").innerText = `All ${(currentState) ? "Packets" : "Attack Vectors"}`;
    let table = {
        table: document.createElement("table"),
        thead: document.createElement("thead"),
        tbody: document.createElement("tbody")
    };
    let tableID = createKey(),
        tablePlace = document.getElementById("tablePlace");
    tablePlace.innerHTML = "";
    document.getElementById("loadingProgress").classList.remove("d-none");
    document.getElementById("resultNoData").classList.add("d-none");
    currentState = !currentState;
    ((status = (currentState) ? "Attack Vector" : "Packets") => {
        document.getElementById("pageTitle").innerHTML = status;
        document.title = `${status} - BWASP`;
    })()

    let newThead = document.createElement("tr"),
        element = [
            ["URL", "Vulnerability Doubt", "Method", "Date", "Impact"],
            ["URL", "Packet", "Vulnerability Doubt", "Method", "Related Data", "Date", "Impact"]
        ];

    // Build thead
    element[Number(!currentState)].forEach((columnName) => {
        let tempThElement = document.createElement("th");
        tempThElement.innerHTML = columnName;
        newThead.appendChild(tempThElement);
    });
    // render thead
    table.thead.appendChild(newThead);

    // Build tbody
    let currentKey = (currentState) ? "vectors" : "packets";
    let currentAPI = options.API[currentKey];

    console.log(currentAPI);
    fetch(currentAPI, options.requestOption)
        .then((res)=>res.json())
        .then((buildData)=>console.log(buildData))

    // Connect to API to receive dataset
    /*
    fetch(currentAPI, options.requestOption)
        .then((res) => res.json())
        .then((buildData) => {
            // console.log(buildData);
            if (buildData.length <= 0) noData();
            for (let count = 0; count < buildData.length; count++) {
                console.log(buildData);
                // fetch(currentAPI+"")



                let frame = document.createElement("tr"),
                    localData = buildData[count],
                    element = Object(),
                    impactData = [];

                if (localData.date === "None" && !options.debug) return noData();

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
                element.url.parent.style.setProperty("width", `${(currentState)?20:10}%`, "important");

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
                if (!currentState) {
                    element["packet"] = document.createElement("td");
                    element.packet.innerText = localData.packet;
                    element.packet.classList.add("align-middle");
                    element.packet.style.setProperty("width", `${(currentState)?0:15}%`, "important");
                    frame.appendChild(element.packet);
                }

                // Vulnerability doubt
                element["vuln"] = {
                    parent: document.createElement("td"),
                    title: document.createElement("p"),
                    cve: document.createElement("div")
                };

                if (currentState) element.vuln.cve.classList.add("d-inline-flex");
                element.vuln.title.classList.add("font-weight-bold", "mb-2", "text-danger");
                element.vuln.title.innerText = localData.vulnerability.type;
                element.vuln.parent.appendChild(element.vuln.title);

                localData.vulnerability.CVE.forEach((data) => {
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
                    cveElement.parent.classList.add("mb-1", (!currentState) ? "mb-1" : "mr-1");
                    cveElement.code.innerText = data.numbering;
                    cveElement.parent.appendChild(cveElement.code);
                    cveElement.parent.appendChild(separateBy[Number(!currentState)]);

                    if (!currentState) {
                        cveElement.description.innerText = data.description;
                        cveElement.description.className = "small";
                        cveElement.parent.append(cveElement.description);
                    }
                    element.vuln.cve.appendChild(cveElement.parent);
                })
                element.vuln.parent.appendChild(element.vuln.cve);

                element.vuln.parent.classList.add("align-middle");
                element.vuln.parent.style.setProperty("width", `${(currentState)?60:45}%`, "important");
                frame.appendChild(element.vuln.parent);

                // Method
                element["method"] = document.createElement("td");
                element.method.innerText = localData.method;
                element.method.classList.add("align-middle");
                element.method.style.setProperty("width", "3%", "important");
                frame.appendChild(element.method);

                // Related
                if (!currentState) {
                    let relatedData = {
                        parent: document.createElement("td"),
                        child: document.createElement("div")
                    };
                    relatedData.parent.classList.add("align-middle");
                    localData.relatedData.forEach((data) => {
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

                switch (localData.impactRate) {
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
     */
})

window.onload = () => {
    // Initialize DOM Elements.
    document.getElementById("switchToPacket").click();
}