var loadQuestion = function (num) {
    var data = {
        'num': num,
        'get_question': 1
    };
    $.get(url, data, function (r) {
        $('.question-wrapper').html(r);
    });
};

var activate_next_btn = function () {
    var answered = $('input[name=answer]:checked');
    var btn = $('button.next-skip');
    if (answered.length) {
        btn.text('Next');
        btn.removeClass('skip');
    } else {
        btn.text('Skip');
        btn.addClass('skip');
    }
}

$(document).ready(function () {
    loadQuestion(1);
});

$(document).on('change', 'input[name=answer][type=radio]', function (e) {
    var t = $(this);
    var question_id = t.parents('.jawab').attr('question-id');
    var data = {
        'question_answer': t.attr('answer-id'),
        'question': question_id,
        'answer': 1,
        'csrfmiddlewaretoken': csrf
    };

    $.post(url, data, function (r) {
        if (r == 'success') {
            activate_next_btn();
        }
    });
});
$(document).on('change', 'input[name=answer][type=checkbox]', function (e) {
    var t = $(this);
    var answer = t.val();

    if (t.prop('checked')) {
        selected_answer.push(t.val());
    } else {
        selected_answer.splice(selected_answer.indexOf(t.val()), 1);
    }
});

$(document).on('click', 'a.next-question', function () {
    var question_number = $('.question-number').text();
    loadQuestion(parseInt(question_number)+1);
});

$(document).on('click', '.select-ans', function(e){
    $(this).parent().find('input').click();
});
