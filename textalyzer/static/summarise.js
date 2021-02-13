document.addEventListener('DOMContentLoaded', () => {
    let summary_form = document.forms['summaryform']

    summary_form.addEventListener('submit', (event) => {
        let summary = summary_form['originaltext'].value;
        let percslider = summary_form['percslider'].value

        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                summary_form['summarizedtext'].innerHTML = this.responseText;
            }
        };

        form_data = { 'originaltext': summary, 'percslider': percslider }
        xhttp.open('POST', '/make_summary', true);
        xhttp.setRequestHeader('Content-type', 'application/json');
        xhttp.send(JSON.stringify(form_data));
        event.preventDefault();
    });
})
