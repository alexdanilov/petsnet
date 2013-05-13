function applyCheckbox(){
    $(".checkbox").unbind('mousedown');
    $(".checkbox").mousedown(
    /* при клике на чекбоксе меняем его вид и значение */
    function() {
        changeCheck($(this));
    });

    $(".checkLabel").unbind('mousedown');
    $(".checkLabel").mousedown(
    /* при клике на чекбоксе меняем его вид и значение */
    function() {
        changeCheck($(this).parent().find("span"));
    });

    $(".checkbox").each(
        /* при загрузке страницы нужно проверить какое значение имеет чекбокс и в соответствии с ним выставить вид */
        function(){
            changeCheckStart($(this));
    });
}
function changeCheck(el)
	/*
    функция смены вида и значения чекбокса
    el - span контейнер дял обычного чекбокса
    input - чекбокс
    */
	{
     var el = el,
     input = el.find("input").eq(0);
     if(!input.attr("disabled")){
           if(!input.attr("checked")) {
              el.css("background-position","0 -12px");
              input.attr("checked", true);
              el.parent().find("b").css("display", "inline-block");
          } else {
              el.css("background-position","0 0");
              input.attr("checked", false);
              el.parent().find("b").css("display", "none");
          }
    }
     return true;
}

function changeCheckStart(el)
/*
	    если установлен атрибут checked, меняем вид чекбокса
*/
{
var el = el,
        input = el.find("input").eq(0);
      if(input.attr("disabled")){
       el.removeClass("checkbox");
       el.toggleClass("disable");
       el.parent().find("i").removeClass("checkLabel");
       el.parent().find("i").toggleClass("disable");
      }
      else{
          if(input.attr("checked")) {
            el.css("background-position","0 -12px");
            el.parent().find("b").css("display", "inline-block");
			input.attr("checked", "checked");
            }
      }
 return true;
}
$(document).ready(function(){
    applyCheckbox();
});