function applyRadio(){
    $(".rad").unbind('mousedown');
    $(".rad").mousedown(
    /* при клике на чекбоксе меняем его вид и значение */
    function() {
        changeRad($(this));
    });

    $(".radLabel").unbind('mousedown');
    $(".radLabel").mousedown(
    /* при клике на чекбоксе меняем его вид и значение */
    function() {
        changeRad($(this).parent().find("span"));
    });

    $(".rad").each(
        /* при загрузке страницы нужно проверить какое значение имеет чекбокс и в соответствии с ним выставить вид */
        function(){
            changeRadStart($(this));
    });
}
function changeRad(el)
	/*
    функция смены вида и значения чекбокса
    el - span контейнер дял обычного чекбокса
    input - чекбокс
    */
	{
     var el = el,
     input = el.find("input").eq(0),
     div = el.parents('.radio');

     if(!input.attr("disabled")){
           if(!div.hasClass('activeRadio')) {
              div.parent().find(".rad").css("background-position","0 0");
              div.parent().find('.radio').removeClass("activeRadio");
              div.parent().find("input").attr("checked", false);
              el.css("background-position","0 -15px");
              input.attr("checked", true);
              el.parent().toggleClass("activeRadio");
          } else {
              return false;
          }
    }
     return true;
}

function changeRadStart(el)
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
            el.css("background-position","0 -15px");
            el.parents(".radio").addClass('activeRadio');
            }
      }
 return true;
}
$(document).ready(function(){
    applyRadio();
});