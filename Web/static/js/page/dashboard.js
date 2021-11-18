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
        this.ports = Object();
    }

    updateView() {
        this.webEnvironments();
        this.updatePacketCount();
        this.updateThreatsCount();
        this.updatePorts();
        this.updateAnalysisLevel();
    }

    updatePacketCount() {
        API.communicate("/api/packet/automation/count", (autoErr, automationCount) => {
            API.communicate("/api/packet/manual/count", (manualErr, manualCount) => {
                if (!autoErr && !manualErr) document.getElementById("receivedPacketsCount").innerText = automationCount.count + manualCount.count;
            })
        })
    }

    updateThreatsCount() {
        API.communicate("/api/domain/count", (err, res) => {
            if (!err) document.getElementById("detectedThreatsCount").innerText = res.count;
        })
    }

    updatePorts() {
        let localPorts = Object();

        // Port count
        API.communicate("/api/ports/count", (err, res) => {
            let targets = [
                document.getElementById("portCountViewPlace"),
                document.getElementById("openedPortsCount")
            ]
            if (!err) targets.forEach((currentTarget) => currentTarget.innerText = res.count);
        })

        // Ports
        API.communicate("/api/ports", (err, res) => {
            if (err) return;
            else {
                res.forEach((currentPort) => {
                    if (currentPort.result === "Open") {
                        if (!Object.keys(localPorts).includes(currentPort["service"]))
                            localPorts[currentPort["service"]] = Array();
                        if (currentPort.port !== "None") localPorts[currentPort["service"]].push(currentPort.port)
                    }
                })
                document.getElementById("portViewPlace-detail").classList.remove("d-none");
                document.getElementById("portViewPlace-noData").classList.add("d-none");
            }
            if (JSON.stringify(this.ports) !== JSON.stringify(localPorts)) {
                // Save ports data
                this.ports = localPorts;

                // Initialize opened ports DOM
                let portView = document.getElementById("portViewPlace");
                portView.innerHTML = "";

                // Build
                console.log(localPorts);
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
                })
            }
        })
    }

    updateAnalysisLevel() {
        API.communicate("/api/job/1", (err, res) => {
            if (!err) document.getElementById("analysisLevelView").innerText = res[0].recursiveLevel;
        })
    }

    webEnvironments() {
        API.communicate(
            APIEndpoints.webEnvironments + "/1",
            (err, res) => {
                if (err) return;
                else {
                    let localObject = {
                        target: res[0].url,
                        data: JSON.parse(res[0].data)
                    }

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
                }
            })
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
    setInterval(() => {
        render.updateView();
    }, 2500);
}