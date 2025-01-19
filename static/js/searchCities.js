$(document).ready(function () {
    $('#ville_input').on('input', function () {
        const query = $(this).val();
        if (query.length > 0) {
            $.getJSON('/autocomplete', { q: query }, function (data) {
                const resultsDiv = $('#autocomplete-results');
                resultsDiv.empty();
                data.forEach(item => {
                    resultsDiv.append(`<div class="autocomplete-item" data-id="${item.id}">${item.nom_commune} (${item.code_postal})</div>`);
                });
            });
        } else {
            $('#autocomplete-results').empty();
        }
    });

    $('#autocomplete-results').on('click', '.autocomplete-item', function () {
        const selectedId = $(this).data('id');
        const selectedText = $(this).text();
        $('#ville_id').val(selectedId);
        $('#ville_input').val(selectedText);
        $('#autocomplete-results').empty();
    });

    $(document).click(function (e) {
        if (!$(e.target).closest('#ville_input, #autocomplete-results').length) {
            $('#autocomplete-results').empty();
        }
    });
});