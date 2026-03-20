// === Google Apps Script ===
// Hướng dẫn cài đặt:
// 1. Mở Google Sheets mới: https://sheets.new
// 2. Đặt tên sheet (ví dụ: "Signature Data")
// 3. Vào Extensions > Apps Script
// 4. Xóa code mặc định, dán toàn bộ code này vào
// 5. Nhấn Deploy > New deployment
//    - Type: Web app
//    - Execute as: Me
//    - Who has access: Anyone
// 6. Copy URL deployment (dạng https://script.google.com/macros/s/.../exec)
// 7. Dùng URL đó khi chạy build.py

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

    // Tạo header nếu sheet trống
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(['Thời gian', 'Trang', 'Họ tên', 'Email', 'Số điện thoại', 'Link chữ ký']);
      sheet.getRange(1, 1, 1, 6).setFontWeight('bold');
    }

    // Lưu ảnh chữ ký lên Google Drive
    var sigBase64 = data.signature.replace(/^data:image\/png;base64,/, '');
    var blob = Utilities.newBlob(
      Utilities.base64Decode(sigBase64),
      'image/png',
      (data.page || 'unknown') + '_' + (data.name || 'anonymous').replace(/[^a-zA-Z0-9]/g, '_') + '_signature.png'
    );
    var file = DriveApp.createFile(blob);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    var sigUrl = 'https://drive.google.com/uc?id=' + file.getId();

    // Ghi dữ liệu vào sheet
    sheet.appendRow([
      new Date().toLocaleString('vi-VN'),
      data.page || '',
      data.name || '',
      data.email || '',
      data.phone || '',
      sigUrl
    ]);

    return ContentService.createTextOutput(JSON.stringify({status: 'success', signatureUrl: sigUrl}))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({status: 'error', message: err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput('Service is running');
}
