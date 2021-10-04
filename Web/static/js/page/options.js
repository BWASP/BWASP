const MaximumRecursiveLevel = 5000;
const RecursiveLevelHandler = ["Input", "Slider"];
const patterns = {
    targetURL: ""
}
const SupportedList = {
    Server: ["Web Server", ["Apache", "Nginx"]],
    Framework: ["Framework / Libs", ["React", "AngularJS"]],
    Backend: ["Backend", ["Flask", "Django"]]
}

// Add event handler to recursive level handler
for(let i=0; i<RecursiveLevelHandler.length; i++){
    document.getElementById(`ToolRecursiveLevel${RecursiveLevelHandler[i]}`).addEventListener("change", function(){
        if(this.value>MaximumRecursiveLevel){
            alert(`Analysis recursive level cannot exceed ${MaximumRecursiveLevel}.`);
            this.value = MaximumRecursiveLevel;
        }
        document.getElementById(`ToolRecursiveLevel${RecursiveLevelHandler[+ !i]}`).value = this.value;
    });
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
            checkbox: `info-data-${Type}-${CodeName}`,
            version: `info-version-${Type}-${CodeName}`
        }
        localSkeleton.parent.classList.add("form-group", "mb-0");
        localSkeleton.child.parent.classList.add("custom-control", "custom-checkbox", "small");

        localSkeleton.child.child.checkbox.type = "checkbox";
        localSkeleton.child.child.checkbox.classList.add("custom-control-input");
        localSkeleton.child.child.checkbox.id = elementNaming.checkbox;

        localSkeleton.child.child.codename.classList.add("custom-control-label", "pt-1");
        localSkeleton.child.child.codename.htmlFor = elementNaming.checkbox;
        localSkeleton.child.child.codename.innerHTML = CodeName;

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