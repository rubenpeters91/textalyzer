"use strict";

async function random_wiki() {
    document.getElementById('wikispinner').style.display = '';
    const form = document.forms[0]
    let response = await fetch('/random_wiki');

    document.getElementById('wikispinner').style.display = 'none';
    if (response.ok) {
        let json_response = await response.json();
        form['originaltext'].value = json_response['wiki_page'];
    } else {
        form['originaltext'].value = 'Something went wrong...';
    }
}
