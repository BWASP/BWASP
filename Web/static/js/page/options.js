
const MaximumRecursiveLevel = 5000;
const patterns = {
    targetURL: /^http[s]?:\/\//
}
const identifier = {
    optionalFunctions: "optFnc",
    webAppInfo: {
        name: "webAppName",
        version: "webAppVersion"
    }
}
const SupportedList = {
    Server: ["Web Server", [["Apache", "apache"], ["Nginx", "nginx"]]],
    Framework: ["Framework / Libs", [["React", "react"], ["Angular.JS", "angularjs"]]],
    Backend: ["Backend", [["Flask", "flask"], ["Django", "django"]]]
}

// Initialize frontend when load
window.onload = () => {
    // Add event handler to recursive level handler
    let RecursiveLevelHandler = ["Input", "Slider"];
    for(let i=0; i<RecursiveLevelHandler.length; i++){
        document.getElementById(`ToolRecursiveLevel${RecursiveLevelHandler[i]}`).addEventListener("change", function(){
            if(this.value>MaximumRecursiveLevel){
                alert(`Analysis recursive level cannot exceed ${MaximumRecursiveLevel}.`);
                this.value = MaximumRecursiveLevel;
            }
            document.getElementById(`ToolRecursiveLevel${RecursiveLevelHandler[+ !i]}`).value = this.value;
        });
    }
}

document.getElementById("ClearAllData").addEventListener("click", function(){
    let data = document.getElementsByTagName("input");
    Object.keys(data).forEach(function(element){
        switch(data[element].type){
            case "text":
                data[element].value="";
                break;
            case "number":
            case "range":
                data[element].value="1";
                break;
            case "checkbox":
                data[element].checked=false;
                break;
            default:
                alert("Exception: Unhandled object present.");
        }
        if(data[element].id.startsWith("info-version")){
            data[element].classList.add("d-none");
        }
    });
})

// Frontend constructor
Object.keys(SupportedList).forEach((Type)=>{
    let toggleTabName = `web${Type}Selection`;
    let Skeleton = {
        parent: document.createElement("div"),
        child: {
            parent: document.createElement("div"),
            child: {
                toggleTab: document.createElement("a"),
                toggleTabText: document.createElement("h6"),
                content: {
                    parent: document.createElement("div"),
                    child: document.createElement("div")
                }
            }
        }
    }

    // Set attributes.
    Skeleton.parent.classList.add("col-md-4");
    Skeleton.child.parent.classList.add("card", "mb-4");

    Skeleton.child.child.toggleTab.href = `#${toggleTabName}`;
    Skeleton.child.child.toggleTab.classList.add("d-block", "card-header", "py-3");
    Skeleton.child.child.toggleTab.setAttribute("data-toggle", "collapse");
    Skeleton.child.child.toggleTab.setAttribute("role", "button");
    Skeleton.child.child.toggleTab.setAttribute("aria-expanded", "false");
    Skeleton.child.child.toggleTab.setAttribute("aria-controls", toggleTabName);

    Skeleton.child.child.toggleTabText.classList.add("m-0", "font-weight-bold", "text-primary");
    Skeleton.child.child.toggleTabText.innerHTML = SupportedList[Type][0];

    Skeleton.child.child.content.parent.classList.add("collapse");
    Skeleton.child.child.content.parent.id=toggleTabName;

    Skeleton.child.child.content.child.classList.add("card-body");

    // Create checkbox input
    SupportedList[Type][1].forEach((CodeName)=>{
        let localSkeleton = {
            parent: document.createElement("div"),
            child: {
                parent: document.createElement("div"),
                child: {
                    checkbox: document.createElement("input"),
                    codename: document.createElement("label"),
                    versionInput: document.createElement("input")
                }
            }
        }
        let elementNaming = {
            checkbox: `${identifier.webAppInfo.name}-${Type}-${CodeName[1]}`,
            version: `${identifier.webAppInfo.version}-${Type}-${CodeName[1]}`
        }
        localSkeleton.parent.classList.add("form-group", "mb-0");
        localSkeleton.child.parent.classList.add("custom-control", "custom-checkbox", "small");

        localSkeleton.child.child.checkbox.type = "checkbox";
        localSkeleton.child.child.checkbox.classList.add("custom-control-input");
        localSkeleton.child.child.checkbox.value = CodeName[1];
        localSkeleton.child.child.checkbox.id = elementNaming.checkbox;

        localSkeleton.child.child.codename.classList.add("custom-control-label", "pt-1");
        localSkeleton.child.child.codename.htmlFor = elementNaming.checkbox;
        localSkeleton.child.child.codename.innerHTML = CodeName[0];
        localSkeleton.child.child.codename.id = `${elementNaming.checkbox}-label`

        localSkeleton.child.child.versionInput.placeholder = "(Version)";
        localSkeleton.child.child.versionInput.classList.add("border", "border-white", "w-50", "pl-1", "d-none")
        localSkeleton.child.child.versionInput.type = "text";
        localSkeleton.child.child.versionInput.id = elementNaming.version;

        // Add Event Listener for checkbox - to - version control input.
        localSkeleton.child.child.checkbox.addEventListener("change", function(){
            let versionInput = document.getElementById(elementNaming.version);
            versionInput.classList[(!this.checked)?"add":"remove"]("d-none");
            versionInput.focus();
        })

        localSkeleton.child.child.codename.appendChild(localSkeleton.child.child.versionInput);
        localSkeleton.child.parent.append(localSkeleton.child.child.checkbox, localSkeleton.child.child.codename);
        Skeleton.child.child.content.child.appendChild(localSkeleton.child.parent);
    })

    // Append all skeletons to each parent
    Skeleton.child.child.toggleTab.appendChild(Skeleton.child.child.toggleTabText);
    Skeleton.child.child.content.parent.appendChild(Skeleton.child.child.content.child);
    Skeleton.child.parent.append(Skeleton.child.child.toggleTab, Skeleton.child.child.content.parent);
    Skeleton.parent.appendChild(Skeleton.child.parent);
    document.getElementById("section-webAppInfo").appendChild(Skeleton.parent);
})

