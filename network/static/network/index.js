document.addEventListener('DOMContentLoaded', function() {
    // likes
    const logged_user = document.getElementById('user_name_hidden').value
    //console.log(logged_user)
    document.querySelectorAll('#like_img').forEach(image => {


        image.onclick = function() {        
            console.log(image)
            console.log(image.src);
            var post_id_like = image.parentElement.parentElement.children[1].children[0].value;
            console.log(post_id_like);
            
            const like_counter= image.parentElement.children[2]
            var like_counter_number = Number(like_counter.innerHTML)

            console.log(like_counter)
            

            //if like is ON
            if (image.src == 'http://127.0.0.1:8000/static/network/like_l.png') {
                image.src = "http://127.0.0.1:8000/static/network/like_d.png"
                //console.log("1");
    
                like_counter.innerHTML = like_counter_number - 1;
                
                var myData = {
                    post_id: post_id_like,
                    user_id: logged_user,
                };              

                fetch(`/api_listlikes`)
                .then(response => response.json())
                .then(like => {                                           
                    document.querySelector('#like_ammount').value = `${like[like.length-1]["id"]}`;                                                  
                });
                var like_number = document.querySelector('#like_ammount')

                fetch(`/api_detailed_like/${Number(like_number.value)}/`, {
                    method: "DELETE",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(myData)
                })

            }
            //if like is OFF
            else {
                image.src = 'http://127.0.0.1:8000/static/network/like_l.png';
                //console.log("2");
                like_counter.innerHTML = like_counter_number + 1;

                var myData = {
                    post_id: post_id_like,
                    user_id: logged_user,
                };                
                fetch(`/api_detailed_like/1/`, {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Accept": "application/json",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(myData)
                }).then(function(response) {
                    return response.json();
                }).then(function(data) {
                    console.log("Data is ok", data);
                }).catch(function(ex) {
                    console.log("parsing failed", ex);
                });     
            }   
        }
    })

    // edit   
    document.querySelectorAll('#edit_appear').forEach(post_button => {
        // console.log(i.parentElement)
        post_button.onclick = function() {
        // i.parentElement.style.display = 'none';
        var card = post_button.parentElement.children;            
        //console.log(card)
        var post_text = card[0]
        var div_like = card[1]                     
        var like_image = div_like.children[0]
        //console.log(like_image)
        
        var edit_content = card[4]
        
        var form_for_new_text = edit_content.children[1]
        var form_save_button = edit_content.children[2]
        var post_id = edit_content.children[3].value
        //console.log(post_id)

        //   !! edit box below !!
        open_edit_box(edit_content);
        form_save_button.addEventListener("click", function() {
            new_text = form_for_new_text.value
            post_text.innerHTML = new_text;          
            var myData = {
                post_text: new_text,
                post_author: 1,
            };
            fetch(`/api_detailed_post/${String(post_id)}/`, {
                method: "put",
                credentials: "same-origin",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(myData)
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                console.log("Data is ok", data);
            }).catch(function(ex) {
                console.log("parsing failed", ex);
            });            
            edit_content.style.display = 'none';
        });    
    }   



})

// getting csrf token for - fetch > put method
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    
function open_edit_box(edit_content) {
    
    if (edit_content.style.display == 'none') {
        edit_content.style.display = 'block'
    }
    else {
        edit_content.style.display = 'none';
    }        
}

// function close_edit_box(edit_content) {
//     edit_content.style.display ='none';
//     if (edit_content.style.display = 'block') {
//         edit_content.style.display = 'none'
//     }
//     else {
//         edit_content.style.display = 'none';
//     }        
// }

})

