// Get modules
import {API as api, elementBuilder as EBuilder, tableBuilder as TBuilder, Cookies, createToast} from '../jHelper.js';

// Define API Endpoints
const APIEndpoints = {
    webEnvironments: "/api/systeminfo",
    job: "/api/job",
    count: {
        packet: {
            auto: "/api/packet/automation/count",
            manual: "/api/packet/manual/count",
        },
        domain: "/api/domain/count",
        port: "/api/ports/count"
    },
    searchCVE: "/api/cve/search",
    ports: "/api/ports",
    CSP: "/api/cspevaluator"
}

let API = await new api();
let builder = {
    element: new EBuilder(),
    table: new TBuilder()
}

class dashboard {
    constructor() {
        this.iconURL = Object();
        this.fileStorage = Object();
        this.webEnvironment = {
            target: String(), data: Object()
        };
        this.viewData = {
            CVECount: {
                count: Number(),
                needsUpdate: false
            }
        };
        this.job = {
            allJobs: Array(),
            currentJob: Object()
        };
        this.ports = Object();
        this.CSP = {
            data: Object(),
            needsUpdate: false
        }
    }

    async updateView() {
        await this.getCurrentJob();
        await this.webEnvironments();
        await this.getCSP();
        this.updateVisibleItems();
        this.updateCSPView();
        this.updatePacketCount();
        this.updateThreatsCount();
        this.updateRelatedCVEs();
        this.updatePorts();
    }

    updateVisibleItems() {
        // CSP
        let CSPElement = {
                pill: document.getElementById("CSPSelectionPill"),
                view: document.getElementById("pills-CSP"),
                table: document.getElementById("CSPViewPlace")
            },
            CSPCondition = typeof (this.CSP.data) === "object" && this.CSP.data.length > 0;
        Object.keys(CSPElement).forEach(key => CSPElement[key].classList[(CSPCondition) ? "remove" : "add"]("d-none"));
    }

    async getCSP() {
        this.CSP.data = await API.communicate(APIEndpoints.CSP);
    }

    updateCSPView() {
        if(typeof (this.CSP.data) !== "object" || this.CSP.data.length <= 0) return;
        let CSPData = JSON.parse(this.CSP.data[0].header),
            tableData = Array(),
            virtualDiv = document.createElement("div"),
            viewPlace = document.getElementById("CSPViewPlace");

        virtualDiv.classList.add("col-md-12");

        for(const key of Object.keys(CSPData)){
            let data = [{
                value: key,
                raw: false
            }], job = false;

            if(typeof(CSPData[key]) === "string"){
                data.push({
                    value: CSPData[key],
                    raw: false
                })
                job = true;
            }else if(Array.isArray(CSPData[key])){
                let tmpDiv = document.createElement("div");
                CSPData[key].forEach(name => tmpDiv.appendChild(builder.element.createBadge(name)));
                data.push({
                    value: tmpDiv,
                    raw: true
                })
                job = true;
            }

            if(job) tableData.push(data);
        }

        virtualDiv.appendChild(builder.table.buildTable(
            ["Key", "Value"],
            tableData
        ));

        viewPlace.innerHTML = "";
        viewPlace.appendChild(virtualDiv);
    }

    async getCurrentJob() {
        this.job.allJobs = await API.communicate(APIEndpoints.job);
    }

    async updatePacketCount() {
        let currentDOM = document.getElementById("receivedPacketsCount");
        if (this.job.allJobs.length > 0) {
            try {
                let count = {
                    auto: await API.communicate(APIEndpoints.count.packet.auto),
                    manual: await API.communicate(APIEndpoints.count.packet.manual)
                };
                currentDOM.innerText = count.auto.count + count.manual.count;
            } catch (e) {
                console.error(e);
            }
        } else currentDOM.innerText = " - ";
    }

    async updateRelatedCVEs() {
        let currentDOM = document.getElementById("relatedCVECount");
        if (this.job.allJobs.length > 0) {
            if (this.viewData.CVECount.needsUpdate) {
                let dataset = this.webEnvironment.data, APIResult = Object(), countedValue = Number();
                for (const type of Object.keys(dataset)) {
                    if (!Number.isInteger(Number(type))) {
                        for (const lib of Object.keys(dataset[type])) {
                            // console.log(type, lib);
                            APIResult = await API.communicate(`${APIEndpoints.searchCVE}/${lib}/${dataset[type][lib].version}/count`);
                            countedValue += APIResult.count;
                        }
                    }
                }

                this.viewData.CVECount.count = countedValue;

                currentDOM.innerText = (this.viewData.CVECount.count === 0) ? "-" : String(this.viewData.CVECount.count);

                this.viewData.CVECount.needsUpdate = false;
            }

        } else currentDOM.innerText = " - ";
    }

