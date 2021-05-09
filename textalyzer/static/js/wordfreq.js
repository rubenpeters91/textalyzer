"use strict";

async function make_wordfreq() {
    document.getElementById('wordfreq-spinner').style.display = '';
    let wordfreq_form = document.forms['keywordform'];
    let originaltext = wordfreq_form['originaltext'].value;
    let max_terms = wordfreq_form['maxterms'].value;
    let wordcloud = wordfreq_form['wordcloud'].value;
    let language = wordfreq_form['setlanguage'].value;

    const form_data = {
        'originaltext': originaltext, 'maxterms': max_terms,
        'wordcloud': wordcloud, 'language': language
    };
    let response = await fetch('/make_wordfreq', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(form_data)
    });

    document.getElementById('wordfreq-spinner').style.display = 'none';
    if (response.ok) {
        let json_response = await response.json();
        if ('image' in json_response) {
            let img_tag = `<img src="data:image/png;base64,${json_response['image']}"` +
                ' alt="word frequency plot" class="img-fluid"/>';
            document.getElementById('plotcontainer').innerHTML = img_tag;
        } else {
            // First remove all contents, else it will draw the plot multiple times
            document.getElementById('plotcontainer').innerHTML = "";
            d3_bar(json_response['words'])
        }
    } else {
        document.getElementById('plotcontainer').innerHTML = '<p>Something went wrong...</p>'
    }
}
