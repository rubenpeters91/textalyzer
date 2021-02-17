function make_wordfreq() {
    let wordfreq_form = document.forms['keywordform']

    let originaltext = wordfreq_form['originaltext'].value;
    let max_terms = wordfreq_form['maxterms'].value
    let wordcloud = wordfreq_form['wordcloud'].value
    let language = wordfreq_form['setlanguage'].value

    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState < 4) {
            document.getElementById('wordfreq-spinner').style.display = ''
        } else {
            document.getElementById('wordfreq-spinner').style.display = 'none'
            if (this.readyState == 4 && this.status == 200) {
                json_response = JSON.parse(this.response)
                embedded_plot = json_response['image']
                img_tag = `<img src="data:image/png;base64,${embedded_plot}" alt="word frequency plot" class="img-fluid"/>`
                document.getElementById('plotcontainer').innerHTML = img_tag
            }
        }
    };

    form_data = { 'originaltext': originaltext, 'maxterms': max_terms, 'wordcloud': wordcloud, 'language': language }
    xhttp.open('POST', '/make_wordfreq', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(JSON.stringify(form_data));
}
