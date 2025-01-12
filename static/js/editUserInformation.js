function createNewTerm(userId){
    let termCreateWindow = window.open(
        `/create/term/id=${userId}/`,
        'Create new term',
        'width=1000,height=500,left=0,top=0',
    )
    // Kiểm tra trong một khoảng thời gian, ví dụ như mỗi giây
    let interval = setInterval(function () {
        if (termCreateWindow.closed) {
            clearInterval(interval); // Dừng kiểm tra khi cửa sổ bị đóng
            location.reload();
        }
    }, 1000); // Kiểm tra mỗi giây
}
async function delTerm(termId) {
    try {
        // Gửi yêu cầu xóa đến server
        const response = await fetch(`/delTerm/id=${termId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (response.ok) {
            const termContainer = document.getElementById(`term${termId}`);
            if (termContainer) {
                termContainer.remove();
            }
        } else {
            alert(`Lỗi khi xóa Item với id=${termId}:`, response.status);
        }
    } catch (error) {
        alert('Lỗi khi gửi yêu cầu xóa:', error);
    }
}

