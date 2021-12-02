// Get modules
import {API as api, createKey, createToast} from '../jHelper.js';

let API = new api(),
    requestData = {tool: Object(), info: Object(), target: Object()};

const patterns = {
        targetURL: /^http[s]?:///
    },
    disableRiskLock = new bootstrap.Modal(document.getElementById('disableRiskLock'), {
        keyboard: false,
        backdrop: 'static',
        show: true
    });


class inputHandler {
    constructor() {
        // Receive data from option handler
        this.maximum = Object();
        this.options = Object();
        this.infoTempStorage = Object();

        // Form data skeleton
        this.formData = {
            tool: {
                analysisLevel: Number(),
                optionalJobs: Array()
            },
            info: Array(),
            target: String(),
            API: {
                google: {
                    key: String(),
                    engineId: String()
                }
            },
            maximumProcess: Number()
        }
    }

    receiveData(dataPackage) {
        Object.keys(dataPackage).forEach(key => this[key] = dataPackage[key]);
    }

    pagingHandler(page) {
        console.info(JSON.stringify(this.formData));
        switch (page) {
            case 0:
                return this.validateURL({
                    targetURL: document.getElementById("input-targetURL")
                });
            case 1:
                this.inputHandling();
                return true;
            case 2:
                return this.validateOptions();
            case 3:
                this.inputHandling();
                this.validateOptions();
                this.buildSelectedOptions();
                return true;
            default:
                return false;
        }
    }

    inputHandling() {
        // Mess up known information
        this.formData.info = Array();
        Object.keys(this.infoTempStorage).forEach(libName => this.formData.info.push({
            name: libName,
            version: this.infoTempStorage[libName]
        }))

        // Render in job submission overview page
        let renderSpace = document.getElementById("overview-environment");
        renderSpace.innerHTML = "";
        this.formData.info.forEach((currentLib) => {
            let skeleton = {
                parent: document.createElement("h5"),
                info: document.createElement("span"),
                version: document.createElement("span")
            }

            skeleton.parent.classList.add("mb-0", "me-2");
            skeleton.info.classList.add("badge", "border", "border-primary", "text-dark");
            skeleton.version.classList.add("small", "text-muted", "ms-2");

            skeleton.version.innerText = currentLib.version;

            skeleton.info.append(
                currentLib.name,
                skeleton.version
            );
            skeleton.parent.appendChild(skeleton.info);

            renderSpace.appendChild(skeleton.parent);
        })
    }

    validateURL(objects) {
        let condition = patterns.targetURL.test(objects.targetURL.value);
        if (condition) {
            this.formData.target = objects.targetURL.value;
            document.getElementById("overview-targetURL").innerText = this.formData.target;
        }
        return condition;
    }

    validateOptions() {
        let objects = {
            analysisLevel: Number(document.getElementById("input-recursiveLevel").value),
            maximumProcesses: Number(document.getElementById("input-maximumProcesses").value),
            API: {
                google: {
                    key: document.getElementById("googleSearchAPI-APIKey").value,
                    engineId: document.getElementById("googleSearchAPI-engineID").value
                }
            }
        };
        let condition =
            (objects.analysisLevel <= this.maximum.recursiveLevel) &&
            (objects.maximumProcesses <= this.maximum.maximumProcesses);
        if (condition) {
            this.formData.tool.analysisLevel = objects.analysisLevel;
            document.getElementById("overview-recursiveLevel").innerText = this.formData.tool.analysisLevel;
            this.formData.maximumProcess = objects.maximumProcesses;
            document.getElementById("overview-maximumProcess").innerText = this.formData.maximumProcess;
        }
        this.formData.API.google.key = objects.API.google.key;
        document.getElementById("overview-googleSearchAPI-APIKey").innerText = objects.API.google.key;
        this.formData.API.google.engineId = objects.API.google.engineId;
        document.getElementById("overview-googleSearchAPI-engineID").innerText = objects.API.google.engineId;
        return condition;
    }

    buildSelectedOptions() {
        let renderSpace = document.getElementById("overview-options");
        renderSpace.innerHTML = "";
        this.formData.tool.optionalJobs.forEach((optionID) => {
            let currentOption = this.options[optionID];

            let skeleton = {
                parent: document.createElement("h5"),
                info: document.createElement("span")
            }

            skeleton.parent.classList.add("mb-0", "me-2");
            skeleton.info.classList.add("badge", "border", `border-${(currentOption.issue)?"danger":"primary"}`, "text-dark");

            skeleton.info.append(currentOption.display);
            skeleton.parent.appendChild(skeleton.info);

            renderSpace.appendChild(skeleton.parent);
        })
    }
}