    async updateThreatsCount() {
        let currentDOM = document.getElementById("detectedThreatsCount");
        if (this.job.allJobs.length > 0) {
            let count = Object();
            try {
                count = await API.communicate(APIEndpoints.count.domain);
            } catch (e) {
                return console.error(e);
            }

            currentDOM.innerText = count.count;
        } else currentDOM.innerText = " - ";
    }

    async updatePorts() {
        let localPorts = Object(),
            targets = [
                document.getElementById("portCountViewPlace"),
                document.getElementById("portCountViewPlace"),
                document.getElementById("openedPortsCount")
            ],
            reGenObject = false;

        if (this.job.allJobs.length > 0) {
            let portData = {
                count: await API.communicate(APIEndpoints.count.port),
                data: await API.communicate(APIEndpoints.ports)
            }

            // Set port count
            targets.forEach((currentTarget) => currentTarget.innerText = portData.count.count);

            // Port information
            if (portData.data.length > 0) {
                for (const port of portData.data) {
                    if (port.result === "Open") {
                        if (!Object.keys(localPorts).includes(port["service"])) localPorts[port["service"]] = Array();
                        if (port.port !== "None") localPorts[port["service"]].push(port.port)
                    }
                }
            }

            // Regen option
            reGenObject = JSON.stringify(this.ports) !== JSON.stringify(localPorts);

            // Open view
            // document.getElementById("portViewPlace-detail").classList.remove("d-none");
            document.getElementById("portViewPlace-noData").classList.add("d-none");

            // Save data if not same data
            if (reGenObject) {
                // Save ports data
                this.ports = localPorts;

                // Initialize opened ports DOM
                let portView = document.getElementById("portViewPlace");
                portView.innerHTML = "";

                // Build
                Object.keys(this.ports).forEach((currentType) => {
                    let skeleton = {
                        parent: document.createElement("section"),
                        name: document.createElement("p"),
                        ports: document.createElement("p")
                    };
                    skeleton.parent.classList.add("col-md-12", "mt-3");
                    skeleton.name.classList.add("text-muted", "small", "text-capitalize");
                    skeleton.name.innerText = `${currentType} (${localPorts[currentType].length})`;
                    localPorts[currentType].forEach(currentPort => {
                        skeleton.ports.innerText += currentPort.concat((localPorts[currentType][localPorts[currentType].length - 1] !== currentPort) ? ", " : "")
                    })

                    skeleton.parent.append(skeleton.name, skeleton.ports)
                    portView.appendChild(skeleton.parent);
                });
                this.updateOverviewPorts();
            }
        } else targets[1].innerText = " - ";
    }

    updateOverviewPorts() {
        let viewPlace = document.getElementById("overview-Ports");
        viewPlace.innerHTML = "";

        Object.keys(this.ports).forEach(type => {
            let portSkeleton = {
                parent: document.createElement("li"),
                type: document.createElement("span")
            };
            portSkeleton.type.classList.add("fw-bold");
            portSkeleton.type.innerText = type;
            portSkeleton.parent.append(
                portSkeleton.type,
                ` : ${this.ports[type].length} Ports`
            )
            viewPlace.appendChild(portSkeleton.parent);
        })
    }

