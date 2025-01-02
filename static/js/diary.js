function createDiary(userId){
    let diaryWindow = window.open(
        `/diary/create/id=${userId}`,
        'Create new diary',
        'width=1000,height=500,left=0,top=0',
    )
    let interval = setInterval(function () {
        if (diaryWindow.closed) {
            clearInterval(interval);
            location.reload();
        }
    }, 1000);
}
function editDiary(diaryId){
    let diaryWindow = window.open(
        `/diary/edit/id=${diaryId}`,
        'edit diary',
        'width=1000,height=500,left=0,top=0',
    )
    let interval = setInterval(function () {
        if (diaryWindow.closed) {
            clearInterval(interval);
            location.reload();
        }
    }, 1000);
}
async function deleteDiary(diaryId){
    const response = await fetch(`/diary/delete/id=${diaryId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    });
    if (response.ok) {
        const termContainer = document.getElementById(`diary${diaryId}`);
        if (termContainer) {
            termContainer.remove();
        }
    }
}