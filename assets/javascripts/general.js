function changeVersion(app, version, warn = false){
    // Sets the module load example to use the selected version
    document.getElementById("mod_" + app.toLowerCase() + "_code").innerHTML=`module load ${app}/${version}`
    document.querySelectorAll(".md-tags-ver-" + app.toLowerCase() +">.md-tag-ver-shown").forEach((e) => e.classList.remove("md-tag-ver-shown"))
    document.getElementById("mod_" + app.toLowerCase() + "_" + version).classList.add("md-tag-ver-shown")
    if (warn){
        document.getElementById("mod_" + app.toLowerCase() + "_warn").style.display = "block";
        document.getElementById("mod_" + app.toLowerCase() + "_warn").querySelector("p.warning-text").innerHTML = document.getElementById("mod_" + app.toLowerCase() + "_" + version).title;
    }else{
        document.getElementById("mod_" + app.toLowerCase() + "_warn").style.display = "none";
    }

    // ew. so gross
}
// Side-nav entries that get an icon. The key is the label exactly as it appears
// in the sidebar; the value selects --md-nav-icon--<value> in extra.css.
const NAV_ICONS = {
    "Getting Started": "start",
    "General": "general",
    "Storage": "storage",
    "Other Services": "services",
    "Training": "training",
};

function addNavIcons(){
    document.querySelectorAll(".md-nav--primary .md-nav__link").forEach((link) => {
        // On the home page the table of contents is nested inside the primary
        // nav, and it has its own "Storage" heading. Skip it.
        if (link.closest(".md-nav--secondary")){
            return;
        }
        // A section with an index page wraps its anchor and its expand toggle in
        // a .md-nav__container, which also carries .md-nav__link. Icon the
        // anchor, not the wrapper, or the entry gets two icons.
        if (link.querySelector(".md-nav__link")){
            return;
        }
        const label = link.querySelector(".md-ellipsis");
        const icon = label && NAV_ICONS[label.textContent.trim()];
        if (icon){
            link.classList.add("md-nav__link--icon", "md-nav__link--icon-" + icon);
        }
    });
}

// document$ is Material's page-load observable. It re-emits on every instant
// navigation, which rebuilds the sidebar and would otherwise drop the classes.
if (typeof document$ !== "undefined"){
    document$.subscribe(addNavIcons);
}else{
    document.addEventListener("DOMContentLoaded", addNavIcons);
}

function toggle(id){
    var item = document.getElementById(id);
    console.log(id);
    console.log(item);
    if (item){
        if (item.classList.contains("hidden"))
        {
           item.classList.remove("hidden")
        }
        else
        {
            item.classList.add("hidden")    
        }
    }else{
        console.log(item)
    }

  }