class optionFrontHandler {
    constructor() {
        // JSON-defined data
        this.steps = Array();
        this.currentStep = Number();
        this.sliderObjects = Object();
        this.maximum = Object();
        this.supportedList = Object();
        this.options = Object();

        // Risk Lock
        this.riskLock = true;

        // Document-defined dataa
        this.elements = {
            stepName: document.getElementById("stepName"),
            stepsView: document.getElementById("stepsView")
        };

        // Input verifier
        this.inputHandler = new inputHandler();

        // Other data
        this.infoTempStorage = Object();
        this.doubleCheck = false;
    }

    disableRiskLock(type = true) {
        if (type) {
            this.riskLock = false;

            // Remove RiskLock modal
            disableRiskLock.hide();
            document.getElementById('disableRiskLock').remove();

            document.getElementById('call-disableRiskLock').classList.add("animate__animated", "animate__fadeOutRight");
            setTimeout(()=> {
                document.getElementById('call-disableRiskLock').remove()

                // Add RiskLock Disabled
                let disabledRiskLock = document.createElement("p");
                disabledRiskLock.classList.add("text-danger", "ms-2", "mb-0", "small", "fw-bold", "animate__animated", "animate__fadeInLeft");
                disabledRiskLock.innerText = "(Risk Protection Disabled)";
                document.getElementById("optionsHead").appendChild(disabledRiskLock);

                createToast("Risk Lock Disabled", "All features are now available.", "danger", false);
            }, 300);
        } else {
            disableRiskLock.show();
        }
    }

    async getOptionsConfig() {
        return await fetch("/static/data/frontRendererData/options.json")
            .then(blob => blob.json())
            .then(res => {
                Object.keys(res).forEach(key => this[key] = res[key]);
                return this;
            });
    }

    async checkAvailability() {
        let data = await API.communicateRAW("/api/job");

        // True if available
        return data.length <= 0;
    }

    changePageView(from, to) {
        console.log(from, to);
    }


    toggleButton(target, type = String()) {
        let backButton = target,
            supportedType = ["show", "hide", "toggle"];
        if ([supportedType[0], supportedType[1]].includes(type)) {
            backButton.classList.remove("d-none");
            this.swapStatus(backButton, "clearAnimation");
            switch (type) {
                case supportedType[0]:
                    backButton.classList.add("animate__animated", "animate__fadeInUp");
                    break;
                case supportedType[1]:
                    backButton.classList.add("animate__animated", "animate__fadeOutDown");
                    break;
            }
        } else {
            if (backButton.classList.contains("animate__animated")) this.toggleButton("show");
            else this.toggleButton("hide");
        }
    }

    updateStepTitle(title) {
        let titleElement = document.getElementById("stepName");
        titleElement.innerText = title;
        this.swapStatus(titleElement, "clearAnimation");
        titleElement.classList.add("animate__animated", "animate__fadeInDown", "animate__fast");
        setTimeout(() => {
            this.swapStatus(titleElement, "clearAnimation");
        }, 600);
    }

    async initPagingView() {
        let availability = await this.checkAvailability();

        // Return if job queued.
        this.swapStatus(document.getElementById("tab-availabilityCheck"), "hide");
        if (!availability) {
            this.swapStatus(document.getElementById("tab-availabilityCheck-fail"), "show");
            return;
        }

        // Open Analysis target view
        setTimeout(() => {
            ["document-top", "document-bottom", "tab-0"].forEach((currentElement) => {
                this.swapStatus(document.getElementById(currentElement), "show");
            })
        }, 300);

        // Match slider and inputs
        Object.keys(this.sliderObjects).forEach((currentKey) => {
            let types = ["input", "slider"],
                currentObject = this.sliderObjects[currentKey];
            for (let index = 0; index < types.length; index++) {
                let localTargets = [
                        document.getElementById(`${types[index]}-${currentKey}`),
                        document.getElementById(`${types[+!index]}-${currentKey}`)
                    ],
                    currentTargetDetail = {
                        message: currentObject.message,
                        initial: currentObject.initial,
                        minimum: currentObject.minimum,
                        maximum: this.maximum[currentKey]
                    }
                localTargets.forEach((currentTarget) => {
                    currentTarget.value = currentTargetDetail.initial;
                    currentTarget.min = currentTargetDetail.minimum;
                    currentTarget.max = currentTargetDetail.maximum;
                })
                localTargets[0].addEventListener("change", function () {
                    if (this.value > currentTargetDetail.maximum) {
                        alert(`${currentTargetDetail.message} ${currentTargetDetail.maximum}.`);
                        this.value = currentTargetDetail.maximum;
                    }
                    localTargets[1].value = this.value;
                });
            }
        })

        // Open
        document.getElementById("maximumRecursiveLevel").innerText = this.maximum.recursiveLevel;
        document.getElementById("maximumProcessesView").innerText = this.maximum.maximumProcesses;
    }

