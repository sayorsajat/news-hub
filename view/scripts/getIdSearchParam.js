export function getDashboardId() {
    let params = new URL(document.location).searchParams;
    if(params.size){
        return params.get("id");
    } else {
        return "";
    }

}