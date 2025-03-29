$(document).on("click", "[data-delete]", function (e) {
    e.preventDefault();

    let deleteUrl = $(this).data("url");
    let csrfToken = $(this).data("csrftoken");
    let itemType = $(this).data("item-type");
    let itemUpdateId = $(this).data("item-id");

    Swal.fire({
        title: "Emin misin?",
        text: itemType === "grade" ? "Bu eğitim düzeyi silinecek!" : "Bu konu silinecek!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Evet, sil!",
        cancelButtonText: "İptal"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: deleteUrl,
                type: "POST",
                headers: { "X-CSRFToken": csrfToken },
                data: JSON.stringify({ item_update_id: itemUpdateId }),
                contentType: "application/json",
                success: function (response) {
                    Swal.fire("Silindi!", response.message, "success").then(() => {
                        location.reload();
                    });
                },
                error: function (xhr) {
                    let errorMsg = xhr.responseJSON?.message || "Bir hata oluştu.";
                    Swal.fire("Hata!", errorMsg, "error");
                }
            });
        }
    });
});
