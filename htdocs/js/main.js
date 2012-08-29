$(document).ready(function(){
	$('#header .searchForm input').focus(function(){
		if($(this).val() == 'Поиск'){
			$(this).val('');
			$(this).css({
				color: '#737373'
			});
		}
	});

	$('#header .searchForm input').blur(function(){
		if($(this).val() == ''){
			$(this).val('Поиск');
			$(this).css({
				color: ''
			});
		}
	});

	var params = {
		changedEl: "#regionsState, #regionsCity, #searchSelect, #searchState, #searchCity",
		scrollArrows: false
	}
	cuSel(params);

	$('#header .menu a').click(function(){
		var rel = $(this).attr('rel'),
		oldRel,
		link = $(this);

		if(!link.hasClass('active')){
			oldRel = link.parents('.menu').find('.active').attr('rel');
			link.parents('.menu').find('.active').removeClass('active');

			if(link.parents('#headerInner').find('.subMenu').hasClass('show')){
				$(oldRel).stop().animate({bottom: '48px'}, 300, function(){
					$(oldRel).removeClass('show');
					$(rel).stop().animate({bottom: 32-$(rel).height()+'px'}, 300, function(){
						$(rel).addClass('show');
					});
					link.addClass('active');
				});
			}
			else{
				$(rel).stop().animate({bottom: 32-$(rel).height()+'px'}, 300, function(){
					$(rel).addClass('show');
				});
				link.addClass('active');
			}
		}
		else{
			$(rel).stop().animate({bottom: '48px'}, 300);
			$(rel).removeClass('show');
			link.removeClass('active');
		}

		return false;
	});

	$('.dayPhoto .image').fancybox({
		transitionIn:'elastic',
		transitionOut:'elastic',
		speedIn: 600,
		speedOut: 200,
		overlayColor:'#fff',
		overlayOpacity:  0.9
	});

    /*
	$('.contentBlock .cats a').click(function(){
		if(!$(this).hasClass('active')){
			$(this).parent().find('.active').removeClass('active');
			$(this).addClass('active');
		}
		return false;
	});
    */
	$('.carousel li:first img').addClass('active');

	$(".carousel a").click(function() {
		if(!$(this).find('img').hasClass('active')){
			$(this).parents('.carousel').find('.active').removeClass('active');
			$(this).find('img').addClass('active');
			$(".clinicInfo .imagesBlock .image img").attr("src", $(this).attr("href"));
		}
		return false;
	})

	$('.clinicInfo .tabs a').click(function(){
		if(!$(this).hasClass('active')){
			$(this).parent().find('.active').removeClass('active');
			$('.clinicInfo .tabsContent').removeClass('show');
			$(this).addClass('active');
			$($(this).attr('rel')).addClass('show');
		}
		return false;
	});

	$(".formWrapper .rating").hover(function(){
         $(this).mousemove(function(event){
             var changedWidth=-1*($(this).offset().left-event.clientX),
                 width=changedWidth*100/parseInt($(this).css('width')),
                 newWidth;

             if(width<=20) newWidth="20%";
             if(width>20 && width<=40) newWidth="40%";
             if(width>40 && width<=60) newWidth="60%";
             if(width>60 && width<=80) newWidth="80%";
             if(width>80 && width<=100) newWidth="100%";
             $(this).find(".fill").css('width',newWidth);
         });
     }, function(){
             $(this).find(".fill").css('width','0%');
     });

     $(".formWrapper .rating").click(function(){
         $(this).unbind('hover');
         $(this).unbind('mousemove');
         var value=parseInt($(this).find('.fill').css('width'))/25;
         $(this).find('input').attr('value', value);
         $(this).parents('.formWrapper').find('.grade').text(value+'/5');
     });

	 $('#comments .bottomButton').click(function(){
	 	$('.formWrapper').stop().animate({height: $('.formWrapper form').height()+30}, 300);
		if(($.browser.safari) || ($.browser.webkit)) $('body').stop().animate({scrollTop: ($('.formWrapper').offset().top)}, 1000);
        else $('html').stop().animate({scrollTop: ($('.formWrapper').offset().top)}, 1000);
		return false;
	 });

	var searchHeight = $('.search').height();
	 $('.search .showHide').click(function(){
	 	if(!$(this).hasClass('active')){
			$(this).parents('.search').stop().animate({height: 0}, 300, function(){
				$('.search').css({
					overflow: 'hidden',
					backgroundImage: 'none'
				});
				$('.search .showHide').text('Показать блок поиска');
				$('.search .showHide').addClass('active');
			});
	 	}
		else{
			$(this).parents('.search').stop().animate({height: searchHeight}, 300, function(){
				$('.search').css({
					overflow: 'hidden',
					backgroundImage: ''
				});
				$('.search .showHide').text('Свернуть блок поиска');
				$('.search .showHide').removeClass('active');
			});
		}
		return false;
	 });

	 $('.showPopup').click(function(){
          var rel=$(this).attr('rel');
		  var winH = $(window).height();
          var winW = $(window).width();

          $('#'+rel).css('display', 'block');

		  $('#mask').css({
		  	height: $(document).height(),
		  	width: $(document).width()
		  });

          $('#popup').css({
          	top: winH/2 - ($('#popupInner').height()/2 + 10) + $(window).scrollTop(),
			marginLeft: -($('#popupInner').width()/2 + 18)
          });

		  $('#popup').css({
		  	display: 'none',
			height: 'auto',
			overflow: 'visible'
		  });
		  $('#mask, #popup').stop().fadeIn(300);

		  return false;
	 });

	 $('#popup div.close, #mask, #choiceServices a').click(function(){

	 	var inputs='', list='';
	 	$('#choiceServices input[checked]').each(function(){
	 		inputs+= $(this).parent().html();
			list+= '<li>'+$(this).parents('.check').find('.checkLabel').text()+'</li>';
	 	});

		$('.selectedServices .list').html(list);
		$('.selectedServices .hiddenCheck').html(inputs);
		if(list != '' && inputs != '') $('.selectedServices').fadeIn(300);
		else $('.selectedServices').fadeOut(300);

		$('#mask, #popup').fadeOut(300, function(){
	 		$('#popup').css({
		  	display: '',
			height: '',
			overflow: ''
		  });
	 		$('#popupInner div[id]').css('display', 'none');
	 	});

	 	return false;
	 });

});

$(window).load(function(){
	 $(".carousel").jCarouselLite({
        btnNext: ".carouseleNext",
        btnPrev: ".carouseleBack",
        circular: false,
        afterEnd: function(){
            caruselCheckShowArrows();
        }
	});
});

	function caruselCheckShowArrows(){
        if($(".carousel li:first").offset().left >= $(".carousel").offset().left){
            $('.carouseleBack').css('display', 'none');
        }else{
            $('.carouseleBack').css('display', 'block');
        }
        if($(".carousel li:last").offset().left+$(".carousel li:last").width() <= $(".carousel").offset().left+$(".carousel").width()){
            $('.carouseleNext').css('display', 'none');
        }else{
            $('.carouseleNext').css('display', 'block');
        }
    };