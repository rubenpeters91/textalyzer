"use strict";

async function make_summary() {
    document.getElementById('summary-spinner').style.display = '';
    let summary_form = document.forms['summaryform'];
    let summary = summary_form['originaltext'].value;
    let sent_length = summary_form['sentlength'].value;
    let language = summary_form['setlanguage'].value;

    const form_data = { 'originaltext': summary, 'sentlength': sent_length, 'language': language };
    let response = await fetch('/make_summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(form_data)
    });

    document.getElementById('summary-spinner').style.display = 'none';
    if (response.ok) {
        let json_response = await response.json();
        summary_form['summarizedtext'].value = json_response['summary'];
        summary_form['inputlength'].value = json_response['input_length'];
    } else {
        summary_form['summarizedtext'].value = 'Something went wrong...';
    }
}
