# Nhập các thông tin cần thiết từ người dùng
scada_id = input("Nhập SCADA ID (ví dụ: RECC0003): ")
new_substation_name = input("Nhập tên trạm điện mới (ví dụ: HVUONG): ")

# Đường dẫn file đầu vào và đầu ra trong thư mục hiện tại
input_file = 'input.ddl'
output_file = 'output.ddl'

try:
    # Đọc nội dung file .ddl
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Biến cờ hiệu để xác định khi nào cần thay thế tên trạm điện
    replace_next = False

    # Duyệt qua các dòng trong file
    for i, line in enumerate(lines):
        # Kiểm tra dòng chứa SCADA ID
        if f'record_key("{scada_id}")' in line:
            replace_next = True
        # Nếu dòng trước có chứa SCADA ID, tìm dòng tên trạm và thay thế
        elif replace_next and 'record("SUBSTN")' in line:
            # Giữ nguyên khoảng cách đầu dòng và thay thế tên trạm điện
            indent = line[:line.find('record("SUBSTN")')]
            lines[i] = f'{indent}record("SUBSTN") record_key("{new_substation_name}")\n'
            replace_next = False

    # Ghi nội dung đã chỉnh sửa vào file .ddl mới
    with open(output_file, 'w') as file:
        file.writelines(lines)

    print(f"Đã thay thế tên trạm điện thành công và xuất ra file: {output_file}")

except FileNotFoundError:
    print(f"Không tìm thấy file {input_file} trong thư mục hiện tại.")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