    getDataById(key) {
        return this[key];
    }

    swapStatus(targetObject, type = "toggle") {
        let hideObjClass = "d-none";
        if (type === "toggle") {
            if (targetObject.classList.contains(hideObjClass)) targetObject.classList.remove(hideObjClass);
            else targetObject.classList.add(hideObjClass);
        } else if (type === "hide") {
            targetObject.classList.add(hideObjClass);
        } else if (type === "show") {
            targetObject.classList.remove(hideObjClass);
        } else if (type === "clearAnimation") {
            let className = String();
            targetObject.classList.value.split(" ")
                .filter(classes => !classes.includes("animate__"))
                .forEach((currentClass) => {
                    className += `${currentClass} `;
                })
            targetObject.className = className.slice(0, -1);
        } else {
            console.error("Error:: Unable to catch code order");
        }
    }

    buildStepBreadCrumbs() {
        let localCount = 0;
        this.steps.forEach((step) => {
            let localSkeleton = {
                parent: document.createElement("li"),
                child: document.createElement("a")
            }
            localSkeleton.parent.classList.add("breadcrumb-item", "active");
            localSkeleton.child.setAttribute("open-page", String(localCount));
            localSkeleton.child.classList.add("text-decoration-none");
            if (localCount >= 1) localSkeleton.child.classList.add("text-muted");
            localSkeleton.child.id = `step-${localCount}`
            localSkeleton.child.href = "#";
            localSkeleton.child.innerText = step["subtitle"];

            localSkeleton.child.addEventListener("click", (event) => {
                this.swapPage(this.currentStep, Number(event.target.getAttribute("open-page")));
            })

            localSkeleton.parent.appendChild(localSkeleton.child);
            this.elements.stepsView.appendChild(localSkeleton.parent);
            localCount++;
        })
    }

    buildOptions() {
        const buildSelectOption = (dataPackage) => {
            let localSkeleton = {
                parent: document.createElement("div"),
                subParent: document.createElement("div"),
                child: {
                    checkbox: document.createElement("input"),
                    label: document.createElement("label")
                }
            }
            let currentElementID = createKey(2, "listElement");

            // Set Attributes
            localSkeleton.parent.classList.add("col-md-3");
            localSkeleton.subParent.classList.add("form-check");
            localSkeleton.child.checkbox.classList.add("form-check-input");
            localSkeleton.child.checkbox.setAttribute("type", "checkbox");
            localSkeleton.child.checkbox.id = currentElementID;
            localSkeleton.child.checkbox.value = dataPackage.optionID;
            localSkeleton.child.label.classList.add("form-check-label");
            if(dataPackage.issue) localSkeleton.child.label.classList.add("text-danger");
            localSkeleton.child.label.htmlFor = currentElementID;
            localSkeleton.child.label.innerText = dataPackage.display;

            // Event listener
            localSkeleton.child.checkbox.addEventListener("change", () => {
                let condition = localSkeleton.child.checkbox.checked;
                if(dataPackage.issue && this.riskLock) {
                    localSkeleton.child.checkbox.checked = false;
                    return createToast("Option restricted", `You must disable Risk Lock before select this option (${dataPackage.display})`, "danger", false);
                }
                if(condition) this.inputHandler.formData.tool.optionalJobs.push(dataPackage.optionID);
                else {
                    let targetIndex = this.inputHandler.formData.tool.optionalJobs.indexOf(dataPackage.optionID);
                    if(targetIndex === -1) return createToast("Data processing error", "Can't find index of string in array", "danger", false);
                    else this.inputHandler.formData.tool.optionalJobs.splice(targetIndex, 1);
                }
            });

            // Assemble parts to parent
            localSkeleton.subParent.append(
                localSkeleton.child.checkbox,
                localSkeleton.child.label
            );
            localSkeleton.parent.appendChild(localSkeleton.subParent);

            // return object
            return localSkeleton.parent;
        }
        let viewPlace = document.getElementById("optionsViewPlace");
        viewPlace.innerHTML = "";
        Object.keys(this.options).forEach((optionID) => {
            viewPlace.appendChild(buildSelectOption({
                optionID: optionID,
                display: this.options[optionID].display,
                issue: this.options[optionID].issue
            }));
        })
    }


