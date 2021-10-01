const MaximumRecursiveLevel = 5000;
const RecursiveLevelHandler = ["Input", "Slider"];
const SupportedList = {
    Server: ["웹 서버", ["Apache", "Nginx"]],
    Framework: ["웹 프레임워크 / 라이브러리", ["React", "AngularJS"]],
    Backend: ["백엔드 시스템", ["Flask", "Django"]]
}

// Add event handler to recursive level handler
for(let i=0; i<RecursiveLevelHandler.length; i++){
    document.getElementById(`ToolRecursiveLevel${RecursiveLevelHandler[i]}`).addEventListener("change", function(){
        if(this.value>MaximumRecursiveLevel){
            alert(`탐색 깊이는 ${MaximumRecursiveLevel}회를 넘을 수 없습니다.`);
            this.value = MaximumRecursiveLevel;
        }
        document.getElementById(`ToolRecursiveLevel${RecursiveLevelHandler[+ !i]}`).value = this.value;
    });
}

document.getElementById("ClearAllData").addEventListener("click", function(){
    let data = document.getElementsByTagName("input");
    Object.keys(data).forEach(function(key){
        switch(data[key].type){
            case "text":
                data[key].value="";
                break;
            case "number":
            case "range":
                data[key].value="1";
                break;
            case "checkbox":
                data[key].checked=false;
                break;
            default:
                alert("핸들되지 않은 개체가 있습니다.");
        }
    });
})

// Frontend constructor
Object.keys(SupportedList).forEach((Type)=>{
    let toggleTabName = `Web${Type}Selection`;
    console.log(SupportedList[Type][0]);
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
        localSkeleton.parent.classList.add("form-group", "mb-0");
        localSkeleton.child.parent.classList.add("custom-control", "custom-checkbox", "small");

        localSkeleton.child.child.checkbox.type = "checkbox";
        localSkeleton.child.child.checkbox.classList.add("custom-control-input");
        localSkeleton.child.child.checkbox.id = `Info-Web-${Type}-${CodeName}`;

        localSkeleton.child.child.codename.classList.add("custom-control-label", "pt-1");
        localSkeleton.child.child.codename.htmlFor = `Info-Web-${Type}-${CodeName}`;
        localSkeleton.child.child.codename.innerHTML = `${CodeName} v.`;

        localSkeleton.child.child.versionInput.placeholder = "버전 (선택)";
        localSkeleton.child.child.versionInput.classList.add("border", "border-white", "w-50")
        localSkeleton.child.child.versionInput.type = "text";
        localSkeleton.child.child.versionInput.id = `Info-Web-${Type}-Version-${CodeName}`;

        localSkeleton.child.child.codename.appendChild(localSkeleton.child.child.versionInput);
        localSkeleton.child.parent.append(localSkeleton.child.child.checkbox, localSkeleton.child.child.codename);

        console.log("=====");
        console.log(localSkeleton.child.parent);
        console.log(CodeName);
        console.log("=====");
        Skeleton.child.child.content.child.appendChild(localSkeleton.child.parent);
    })

    // Append all skeletons to each parent
    Skeleton.child.child.toggleTab.appendChild(Skeleton.child.child.toggleTabText);
    Skeleton.child.child.content.parent.appendChild(Skeleton.child.child.content.child);
    Skeleton.child.parent.append(Skeleton.child.child.toggleTab, Skeleton.child.child.content.parent);
    Skeleton.parent.appendChild(Skeleton.child.parent);
    console.log(Skeleton.parent);
    document.getElementById("Section-WebAppInfo").appendChild(Skeleton.parent);
})