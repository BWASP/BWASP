// Get modules
import {API as api} from '../jHelper.js';

// Define API Endpoints
const APIEndpoints = {
    webEnvironments: "/api/systeminfo"
}

let API = await new api();

class dashboard {
    updateView() {
        this.webEnvironments();
        this.updatePacketCount();
        this.updateThreatsCount();
        this.updatePortsCount();
    }

    updatePacketCount() {
        API.communicate("/api/packet/automation/count", (autoErr, automationCount) => {
            API.communicate("/api/packet/manual/count", (manualErr, manualCount) => {
                if (autoErr || manualErr) setTimeout(() => {
                    return this.updatePacketCount();
                }, 500);
                else document.getElementById("receivedPacketsCount").innerText = automationCount.count + manualCount.count;
            })
        })
    }

    updateThreatsCount() {
        API.communicate("/api/domain/count", (err, res) => {
            if (err) setTimeout(() => {
                return this.updateThreatsCount();
            }, 500);
            else document.getElementById("detectedThreatsCount").innerText = res.count;
        })
    }

    updatePortsCount() {
        API.communicate("/api/ports/count", (err, res) => {
            if (err) setTimeout(() => {
                return this.updatePortsCount();
            }, 500);
            else document.getElementById("openedPortsCount").innerText = res.count;
        })
    }

    webEnvironments() {
        API.communicate(
            APIEndpoints.webEnvironments + "/1",
            (err, res) => {
                if (err) {
                    return window.setTimeout(() => {
                        this.webEnvironments();
                    }, 500);
                } else res = {
                    target: res[0].url,
                    data: JSON.parse(res[0].data)
                };

                document.getElementById("webEnvURLPlace").innerText = res.target;
                document.getElementById("webEnvDataPlace").innerHTML = "";
                Object.keys(res.data).forEach((key) => {
                    document.getElementById("webEnvDataPlace").appendChild(this.buildWebEnvCard(key, res.data[key]));
                });

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