    async webEnvironments() {
        if (this.job.allJobs.length > 0) {
            let environmentData, localObject = [Object(), Object()];
            try {
                environmentData = await API.communicate(`${APIEndpoints.webEnvironments}/1`);
                localObject = {
                    target: environmentData[0].url, data: JSON.parse(environmentData[0].data)
                }
            } catch (e) {
                return console.error(e);
            }

            document.getElementById("webEnvDataPlace").classList.remove("d-none");
            // document.getElementById("webEnvDataPlace-detail").classList.remove("d-none");
            document.getElementById("webEnvDataPlace-noData").classList.add("d-none");

            let reGenObject = JSON.stringify(this.webEnvironment) !== JSON.stringify(localObject);
            this.webEnvironment.target = localObject.target;
            this.webEnvironment.data = localObject.data;

            // CVE Count must be updated when web environment data has changed.
            this.viewData.CVECount.needsUpdate = reGenObject;

            if (reGenObject) {
                document.getElementById("pageTitle_sub").innerText = `Target: ${this.webEnvironment.target}`;
                document.getElementById("webEnvDataPlace").innerHTML = "";
                let viewArea = document.getElementById("viewArea");
                viewArea.innerHTML = "";
                for (const key of Object.keys(this.webEnvironment.data)) {
                    if (!Number.isInteger(Number(key))) {
                        viewArea.appendChild(await this.buildOverviewEnvironments(key, this.webEnvironment.data[key]));
                        document.getElementById("webEnvDataPlace").appendChild(await this.buildWebEnvCard(key, this.webEnvironment.data[key]));
                    }
                }
                let masonry = new Masonry('#viewArea', {
                    columnWidth: 1,
                    itemSelector: '.grid-item'
                });
            }
        } else {
            document.getElementById("webEnvDataPlace").classList.add("d-none");
            // document.getElementById("webEnvDataPlace-detail").classList.add("d-none");
            document.getElementById("webEnvDataPlace-noData").classList.remove("d-none");
        }
    }

    async buildOverviewEnvironments(type, dataPackage) {
        let skeleton = {
            parent: document.createElement("div"),
            type: document.createElement("p"),
            childBox: document.createElement("div")
        };

        skeleton.parent.classList.add("border", "p-3", "rounded-custom", "grid-item");
        skeleton.type.classList.add("text-muted", "small", "mb-1", "text-uppercase");
        skeleton.childBox.classList.add("row");

        skeleton.type.innerText = type;

        for (const key of Object.keys(dataPackage)) {
            let childParent = document.createElement("div");
            childParent.classList.add("col", "mt-2");

            childParent.appendChild(await this.buildWebEnvIcon(key, dataPackage[key].icon));

            // console.log(key, dataPackage[key].icon);
            skeleton.childBox.appendChild(childParent);
        }

        // Assembly
        skeleton.parent.append(
            skeleton.type,
            skeleton.childBox
        );

        return skeleton.parent;
    }

    async getIcon(filename) {
        // Return icon URL from saved location
        if (Object.keys(this.iconURL).includes(filename)) return this.iconURL[filename].url;
        else this.iconURL[filename] = {
            url: String()
        }

        let iconURL = {
            alternative: `https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/drivers/webextension/images/icons/${filename}`,
            local: `/static/img/icons/${filename}`,
            unknown: "/static/img/icons/unknown.png"
        };
        for (const icon of Object.keys(iconURL)) {
            let checker = new Request(iconURL[icon]);
            let status = await fetch(checker)
                .then(res => {
                    return res.status;
                })
                .catch(err => console.log(err));
            if (status === 200) {
                this.iconURL[filename].url = iconURL[icon];
                return iconURL[icon];
            }
        }
    }

    async buildWebEnvIcon(name, filename) {
        let skeleton = {
                parent: document.createElement("div"),
                icon: document.createElement("img")
            },
            iconURL = await this.getIcon(filename);

        // Set classes
        skeleton.parent.classList.add("dashboard", "icon", "rounded-custom", "d-flex", "align-items-center", "justify-content-center");
        skeleton.icon.classList.add("p-1");

        // Set size
        skeleton.icon.setAttribute("width", "55");
        skeleton.icon.setAttribute("height", "55");

        // Set description
        skeleton.parent.setAttribute("title", name);

        // Set src
        skeleton.icon.src = iconURL;

        // Assembly elements and return
        skeleton.parent.appendChild(skeleton.icon);
        return skeleton.parent;
    }

