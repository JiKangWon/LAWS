$('.CreateChapter').click(function () {
    let sessionClassList = $(this).attr("class").split(' ');
    let session;
    for(let sessionClass of sessionClassList){
        if(sessionClass.includes('Session')){
            session = sessionClass;
            break;
        }
    }
    let subjectId = $(`.${session}.Subject`).val();
    let linkCreateChapter = `/models/chapters/create/id=${subjectId}/`;
    newWindow = window.open(linkCreateChapter, 'Tạo chapter', 'width=400,height=400,left=0,top=0')
});
$(document).ready(function () {
    $('.Subject').on('change', function () {
        const subjectId = $(this).val(); 
        console.log(subjectId);
        const chapterSelect = $(this).closest('div').next().find('.Chapter'); 
        if (subjectId) {
            $.ajax({
                url: "/getChapters/",
                type: "GET",
                data: { subjectId: subjectId },
                success: function (response) {
                    chapterSelect.empty(); 
                    chapterSelect.append('<option value="">--Select chapters in this session--</option>');       
                    response.chapters.forEach(function (chapter) {
                        chapterSelect.append(`<option value="${chapter.id}">${chapter.title}</option>`);
                    });
                },
                error: function () {
                    alert('Failed to fetch chapters. Please try again.');
                }
            });
        } else {
            chapterSelect.empty();
            chapterSelect.append('<option value="">--Select chapters in this session--</option>');
        }
    });
});
    // Hàm xử lý việc thêm chapter trong session
    $(".MoreChapter").click(function () {
        const parentDiv = $(this).parent();
        let session;
        // IF THE INFORMATION ABOUT SESSION
        let sessionClassList = $(this).attr("class").split(" ");
        for (let sessionClass of sessionClassList) {
            if (sessionClass.includes("Session")) {
                session = sessionClass;
                break;
            }
        }
        // GET SUBJECT OF THIS SESSION
        const subjectSelect = document.getElementsByClassName(`Subject ${session}`);
        if (!subjectSelect.length) {
            alert("No Subject element found for this session!");
            return;
        }    
        const subjectId = subjectSelect[0].value;
        if (!subjectId) {
            let res = `
                    <div class="ChapterAndContentContainer">
                        <select name="chapter" class="Chapter">
                            <option value="">--Select chapters in this session--</option>
                        </select>
                        <div class="ClickTag ContentInformation">Content of this chapter</div>
                    </div>
                `;
            parentDiv.append(res);        
            return;    
        }
        // USE AJAX TO GET DATA
        $.ajax({
            url: "/getChapters/",
            type: "GET",
            data: { subjectId: subjectId },
            success: function (response) {
                // CREATE SELECT-OPTION TAG AND GET CHAPTER TO OPTION TAGS
                let res = `
                    <div class="ChapterAndContentContainer">
                        <select name="chapter" class="Chapter">
                            <option value="">--Select chapters in this session--</option>
                `;
                response.chapters.forEach(function (chapter) {
                    res += `<option value="${chapter.id}">${chapter.title}</option>`;
                });
                res += `
                        </select>
                        <div class="ClickTag ContentInformation">Content of this chapter</div>
                    </div>
                `;
                parentDiv.append(res);
            },
            error: function () {
                alert("Failed to fetch chapters. Please try again.");
            }
        });
    });