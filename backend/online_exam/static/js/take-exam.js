var loadQuestion = function (num) {
    var data = {
        'num': num,
        'get_question': 1
    };
    $.get(url, data, function (r) {
        $('.question-wrapper').html(r);
        $('.current-question-num').val(num);
    });
};

var activate_next_btn = function () {
    var answered = $('input[name=answer]:checked');
    var btn = $('button.next-question');
    if (answered.length) {
        btn.text('Next');
        btn.removeClass('skip');
    } else {
        btn.text('Skip');
        btn.addClass('skip');
    }
}

$(document).ready(function () {
    // load last left question
    // get last question number from the session
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

    // need to check if current answered number in skipped_number
    // if so, delete current number from skipped_number
});

$(document).on('change', 'input[name=answer][type=checkbox]', function (e) {
    // answer process with multiple answer
});

$(document).on('click', '.select-ans', function(e){
    $(this).parent().find('input').click();
});

$(document).on('click', '.next-question', function (e) {
    var t = $(this);
    var current_number = $('.current-question-num').val();
    var next_num = parseInt(current_number)+1;
    if (t.hasClass('skip')) {
        skipped_number.push(current_number);
    } else {
        loadQuestion(next_num);
    }
});

$(document).on('click', '.previous-question', function (e) {
    var t = $(this);
    var current_number = $('.current-question-num').val();
    if (current_number != 1) {
        var next_num = parseInt(current_number)-1;
        loadQuestion(next_num);
    }
});

$(document).on('keypress', '.current-question-num', function (e) {
    if (e.which == 13) {
        var num = $(this).val();
        loadQuestion(num);
    }
})
