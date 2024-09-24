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

    # Duyệt qua các dòng trong file để tìm SCADA ID
    for i, line in enumerate(lines):
        # Kiểm tra dòng chứa SCADA ID
        if f'record("DEVICE") record_key("{scada_id}")' in line:
            # Dịch chuyển lên 3 dòng để xác định dòng record("SUBSTN")
            substation_line_index = i - 3

            # Kiểm tra xem có đủ dòng để dịch chuyển không
            if substation_line_index >= 0 and 'record("SUBSTN")' in lines[substation_line_index]:
                # Giữ nguyên định dạng và thay thế tên trạm điện
                original_line = lines[substation_line_index]
                # Tìm vị trí record_key và thay thế tên trạm điện
                updated_line = original_line.split('record_key("')[0] + f'record_key("{new_substation_name}")\n'
                lines[substation_line_index] = updated_line
            else:
                print("Không tìm thấy dòng record('SUBSTN') ở vị trí mong đợi.")
            break

    # Ghi nội dung đã chỉnh sửa vào file .ddl mới
    with open(output_file, 'w') as file:
        file.writelines(lines)

    print(f"Đã thay thế tên trạm điện thành công và xuất ra file: {output_file}")

except FileNotFoundError:
    print(f"Không tìm thấy file {input_file} trong thư mục hiện tại.")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")
