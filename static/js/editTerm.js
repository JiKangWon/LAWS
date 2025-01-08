function createNewClass(termId){
    const createClassWindow = window.open(
        `/create/class/id=${termId}`,
        `Create new class`,
        `width=1000,height=500,left=0,top=0`
    )
    let interval = setInterval(function () {
        if (createClassWindow.closed) {
            clearInterval(interval); // Dừng kiểm tra khi cửa sổ bị đóng
            location.reload();
        }
    }, 1000); // Kiểm tra mỗi giây
}
async function delClass(classId) {
    // Xác nhận yêu cầu xóa
    const confirmDelete = confirm(`Do you want to delete this class?`);
    if (!confirmDelete) {
        return;
    }
    try {
        // Gửi yêu cầu xóa đến server
        const response = await fetch(`/delClass/id=${classId}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
        });
        if (response.ok) {
            const termContainer = document.getElementById(`class${classId}`);
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
