const MaximumRecursiveLevel = 5000;
const RecursiveLevelHandler = ["Input", "Slider"];

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