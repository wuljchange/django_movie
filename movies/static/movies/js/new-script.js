    function vote(obj) {
        if ('{{ user.is_authenticated }}' == 'True'){
            var ids = new Array();
            ids = obj.id.split('-');
            var comment_id = ids[2];
            var choice = ids[1];
            var id = ids[0]+"-"+choice+"s"+comment_id
            var sp = document.getElementById(id)
            var ul = "/comment/"+comment_id+"/"+choice;
            $.ajax({
                url: ul,
                type: "get",
                dataType: "json",
                success: function(data){
                    if (data.res == "done"){
                        alert("你已经对该评论投过票了!");
                    }else{
                        var vote = Number(sp.innerText);
                        sp.innerText = String(vote+1);
                    }
                },
                error: function(data){
                    alert("error");
                },
            });
        }else{
            alert('please login first!');
        }
    }

    function show(txt) {
        if (txt == 'hot'){
            document.getElementById('comment-body-hot').style.display="block";
            document.getElementById('comment-body-new').style.display="none";
        }else{
            document.getElementById('comment-body-hot').style.display="none";
            document.getElementById('comment-body-new').style.display="block";
        }
    }