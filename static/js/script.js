$(function(){

    //Переключение в менюи подгрузка категорий

    $('.menu  ul li a').live('click', function(){
        var el = $(this);
        var alias = el.attr('rel');

        if (!el.parent().hasClass('current')){
            if (alias){
                $.ajax({
                    type:'get',
                    url:'/get_categories/',
                    data:{
                     'section_alias':alias
                    },
                    success:function(data){
                        $('.menu ul li').removeClass('current');
                        el.parent().addClass('current');
                        $('.submenu').replaceWith(data);
                    },
                    error:function(data){

                    }
                });
                return false;
            }
        }


    });
    //Добавление товара в корзину

    $('.add_product_to_cart').live('click', function(){
        var el = $(this);
        var product_id = el.find('.product_id').val();

        if (product_id){
            $.ajax({
                type:'post',
                url:'/add_product_to_cart/',
                data:{
                 'product_id':product_id
                },
                success:function(data){

                    $('.header_cart').replaceWith(data);

                    setTimeout(function(){
                        $('.header_cart').fadeTo('fast',0.3,function(){
                            $('.header_cart').fadeTo('fast',1,function(){
                                $('.header_cart').fadeTo('fast',0.3,function(){
                                    $('.header_cart').fadeTo('fast',1,function(){

                                    });
                                });
                            });
                        });
                    } ,500);

                },
                error:function(data){

                }



            });
        }

    });

    //Удаление товара из корзины
    $('.delete_product_from_cart').live('click', function(){
        var el = $(this);
        var cart_product_id = el.find('.cart_product_id').val();

        if (cart_product_id){
            $.ajax({
                type:'post',
                url:'/delete_product_from_cart/',
                data:{
                 'cart_product_id':cart_product_id
                },
                success:function(data){
                    data = eval('(' + data + ')');
                    $('.header_cart').replaceWith(data.cart_html);

                    if (data.cart_total == ''){
                        $('.cart_table').replaceWith('<div class="text"><br/><br/><br/><br/><br/><br/></div>');
                        $('.rc_dark').text('Ваша корзина пока пуста');

                    }
                    else{
                        $('.cart_str_total').text(data.cart_total);
                    }



                    el.parent().fadeOut('fast', function(){
                        $(this).remove();
                    });


                },
                error:function(data){
                }

            });
        }

    });

    //Переключение на главной товаров. Распродажа, Хиты, Рекомендации
    $('.catalog_groups ul li a').live('click', function(){
        var el = $(this);
        var type_el = el.attr('rel');
        if (type_el){
            if (!el.parent().hasClass('current')){

                $.ajax({
                    type:'get',
                    url:'/get_products/',
                    data:{
                     'type_el':type_el
                    },
                    success:function(data){
                        $('.items').replaceWith(data);
                        $('.catalog_groups ul li').removeClass('current').removeClass('rc_dark');
                        $('.catalog_groups ul li .rc_dark_arr').remove();
                        el.parent().addClass('current').addClass('rc_dark').append('<div class="rc_dark_arr"></div>');

                        $('.discounts').hide();
                        switch (type_el){
                            case 'sale':
                                $('.sale_products_index').show();
                                break;
                            case 'top':
                                $('.top_products_index').show();
                                break;
                            case 'recomended':
                                $('.recomended_products_index').show();
                                break;

                        }
                    },
                    error:function(data){

                    }
                });
            }
        }
        return false;
    });


    $('a.show_top_products').live('click', function(){
        $('.sale .sale_items').hide();
        $('.sale .top_products').show();

        var h2_text = $('.sale h2').text();
        var this_text = $(this).text();

        var h2_class = $('.sale h2').attr('class');
        var this_class = $(this).attr('class');

        $('.sale h2').text(this_text);
        $(this).text(h2_text);

        $('.sale h2').attr('class',this_class);
        $(this).attr('class',h2_class);

        $('.sale .sale_all').hide();
        $('.sale .top_products_all').show();


        return false;
    });
    $('a.show_recomended_products').live('click', function(){
        $('.sale .sale_items').hide();
        $('.sale .recomended_products').show();


        var h2_text = $('.sale h2').text();
        var this_text = $(this).text();

        var h2_class = $('.sale h2').attr('class');
        var this_class = $(this).attr('class');

        $('.sale h2').text(this_text);
        $(this).text(h2_text);

        $('.sale h2').attr('class',this_class);
        $(this).attr('class',h2_class);

        $('.sale .sale_all').hide();
        $('.sale .recomended_products_all').show();

        return false;
    });
    $('a.show_sale_products').live('click', function(){
        $('.sale .sale_items').hide();
        $('.sale .sale_products').show();

        var h2_text = $('.sale h2').text();
        var this_text = $(this).text();

        var h2_class = $('.sale h2').attr('class');
        var this_class = $(this).attr('class');

        $('.sale h2').text(this_text);
        $(this).text(h2_text);

        $('.sale h2').attr('class',this_class);
        $(this).attr('class',h2_class);

        $('.sale .sale_all').hide();
        $('.sale .sale_products_all').show();

        return false;
    });



});


