// Get modules
import {API as api} from '../jHelper.js';

// Define API Endpoints
const APIEndpoints = {
    webEnvironments: "/api/systeminfo"
}

let API = await new api();

class dashboard {
    constructor() {
        this.webEnvironment = {
            target: String(),
            data: Object()
        };
        this.viewData = {
            CVECount: {
                count: Number(),
                runCount: Number()
            }
        }
        this.job = {
            allJobs: Array(),
            currentJob: Object()
        };
        this.ports = Object();
        this.flip = true;
    }

    async updateView() {
        await this.getCurrentJob();
        await this.webEnvironments();
        this.updatePacketCount();
        this.updateThreatsCount();
        this.updateRelatedCVEs();
        this.updatePorts();
    }

    async getCurrentJob() {
        this.job.allJobs = await API.communicateRAW("/api/job");
    }

    async updatePacketCount() {
        let currentDOM = document.getElementById("receivedPacketsCount");
        if (this.job.allJobs.length > 0) {
            try{
                let count = {
                    auto: await API.communicateRAW("/api/packet/automation/count"),
                    manual: await API.communicateRAW("/api/packet/manual/count")
                };
                currentDOM.innerText = count.auto.count + count.manual.count;
            }catch (e) {
                console.error(e);
            }
        } else currentDOM.innerText = " - ";
    }

    updateRelatedCVEs() {
        let currentDOM = document.getElementById("relatedCVECount");
        if (this.job.allJobs.length > 0) {
            if (!this.flip) this.flip = !this.flip;
            else {
                this.viewData.CVECount.runCount += 1;
                Object.keys(this.webEnvironment.data).forEach((currentKey) => {
                    Object.keys(this.webEnvironment.data[currentKey]).forEach(async (currentLib) => {
                        currentLib = {
                            name: currentLib,
                            version: this.webEnvironment.data[currentKey][currentLib]["version"]
                        };
                        await API.communicate(`/api/cve/search/${currentLib.name}/${currentLib.version}/count`, (err, res) => this.addCVECount(res.count));
                    })
                })

                // Save to DOM
                if (this.viewData.CVECount.runCount >= 3)
                    currentDOM.innerText = (this.viewData.CVECount.count === 0)
                        ? "-"
                        : String(this.viewData.CVECount.count);
                this.addCVECount(0, true);
            }
        } else currentDOM.innerText = " - ";
    }

    addCVECount(count, init = false) {
        if (init) return this.viewData.CVECount.count = Number();
        this.viewData.CVECount.count += count;
    }

    async updateThreatsCount() {
        let currentDOM = document.getElementById("detectedThreatsCount");
        if (this.job.allJobs.length > 0) {
            let count = Object();
            try{
                count = await API.communicateRAW("/api/domain/count");
            }catch (e) { return console.error(e); }

            currentDOM.innerText = count.count;
        } else currentDOM.innerText = " - ";
    }

