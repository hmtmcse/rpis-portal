PWeb.Account = (function () {

    let originalCover, imageUploader, tempCover, uploadCoverPageForm, tempCoverIdJs, coverCropperLib, coverImageRepositionText
    let avatarImageUploadInput, avatarCropModal, avatarImageUploadForm, modalAvatarImageView, cropperLib,
        modalAvatarImageViewJSid

    function coverImageUploadChange() {
        imageUploader.on("change", function (event) {
                let target = event.target
                if (target !== undefined && target.files.length > 0) {
                    const [file] = target.files
                    tempCover.attr("src", URL.createObjectURL(file))
                    showHideOriginalTempCover(false)
                    showHideCoverActions(false)
                    initCoverPageCropper()
                }
            }
        )
    }

    function showHideCoverActions(isShowDefault = true) {
        let defaultCoverAction = jQuery(".default-cover-action")
        let modifyCoverAction = jQuery(".modify-cover-action")
        if (isShowDefault) {
            coverCropperLib.destroy()
            defaultCoverAction.show()
            modifyCoverAction.hide()
            coverImageRepositionText.hide()
            uploadCoverPageForm.trigger("reset")
        } else {
            defaultCoverAction.hide()
            modifyCoverAction.show()
            coverImageRepositionText.show()
        }
    }

    function showHideOriginalTempCover(isShowOriginal = true) {
        if (isShowOriginal) {
            originalCover.show()
            tempCover.hide()
        } else {
            originalCover.hide()
            tempCover.show()
        }
    }

    function handleCancelModification() {
        let cancelCoverModify = jQuery("#cancel-cover-modify")
        cancelCoverModify.on("click", function () {
            showHideCoverActions(true)
            showHideOriginalTempCover(true)
        })
    }

    function handleAvatarImageUpload() {
        avatarImageUploadInput.on("change", function (event) {
            let files = event.target.files;
            if (files && files.length > 0) {
                const [file] = files
                showHideAvatarModal(true)
                modalAvatarImageView.attr("src", URL.createObjectURL(file))
                avatarImageUploadInput.val(null)
            }
        })
    }

    function showHideAvatarModal(isShow = true) {
        if (isShow) {
            avatarCropModal.modal('show')
        } else {
            avatarCropModal.modal('hide')
        }
    }

    function handleAvatarModalEvents() {
        avatarCropModal.on('hidden.bs.modal', function () {
            avatarImageUploadForm.trigger("reset")
            if (cropperLib) {
                cropperLib.destroy();
                cropperLib = null;
            }
        });

        avatarCropModal.on('shown.bs.modal', function () {
            cropperLib = new Cropper(modalAvatarImageViewJSid, {
                aspectRatio: 1,
                viewMode: 3,
            });
        })
    }

    function handleCropFunctionAndUploadImage() {
        let cropAction = jQuery(".js-modal-crop-image")
        let profileAvatarImage = jQuery("#profile-avatar-image")
        cropAction.on("click", function () {
            if (cropperLib) {
                let canvas = cropperLib.getCroppedCanvas({
                    width: 180,
                    height: 180,
                });
                canvas.toBlob(function (blob) {
                    let formData = new FormData();
                    formData.append('profilePhoto', blob, 'avatar.jpg');
                    PWeb.ajax.call({
                        data: formData,
                        url: PWeb.baseURL + "/member/upload-profile-photo",
                        processData: false,
                        contentType: false,
                        success: function (content) {
                            PWeb.messageBox.showMessage(content.success, content.message)
                            avatarCropModal.modal('hide')
                            if (content.success) {
                                profileAvatarImage.attr("src", canvas.toDataURL())
                            }
                        }
                    })
                })
            }
        })
    }


    function initCoverPageCropper() {
        coverCropperLib = new Cropper(tempCoverIdJs, {
            viewMode: 3,
            dragMode: 'move',
            autoCropArea: 1,
            restore: false,
            guides: false,
            highlight: false,
            cropBoxMovable: false,
            cropBoxResizable: false
        })
    }

    function handleCoverPageModifyConfirm() {
        let confirmCoverModify = jQuery("#confirm-cover-modify")
        confirmCoverModify.on("click", function () {
            if (coverCropperLib) {
                let canvas = coverCropperLib.getCroppedCanvas();
                canvas.toBlob(function (blob) {
                    let formData = new FormData();
                    formData.append('cover', blob, 'cover.jpg');
                    PWeb.ajax.call({
                        data: formData,
                        url: PWeb.baseURL + "account/update-resource/",
                        processData: false,
                        contentType: false,
                        success: function (content) {
                            PWeb.messageBox.showMessage(content.success, content.message)
                            if (content.success && content.cover) {
                                originalCover.attr("src", PWeb.assetsURL + content.cover)
                                tempCover.attr("src", PWeb.assetsURL + content.cover)
                                showHideCoverActions(true)
                                showHideOriginalTempCover(true)
                            }
                        }
                    })
                })
            }
        })
    }

    return {

        uploadAvatar: function () {
            avatarImageUploadInput = jQuery("#avatar-image-upload")
            avatarImageUploadForm = jQuery("#avatar-image-upload-form")
            avatarCropModal = jQuery("#avatar-upload-modal")
            modalAvatarImageView = jQuery("#modal-avatar-image-view")
            modalAvatarImageViewJSid = document.getElementById("modal-avatar-image-view");
            handleAvatarImageUpload()
            handleAvatarModalEvents()
            handleCropFunctionAndUploadImage()
        },

        uploadCoverImage: function () {
            originalCover = jQuery("#original-cover-image")
            tempCover = jQuery("#temp-cover-image")
            tempCoverIdJs = document.getElementById("temp-cover-image");
            imageUploader = jQuery("#cover-image-upload")
            uploadCoverPageForm = jQuery("#upload-cover-page-form")
            coverImageRepositionText = jQuery("#cover-image-reposition-text")


            handleCoverPageModifyConfirm()
            handleCancelModification()
            coverImageUploadChange()

        }
    }
}());

jQuery(document).ready(function () {
    PWeb.Account.uploadCoverImage();
    PWeb.Account.uploadAvatar();
});
