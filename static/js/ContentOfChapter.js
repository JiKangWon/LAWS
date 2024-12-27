$('.ContentInformation').click(function() {
    const chapterId = $(this).prev('.Chapter').val();
    const getContentOfChapterUrl = `/getContentOfChapters/id=${chapterId}/`;
    newWindow = window.open(
        getContentOfChapterUrl, 
        'Content of chapter', 
        'width=1000,height=500,left=0,top=0'
    );
});