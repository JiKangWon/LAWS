function createDeadline(userId){
    let deadlineCreateWindow = window.open(
        `/deadline/create/id=${userId}/`,
        'Create new deadline',
        'width=1000,height=500,left=0,top=0',
    )
    let interval = setInterval(function () {
        if (deadlineCreateWindow.closed) {
            clearInterval(interval);
            location.reload();
        }
    }, 1000); // Kiểm tra mỗi giây
}
async function delDeadline(deadlineId){
    const response = await fetch(`/deadline/delete/id=${deadlineId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    });
    if (response.ok) {
        const termContainer = document.getElementById(`deadline${deadlineId}`);
        if (termContainer) {
            termContainer.remove();
        }
    }
}