    async buildSupportedList() {
        let counter = Number();
        this.supportedList = await fetch("/static/data/supportedList.json")
            .then(blob => {
                return blob.json()
            });
        const buildTitle = (title) => {
            let localTitle = document.createElement("h2");
            localTitle.classList.add("fw-bold", "col-md-12", "mb-2");
            localTitle.innerText = title;

            return localTitle;
        }
        const buildSubTitle = (title) => {
            let skeleton = {
                parent: document.createElement("h5"),
                icon: document.createElement("i")
            }
            skeleton.parent.classList.add("col-md-12", "mt-3", "mb-1", "text-muted", "text-capitalize");
            skeleton.icon.classList.add("bi", "bi-forward");
            skeleton.parent.append(
                skeleton.icon,
                ` ${title}`
            )

            return skeleton.parent;
        }
        const buildSelectOption = (libName) => {
            let localSkeleton = {
                parent: document.createElement("div"),
                subParent: document.createElement("div"),
                child: {
                    checkbox: document.createElement("input"),
                    label: document.createElement("label"),
                    versionInput: document.createElement("input")
                }
            }
            let currentElementID = {
                element: createKey(2, "listElement")
            };
            currentElementID["version"] = `${currentElementID}-version`;

            // Set Attributes
            localSkeleton.parent.classList.add("col-md-3", "pb-1", "pt-1", "d-flex", "align-items-center");
            localSkeleton.subParent.classList.add("form-check");
            localSkeleton.child.checkbox.classList.add("form-check-input");
            localSkeleton.child.checkbox.setAttribute("type", "checkbox");
            localSkeleton.child.checkbox.id = currentElementID.element;
            localSkeleton.child.label.classList.add("form-check-label");
            localSkeleton.child.label.htmlFor = currentElementID.element;
            localSkeleton.child.label.innerText = libName;
            localSkeleton.child.versionInput.classList.add("rounded-custom", "border", "ps-2", "w-100", "d-none");
            localSkeleton.child.versionInput.placeholder = "Version";
            localSkeleton.child.versionInput.id = currentElementID.version

            // Add event listener to checkbox object
            localSkeleton.child.checkbox.addEventListener("change", () => {
                let condition = localSkeleton.child.checkbox.checked;

                if (condition) this.inputHandler.infoTempStorage[libName] = String();
                else delete this.inputHandler.infoTempStorage[libName];

                localSkeleton.child.versionInput.classList[(condition) ? "remove" : "add"]("d-none");
                if (!condition) localSkeleton.child.versionInput.value = "";
            })

            localSkeleton.child.versionInput.addEventListener("change", () => {
                if (localSkeleton.child.checkbox.checked) {
                    this.inputHandler.infoTempStorage[libName] = localSkeleton.child.versionInput.value;
                }
                console.log(this.inputHandler.infoTempStorage);
            })

            // Assemble parts to parent
            localSkeleton.subParent.append(
                localSkeleton.child.checkbox,
                localSkeleton.child.label,
                localSkeleton.child.versionInput
            );
            localSkeleton.parent.appendChild(localSkeleton.subParent);

            // Add counter
            counter += 1;

            // return object
            return localSkeleton.parent;
        }

        Object.keys(this.supportedList).forEach((currentKey) => {
            let currentList = this.supportedList[currentKey],
                currentSection = document.createElement("section");

            // Configure section
            currentSection.classList.add("row");

            // Build title
            currentSection.appendChild(buildTitle(currentKey));

            // If array
            if (Array.isArray(currentList)) {
                currentList.forEach((currentData) => {
                    currentSection.appendChild(buildSelectOption(currentData));
                })
            } else {
                Object.keys(currentList).forEach((currentSubTitle) => {
                    currentSection.appendChild(buildSubTitle(currentSubTitle));
                    currentList[currentSubTitle].forEach((currentData) => {
                        currentSection.appendChild(buildSelectOption(currentData));
                    })
                })
            }

            let divider = document.createElement("hr");
            divider.classList.add("col-md-12", "mt-4", "mb-4");
            currentSection.appendChild(divider);

            document.getElementById("sampleHere").appendChild(currentSection);
        })
        // createToast("Successfully Rendered", `Loaded ${counter.toLocaleString()} libs.`)
    }

