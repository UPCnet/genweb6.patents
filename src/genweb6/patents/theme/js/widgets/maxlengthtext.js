
$(document).ready(function() {
    console.log("max length text widget loaded");
    $(".maxlengthtext-widget").each(function() {
        const max_length = $(this).attr("maxlength");

        function updateFeedback(input) {
            if (input.value.length >= max_length) {
                /* Add an error message sibling if does not exist */
                const err_text = input.getAttribute("data-maxlength-exceeded-text") || "The maximum length has been exceeded.";
                if(!$(`em[data-for=${input.id}]`).length > 0){
                    $(`<em class="info-feedback" data-for=${input.id}>${err_text}</em>`)
                        .insertAfter(input);
                }
            }
            else {
                /* Remove the error message sibling */
                $(`em[data-for=${input.id}]`).remove();
            }
        }

        // Initial check in case the input is already filled
        updateFeedback(this);

        $(this).on("input", () => { updateFeedback(this); });
    });
});    
