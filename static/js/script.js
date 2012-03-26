$(function(){

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

                    $('.header_cart').replaceWith(data);

                    el.parent().fadeOut('fast', function(){
                        $(this).remove();
                    });
                    /*
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
                    */

                },
                error:function(data){

                }



            });
        }

    });



});


