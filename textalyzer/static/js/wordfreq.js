function make_wordfreq() {
    let wordfreq_form = document.forms['keywordform']

    let originaltext = wordfreq_form['originaltext'].value;
    let max_terms = wordfreq_form['maxterms'].value
    let language = wordfreq_form['setlanguage'].value

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState < 4) {
            document.getElementById('wordfreq-spinner').style.display = ''
        } else {
            document.getElementById('wordfreq-spinner').style.display = 'none'
            if (this.readyState == 4 && this.status == 200) {
                document.getElementById('plotcontainer').innerHTML = this.response
            }
        }
    };

    form_data = { 'originaltext': originaltext, 'maxterms': max_terms, 'language': language }
    xhttp.open('POST', '/make_wordfreq', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify(form_data));
}
