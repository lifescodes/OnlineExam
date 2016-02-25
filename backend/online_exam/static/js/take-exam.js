var loadSkippedNumber = function() {
    for (var i = 0; i < skipped_number.length; i++) {
        var e = '<div class="skipped-number">'+skipped_number[i]+'</div>';
        $('.skipped').append(e);
    }
};

var addSkippedNumber = function(num) {
    if (skipped_number.indexOf(num) == -1) {
        skipped_number.push(num);
        var e = '<div class="skipped-number" id="'+num+'">'+num+'</div>';
        $('.skipped').append(e);
    }
}

var removeSkippedNumber = function(num) {
    if (skipped_number.indexOf(num) != -1) {
        skipped_number.splice(skipped_number.indexOf(num), 1);
        $('.skipped').find('#'+num).fadeOut(function(){ $(this).remove() });
    }
}

var loadQuestion = function (num, kwargs) {
    var data = {
        'num': num,
        'get_question': 1
    };
    if (typeof kwargs !== 'undefined') {
        data = jQuery.extend(data, kwargs);
    }
    $.get(url, data, function (r) {
        $('.question-wrapper').html(r);
        $('.current-question-num').val(num);
        
        var is_answered = $(r).find('input[type=radio][checked]');
        var btn = $('button.next-question');
        if (is_answered.length) {
            btn.text('Next');
            btn.removeClass('skip');
        } else {
            btn.text('Skip');
            btn.addClass('skip');
        }
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
    // TODO:load last left question
    loadQuestion(1);
    loadSkippedNumber();
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
            var current_number = $('.question-wrapper').find('.question-num').text();
            console.log(current_number);
            removeSkippedNumber(parseInt(current_number));
        }
    });

    // TODO: need to check if current answered number in skipped_number
    // if so, delete current number from skipped_number
});

$(document).on('change', 'input[name=answer][type=checkbox]', function (e) {
    // TODO: answer process with multiple answer
});

$(document).on('click', '.select-ans', function(e){
    $(this).parent().find('input').click();
});

$(document).on('click', '.next-question', function (e) {
    var t = $(this);
    var current_number = $('.current-question-num').val();
    current_number = parseInt(current_number);
    var next_num = parseInt(current_number)+1;
    if (t.hasClass('skip')) {
        loadQuestion(next_num, {'skip': current_number});
        addSkippedNumber(current_number);
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

$(document).on('click', '.skipped-number', function(e){
    var num = $(this).text();
    loadQuestion(num);
});
