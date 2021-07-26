function delete_user(user_id) {
    let tr = $(`#tr${user_id}`)
    tr.fadeOut();
   $.ajax(`delete/${user_id}`,{type:'delete'},function (q) {
    console.log(json.dumps('{errors:not}'))
   })
}