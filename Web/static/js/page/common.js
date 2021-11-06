let versionCheckModal = new bootstrap.Modal(document.getElementById('versionModal'), {
    show: true
});

let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

document.getElementById("BWASP-Version").addEventListener("click", ()=>{
    versionCheckModal.show();
})