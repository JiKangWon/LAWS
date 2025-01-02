function openShift(userId){
    const number = prompt('Nhập số phiên làm việc trong ca:');
    window.location.href = `/todo/open/id=${userId}/number=${number}`;
}