    movePage(forward = true) {
        let page = {
            current: this.currentStep,
            next: this.currentStep + ((forward) ? 1 : -1)
        };

        if ((page.next > this.steps.length - 1)) return createToast("optionFrontHandler.movePage()", "Request page index out of range", "danger");

        // Swap page if not triggered.
        this.swapPage(page.current, page.next);
    }

    swapPage(from, to, force = false, isFromBreadCrumb = false) {
        let buttons = {
            submit: document.getElementById("document-bottom-submit"),
            proceed: document.getElementById("document-bottom-next")
        };
        // If target step(page) is out of range (of JSON file index)
        if (to > this.steps.length - 1 && !force) return createToast("Error", "Request page index out of range", "danger");
        // If input values in current page got an error
        else if (!this.inputHandler.pagingHandler(from) && !force) return createToast("Error", "Value error occurred in current page", "danger");
        // If requested same page as currently presented.
        else if (this.currentStep === to && !force) return createToast("Notice", "Requested same page (Current view)", "primary");

        if(to === this.steps.length - 1) {
            this.inputHandler.pagingHandler(to);
            buttons.submit.classList.remove("d-none");
            buttons.proceed.classList.add("d-none");
        }else{
            buttons.submit.classList.add("d-none");
            buttons.proceed.classList.remove("d-none");
        }

        // Show back button
        this.toggleButton(document.getElementById("document-bottom-back"), (to > 0) ? "show" : "hide");
        let pageView = {
            current: document.getElementById(`tab-${from}`),
            next: document.getElementById(`tab-${to}`)
        };

        // Update current step title with animation
        this.updateStepTitle(this.steps[to].title);

        // Clear and add fade out animation
        this.swapStatus(pageView.current, "clearAnimation");
        this.swapStatus(pageView.next, "clearAnimation");
        pageView.current.classList.add("animate__animated", `animate__${(from > to) ? "fadeOutRight" : "fadeOutLeft"}`, "animate__fast");
        pageView.next.classList.add("animate__animated", `animate__${(from > to) ? "fadeInLeft" : "fadeInRight"}`, "animate__fast");

        // Open next tab
        setTimeout(() => {
            pageView.current.classList.add("d-none");
            pageView.next.classList.remove("d-none");
        }, 500)

        // Update current page
        this.currentStep = to;
    }

    submitForm() {
        fetch("/automation/options", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            },
            body: new URLSearchParams({
                reqJsonData: JSON.stringify(this.inputHandler.formData)
            })
        }).then(() => console.log("Done"));

        createToast("Job submitted", "Redirecting you to dashboard", "success", false, 3);
        setTimeout(() => {
            document.location.replace("/dashboard");
        }, 3000);
    }

    sendConfigToHandler(dataPackage) {
        this.inputHandler.receiveData({
            maximum: dataPackage.maximum,
            options: dataPackage.options
        })
    }
}

let handler = new optionFrontHandler();

// Define classes

// Initialize frontend when load
window.onload = async () => {

    // Set event listener
    document.getElementById("document-bottom-next").addEventListener("click", () => {
        handler.movePage();
    })
    document.getElementById("document-bottom-submit").addEventListener("click", () => {
        handler.submitForm();
    })
    document.getElementById("document-bottom-back").addEventListener("click", () => {
        handler.movePage(false);
    })
    document.getElementById("call-disableRiskLock").addEventListener("click", () => {
        handler.disableRiskLock(false);
    })
    document.getElementById("unlockRiskLock").addEventListener("click", () => {
        handler.disableRiskLock(true);
    })

    // Create front
    handler.getOptionsConfig().then(async (dataPackage) => {
        await handler.sendConfigToHandler(dataPackage);
        await handler.initPagingView();
        await handler.buildStepBreadCrumbs(
            handler.elements,
            handler.steps
        )
        await handler.buildSupportedList();
        await handler.buildOptions();
    })
}