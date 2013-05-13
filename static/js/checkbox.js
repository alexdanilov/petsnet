function applyCheckbox(){
    $(".checkbox").unbind('mousedown');
    $(".checkbox").mousedown(
    /* ��� ����� �� �������� ������ ��� ��� � �������� */
    function() {
        changeCheck($(this));
    });

    $(".checkLabel").unbind('mousedown');
    $(".checkLabel").mousedown(
    /* ��� ����� �� �������� ������ ��� ��� � �������� */
    function() {
        changeCheck($(this).parent().find("span"));
    });

    $(".checkbox").each(
        /* ��� �������� �������� ����� ��������� ����� �������� ����� ������� � � ������������ � ��� ��������� ��� */
        function(){
            changeCheckStart($(this));
    });
}
function changeCheck(el)
	/*
    ������� ����� ���� � �������� ��������
    el - span ��������� ��� �������� ��������
    input - �������
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
	    ���� ���������� ������� checked, ������ ��� ��������
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