    async updatePorts() {
        let localPorts = Object(),
            targets = [
                document.getElementById("portCountViewPlace"),
                document.getElementById("openedPortsCount")
            ];

        if (this.job.allJobs.length > 0) {
            let portData = {
                count: await API.communicateRAW("/api/ports/count"),
                data: await API.communicateRAW("/api/ports")
            }

            // Set port count
            targets.forEach((currentTarget) => currentTarget.innerText = portData.count.count);

            // Port information
            if(portData.data.length > 0) {
                for(const port of portData.data){
                    if (port.result === "Open") {
                        if (!Object.keys(localPorts).includes(port["service"]))
                            localPorts[port["service"]] = Array();
                        if (port.port !== "None") localPorts[port["service"]].push(port.port)
                    }
                }
            }

            // Open view
            document.getElementById("portViewPlace-detail").classList.remove("d-none");
            document.getElementById("portViewPlace-noData").classList.add("d-none");

            // Save data if not same data
            if (JSON.stringify(this.ports) !== JSON.stringify(localPorts)) {
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
                        skeleton.ports.innerText += currentPort.concat(
                            (localPorts[currentType][localPorts[currentType].length - 1] !== currentPort)
                                ? ", "
                                : ""
                        )
                    })

                    skeleton.parent.append(
                        skeleton.name,
                        skeleton.ports
                    )
                    portView.appendChild(skeleton.parent);
                });
            }
        }else targets[1].innerText = " - ";
    }

    updateAnalysisLevel() {
        API.communicate("/api/job/1", (err, res) => {
            document.getElementById("analysisLevelView").innerText = (!err) ? res[0].recursiveLevel : "0";
        })
    }

    async webEnvironments() {
        if (this.job.allJobs.length > 0) {
            let environmentData, localObject = [Object(), Object()];
            try{
                environmentData = await API.communicateRAW(`${APIEndpoints.webEnvironments}/1`);
                localObject = {
                    target: environmentData[0].url,
                    data: JSON.parse(environmentData[0].data)
                }
            }catch (e) { return console.error(e); }

            document.getElementById("webEnvDataPlace").classList.remove("d-none");
            document.getElementById("webEnvDataPlace-detail").classList.remove("d-none");
            document.getElementById("webEnvDataPlace-noData").classList.add("d-none");

            let reGenObject = JSON.stringify(this.webEnvironment) !== JSON.stringify(localObject);
            this.webEnvironment.target = localObject.target;
            this.webEnvironment.data = localObject.data;

            if (reGenObject) {
                document.getElementById("webEnvURLPlace").innerText = this.webEnvironment.target;
                document.getElementById("webEnvDataPlace").innerHTML = "";
                Object.keys(this.webEnvironment.data).forEach((key) => {
                    document.getElementById("webEnvDataPlace").appendChild(this.buildWebEnvCard(key, this.webEnvironment.data[key]));
                });
            }
        }else{
            document.getElementById("webEnvDataPlace").classList.add("d-none");
            document.getElementById("webEnvDataPlace-detail").classList.add("d-none");
            document.getElementById("webEnvDataPlace-noData").classList.remove("d-none");
        }
    }

    buildWebEnvCard(type, dataPackage) {
        let skeleton = {
            parent: document.createElement("div"),
            type: document.createElement("p"),
            child: document.createElement("div")
        };
        // Class Set
        skeleton.parent.classList.add("col-md-6", "mt-3");
        skeleton.type.classList.add("text-muted", "small", "text-capitalize");
        // Value Set
        skeleton.type.innerText = type;
        Object.keys(dataPackage).forEach((key) => {
            let data = dataPackage[key],
                localSkeleton = {
                    parent: document.createElement("a"),
                    productImage: document.createElement("img"),
                    productName: document.createElement("p"),
                    version: document.createElement("p")
                },
                versionCase = (data.version !== 0);

            // set classes
            localSkeleton.parent.href = "javascript:void(0);";
            localSkeleton.productImage.width = 30;
            localSkeleton.productImage.height = 30;
            localSkeleton.productImage.classList.add("rounded-circle", "shadow-sm", "p-1");
            localSkeleton.productName.classList.add("mb-0", "ms-2");
            localSkeleton.parent.classList.add("mt-2", "sizer", "align-items-center", "text-decoration-none");
            localSkeleton.version.classList.add("mb-0", "badge", "ms-1", "text-dark", "border", "border-secondary");

            // Set value
            localSkeleton.productImage.src = `https://raw.githubusercontent.com/AliasIO/wappalyzer/master/src/drivers/webextension/images/icons/${data.icon}`;
            localSkeleton.productName.innerText = key;
            if (versionCase) localSkeleton.version.innerText = data.version;

            localSkeleton.parent.append(
                localSkeleton.productImage,
                localSkeleton.productName
            );
            if (versionCase) localSkeleton.parent.appendChild(localSkeleton.version);
            skeleton.child.appendChild(localSkeleton.parent);
        })
        skeleton.parent.append(
            skeleton.type,
            skeleton.child
        );
        return skeleton.parent;
    }
}

window.onload = () => {
    let render = new dashboard();
    render.updateView();
    setInterval(async () => {
        await render.updateView();
    }, 3000);
}