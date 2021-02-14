function make_summary() {
    let summary_form = document.forms['summaryform']

    let summary = summary_form['originaltext'].value;
    let sent_length = summary_form['sentlength'].value

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            json_response = JSON.parse(this.response)
            summary_form['summarizedtext'].value = json_response['summary'];
            summary_form['inputlength'].value = json_response['input_length'];
        }
    };

    form_data = { 'originaltext': summary, 'sentlength': sent_length }
    xhttp.open('POST', '/make_summary', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify(form_data));
}