    async buildWebEnvCard(type, dataPackage) {
        let skeleton = {
            parent: document.createElement("section"),
            type: document.createElement("p"),
            childBox: document.createElement("div")
        };

        // Set classes
        skeleton.parent.classList.add("row", "mb-3", "col-md-6");
        skeleton.childBox.classList.add("row");
        skeleton.type.classList.add("col-md-12", "text-muted", "small", "text-capitalize");

        // Set values
        skeleton.type.innerText = type;

        // Create child
        for (const key of Object.keys(dataPackage)) {
            let data = dataPackage[key],
                versionCase = (data.version !== 0),
                childSkeleton = {
                    parent: document.createElement("a"),
                    icon: document.createElement("img"),
                    details: {
                        parent: document.createElement("div"),
                        name: document.createElement("p"),
                        version: document.createElement("p")
                    }
                };

            // Set classes to child
            childSkeleton.parent.classList.add("col-md-6", "mb-2", "sizer", "align-items-center", "text-decoration-none");
            childSkeleton.details.parent.classList.add("ms-2");
            childSkeleton.icon.classList.add("rounded-custom", "border", "p-1");
            childSkeleton.details.name.classList.add("mb-0", "h6");
            childSkeleton.details.version.classList.add("mb-0", "text-muted", "small");

            // Set attrs
            childSkeleton.parent.href = "javascript:void(0);";
            childSkeleton.icon.setAttribute("width", "55");
            childSkeleton.icon.setAttribute("height", "55");
            childSkeleton.icon.src = await this.getIcon(data.icon);

            // Set values
            childSkeleton.details.name.innerText = key;
            if (versionCase) childSkeleton.details.version.innerText = data.version;

            // Add event listener
            childSkeleton.parent.addEventListener("click", async () => {
                let views = {
                    name: document.getElementById("envDetails-name"),
                    icon: document.getElementById("envDetails-icon"),
                    version: document.getElementById("envDetails-version"),
                    viewPlace: document.getElementById("envDetails-CVEs-viewPlace"),
                    detectedArea: document.getElementById("envDetails-detectedArea")
                }

                document.getElementById("envDetails-CVECount-area").classList.add("d-none");
                document.getElementById("envDetails-CVEs").classList.add("d-none");

                views.name.innerText = key;
                views.icon.src = childSkeleton.icon.src;
                views.version.innerText = (versionCase)
                    ? data.version
                    : " ";
                views.detectedArea.innerText = data.detect;

                let modal = new bootstrap.Modal(document.getElementById("envDetails"), {
                    show: true
                });
                modal.show();

                let cve = Object();
                try {
                    let baseAPIEndpoint = `${APIEndpoints.searchCVE}/${key}/${data.version}`;
                    cve = {
                        count: await API.communicate(`${baseAPIEndpoint}/count`),
                        data: await API.communicate(baseAPIEndpoint)
                    }
                } catch (e) {
                    return createToast("Error has occurred", `${e.name}: ${e.message}`, "danger", false);
                }

                // Remove d-none option to display
                document.getElementById("envDetails-CVECount-area").classList.remove("d-none");
                document.getElementById("envDetails-CVEs").classList.remove("d-none");

                // Set count data
                document.getElementById("envDetails-CVECount").innerText = String(cve.count.count);
                document.getElementById("envDetails-renderedCVECount").innerText = String(cve.data.length);

                // Render CVE Datas
                let viewPlace = document.getElementById("envDetails-CVEs-viewPlace");
                viewPlace.innerHTML = "";

                cve.data.forEach((data) => {
                    let CVESkeleton = {
                        parent: document.createElement("div"),
                        cve: document.createElement("p"),
                        description: document.createElement("p")
                    }

                    CVESkeleton.parent.classList.add("shadow-sm", "rounded-custom", "p-3", "mt-2", "mb-2");
                    CVESkeleton.cve.classList.add("h6", "mb-1", "fw-bold");
                    CVESkeleton.description.classList.add("text-muted", "mb-0", "small");

                    CVESkeleton.cve.innerText = data.year;
                    CVESkeleton.description.innerText = data.description;

                    CVESkeleton.parent.append(
                        CVESkeleton.cve,
                        CVESkeleton.description
                    );

                    views.viewPlace.appendChild(CVESkeleton.parent);
                });

                // alert(`Hello! I am ${key}`);
                console.log(cve);
            });

            // Assembly and return
            childSkeleton.details.parent.append(
                childSkeleton.details.name,
                childSkeleton.details.version
            );
            childSkeleton.parent.append(
                childSkeleton.icon,
                childSkeleton.details.parent
            );
            skeleton.childBox.appendChild(childSkeleton.parent);
            // console.log(skeleton.childBox);
        }

        skeleton.parent.append(skeleton.type, skeleton.childBox);
        return skeleton.parent;
    }
}

window.onload = () => {
    let render = new dashboard();
    render.updateView();
    setInterval(async () => {
        try{
            await render.updateView();
        } catch (e) {
            console.error("[Dashboard Handler] Data not received.");
        }
    }, 3000);
}