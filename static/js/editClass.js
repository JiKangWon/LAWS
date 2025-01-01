function createNewSubject(classId){
    let createSubjectWindow = window.open(
        `/create/subject/id=${classId}`,
        `Create new subject`,
        `width=600,height=400,left=0,top=0`
    );
    let interval = setInterval(function () {
        if (createSubjectWindow.closed) {
            clearInterval(interval); 
            location.reload();
        }
    }, 1000);
}
async function delSubject(subjectId) {
    try {
        // Gửi yêu cầu xóa đến server
        const response = await fetch(`/delSubject/id=${subjectId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (response.ok) {
            const termContainer = document.getElementById(`subject${subjectId}`);
            if (termContainer) {
                termContainer.remove();
            }
        } else {
            alert(`Lỗi khi xóa Item với id=${subjectId}:`, response.status);
        }
    } catch (error) {
        alert('Lỗi khi gửi yêu cầu xóa:', error);
    }
}