/***
 * Renderer of HTML ul element.
 * @param target Target element
 * @param dataPackage Text array
 */
let renderULElement = (target, dataPackage) => {
    let skeleton = document.createElement("ul");
    skeleton.classList.add("pl-3", "mb-0");
    dataPackage.forEach((path)=>{
        let localSkeleton = [document.createElement("li"), document.createElement("code")];
        localSkeleton[1].innerHTML = path;
        localSkeleton[0].appendChild(localSkeleton[1]);
        skeleton.appendChild(localSkeleton[0]);
    })
    target.innerHTML = "";
    target.appendChild(skeleton);
}

// Handler for submit check modal
document.getElementById("submitJobRequest").addEventListener("click", function(){
    let formData = document.getElementsByTagName("input"),
        optionalJobs = [],
        webAppInfo = {types: ["Server", "Framework", "Backend"], server:[], framework:[], backend:[], renderData: {}},
        requestData = {tool: Object(), info: Object(), target: Object()},
        renderTmpStorage = {};

    // Target URL
    requestData.target["url"] = document.getElementById("target-url").value;
    if(patterns.targetURL.test(requestData.target.url)===false) {
        return document.getElementById("regexViolence-targetURL").classList.remove("d-none");
    }else {
        document.getElementById("regexViolence-targetURL").classList.add("d-none");
        document.getElementById("modal-tool-targetURL").innerHTML = requestData.target.url;
    }

    // Pre-defined URL Path
    requestData.target["path"] = document.getElementById("target-urlPath").value.replaceAll(" ", "").split(",");
    if(requestData.target.path.length > 0){
        renderULElement(document.getElementById("modal-tool-URLPath"), requestData.target.path);
    }

    // Analysis recursive level
    requestData.tool["analysisLevel"] = document.getElementById("ToolRecursiveLevelSlider").value;
    if(isNaN(requestData["tool"]["analysisLevel"])) {
        return alert("Error!");
    }else{
        document.getElementById("modal-tool-analysisLevel").innerHTML = requestData.tool.analysisLevel;
    }

    // Optional functions
    requestData.tool["optionalJobs"] = [];
    Object.keys(formData).forEach((index)=>{
        if(formData[index].id.split("-")[0]===identifier.optionalFunctions && formData[index].checked){
            optionalJobs.push([formData[index].value, document.getElementById(formData[index].id+"-label").innerHTML]);
        }
    })
    if(optionalJobs.length>0) {
        let tmp = [];
        optionalJobs.forEach((data) => {
            requestData.tool.optionalJobs.push(data[0]);
            tmp.push(data[1]);
        });
        renderULElement(document.getElementById("modal-tool-options"), tmp);
    }

    // Get webapp information input
    renderTmpStorage = {};

    webAppInfo.types.forEach((type)=>{
        requestData.info[type.toLowerCase()] = Array();
        let tempStorage = [];
        Object.keys(formData).forEach((index)=>{
            let keySet = formData[index].id.split("-");
            if(keySet[0]===identifier.webAppInfo.name && keySet[1]===type && formData[index].checked) {
                let localDataset = {
                    name: formData[index].value,
                    version: document.getElementById(`${identifier.webAppInfo.version}-${type}-${formData[index].value}`).value
                }
                requestData.info[type.toLowerCase()].push(localDataset)
                tempStorage.push(document.getElementById(formData[index].id + "-label").innerText.concat((localDataset.version.length>0)?` (Version: ${localDataset.version})`:""));
            }
        })
        console.log(tempStorage);
        if(tempStorage.length > 0) renderULElement(document.getElementById(`modal-info-${type.toLowerCase()}`), tempStorage);
    })

    $("#jobSubmitVerifyModal").modal({
        backdrop: 'static',
        show: true
    })
    alert(JSON.stringify(requestData));
})