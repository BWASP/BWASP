// true (vector) / false (packet)
let currentState = true;
let implementationSample_attackVector = [
    {
        url: "http://bobmart.com/main.php",
        payloads: ["/class.php", "/korea.php", "/bwasp.php", "/abc.bobmart.com", "/admin.bobmart.com"],
        vulnerability: {
            type: "Cross Site Script(XSS)",
            CVE: [
                {
                    numbering: "2021-0000-111"
                }
            ]
        },
        method: "None",
        date: "2021-09-28 11:00",
        impactRate: 0
    }
];
let implementationSample_packets = [
    {
        url: "http://bobmart.com/main.php",
        payloads: ["/class.php", "/korea.php", "/bwasp.php", "/abc.bobmart.com", "/admin.bobmart.com"],
        packet: "?num= parameter check",
        vulnerability: {
            type: "Cross Site Script(XSS)",
            CVE: [
                {
                    numbering: "2021-0000-111",
                    description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
                }
            ]
        },
        method: "None",
        relatedData: ["http://xsstest123456.com/xssprob1.md"],
        date: "2021-09-28 11:00",
        impactRate: 0
    }
];

console.log

document.getElementById("switchToPacket").addEventListener("click", function(){
    currentState = !currentState;
    let status = (currentState) ? "Attack Vector" : "Packets";
    let idKeyList = [], key = "";
    let createKey = () => {
        let gen = () => {
            key = Math.random().toString(36).substring(2);
            if(!idKeyList.includes(key)) return key;
            else gen()
        }
        return `anonID-${gen()}-${gen()}`;
    }
    // for(let s=0; s<=500; s++) console.log(createKey());
    key = Math.random().toString(36).substring(2);
    document.getElementById("titleOfPage").innerHTML = status;
    document.title = `${status} - BWASP`;

    let thead = document.getElementById("parallelTableHead"),
        table = $('#dataTable'),
        newThead = document.createElement("tr"),
        newTbodyElements = [],
        element = [
            ["URL", "Vulnerability Doubt", "Method", "Date", "Impact"],
            ["URL", "Packet", "Vulnerability Doubt", "Method", "Related Data", "Date", "Impact"]
        ],
        currentData = [];

    // Build thead
    element[Number(currentState)].forEach((columnName)=>{
        let tempThElement = document.createElement("th");
        tempThElement.innerHTML = columnName;
        newThead.appendChild(tempThElement);
    });
    // render thead
    thead.innerHTML = "";
    thead.appendChild(newThead);

    // Build tbody
    let buildData = (currentState) ? implementationSample_attackVector : implementationSample_packets;
    for(let count=0; count<buildData.length; count++){
        let frame = document.createElement("tr");
        let localData = buildData[count], element = Object();
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
        element.url.child.url.href = `#${idKey}`;
        element.url.child.url.innerHTML = localData.url;
        element.url.child.url.classList.add("d-block", "py-3", "m-0", "font-weight-bold", "text-primary");

        console.log(element.url.child.url);
    }
    // tbody - essential - URL



    // Initialize datatables
    table.DataTable();



    if(currentState){
        // Attack vector

    }else{
        // Packets
    }
})