function createNewSession(dayId){
    let createSessionWindow = window.open(
        `/create/session/id=${dayId}/`,
        'Create new session',
        'width=1000,height=500,left=0,top=0',
    )
    let interval = setInterval(function () {
        if (createSessionWindow.closed) {
            clearInterval(interval);
            location.reload();
        }
    }, 1000); 

}

async function delSessions(sessionId) {
    try {
        // Gửi yêu cầu xóa đến server
        const response = await fetch(`/delSessions/id=${sessionId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        alert('Lỗi khi gửi yêu cầu xóa:', error);
    }
}

async function changeStatus(sessionId, element) {
    try {
        // Gửi yêu cầu xóa đến server
        const response = await fetch(`/put/session/status/id=${sessionId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (!response.ok) {
            alert("Lỗi rùi bé ơi");
            return;
        } 
        if (element.checked){
        }
        else {
        }
    } catch (error) {
        alert('Lỗi khi gửi yêu cầu xóa:', error);
    }
}