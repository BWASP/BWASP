// Get modules
import {Cookies, createToast} from '../jHelper.js';

let cookies = new Cookies(),
    initialFrontConfig = {
        dashboard: {
            refreshRate: 3,
            stopRequestWhenFailed: false
        }
    },
    frontConfig = Object(),
    targetCookieName = "frontConfig";

// Get frontend config data from cookie
while(true){
    frontConfig = cookies.read(targetCookieName);

    try{
        frontConfig = JSON.parse(frontConfig);
    }catch {
        // createToast("Config validation fail", "Config JSON structure has corrupted.\nDeleted config", "danger");
    }
    console.log(frontConfig);

    if(typeof(frontConfig) === "object") break;
    else {
        // createToast("Front config not found", "Generating with initial options");
        cookies.create(targetCookieName, JSON.stringify(initialFrontConfig));
    }
}

// Auto-activated Sidebar
(() => {
    if(window.location.pathname === "/") return;
    let side = {
        uri: window.location.pathname.split("/"),
        target: "target"
    };
    side.uri.splice(0, 1);
    side.uri.forEach(data => side.target += `-${data}`);

    try{
        document.getElementById(side.target).classList.add("active");
    }catch (e){
        console.error(e);
    }
})();