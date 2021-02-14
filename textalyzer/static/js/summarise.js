function make_summary() {
    let summary_form = document.forms['summaryform']

    let summary = summary_form['originaltext'].value;
    let sent_length = summary_form['sentlength'].value
    let language = summary_form['setlanguage'].value

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState < 4) {
            document.getElementById('summary-spinner').style.display = ''
        } else {
            document.getElementById('summary-spinner').style.display = 'none'
            if (this.readyState == 4 && this.status == 200) {
                json_response = JSON.parse(this.response)
                summary_form['summarizedtext'].value = json_response['summary'];
                summary_form['inputlength'].value = json_response['input_length'];
            } else {
                summary_form['summarizedtext'].value = 'Something went wrong...';
            }
        }
    };

    form_data = { 'originaltext': summary, 'sentlength': sent_length, 'language': language }
    xhttp.open('POST', '/make_summary', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify(form_data));
}
