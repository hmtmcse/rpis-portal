jQuery(document).ready(function () {
    PWeb.viewMode.init()
    const element = document.getElementsByClassName("active")[0];
    if (element) {
        element.scrollIntoView({behavior: "smooth", block: "end", inline: "nearest"});
    }

    jQuery('.delete-confirmation').confirm({
        title: 'Confirmation!',
        content: 'Are you sure want to delete?'
    });

    jQuery('.cancel-confirmation').confirm({
        title: 'Confirmation!',
        content: 'Are you sure want to cancel?'
    });

    jQuery('.add-datepicker').datepicker({
        format: 'dd/mm/yyyy',
    });

    jQuery('.searchable-select').select2({
        theme: "bootstrap-5",
    });
});